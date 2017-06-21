#!/usr/bin/env python
# -*- coding=utf-8 -*-
import json, sys, os
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory, Host, Group
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible.executor.playbook_executor import PlaybookExecutor


class MyInventory(object):
    def __init__(self, resource, loader, variable_manager):
        self.resource = resource
        # 创建主机配置清单对象
        self.inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list=[])
        self.dynamic_inventory()

    def add_dynamic_group(self, hosts, groupname, groupvars=None):
        """
        动态创建主机组
        :param hosts: 主机列表
        :param groupname: 组机组名
        :param groupvars: 组参数
        :return: 
        """
        my_group = Group(name=groupname)  # 创建主机组对象
        if groupvars:
            # 设置主机组参数
            for key, value in groupvars.items():
                my_group.set_variable(key, value)
        for host in hosts:
            # 设置链接参数
            hostname = host.get("hostname")
            hostip = host.get('ip', hostname)
            hostport = host.get("port")
            username = host.get("username")
            password = host.get("password")
            ssh_key = host.get("ssh_key")
            my_host = Host(name=hostname, port=hostport)  # 创建主机对象
            # 设置主机参数
            my_host.set_variable('ansible_ssh_host', hostip)
            my_host.set_variable('ansible_ssh_port', hostport)
            my_host.set_variable('ansible_ssh_user', username)
            my_host.set_variable('ansible_ssh_pass', password)
            my_host.set_variable('ansible_sudo_pass', password)
            my_host.set_variable('ansible_sudo', 'yes')
            my_host.set_variable('ansible_ssh_private_key_file', ssh_key)
            for key, value in host.items():
                if key not in ["hostname", "port", "username", "password"]:
                    my_host.set_variable(key, value)
            my_group.add_host(my_host)  # 将主机对象添加到主机组对象中

        self.inventory.add_group(my_group)  # 将主机组添加到主机配置清单中

    def dynamic_inventory(self):
        """
        动态配置主机清单对象
        :return: 
        """
        if isinstance(self.resource, list):
            # 只是主机列表，也就是所有的主机都属于同一个默认的主机组
            self.add_dynamic_group(self.resource, 'default_group')
        elif isinstance(self.resource, dict):
            # 包含组的主机列表，也就是有若干个主机组
            for groupname, hosts_and_vars in self.resource.items():
                self.add_dynamic_group(hosts_and_vars.get("hosts"), groupname, hosts_and_vars.get("vars"))


class ModelResultsCollector(CallbackBase):
    """
    单独执行模块的结果收集对象
    """

    def __init__(self, *args, **kwargs):
        super(ModelResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}
        self.host_ok = {}
        self.host_unreachable = {}
        self.host_failed = {}

    def v2_runner_on_unreachable(self, result):
        """
        不可及收集结果函数
        :param result: 执行结果
        :return: 
        """
        self.host_unreachable[result._host.get_name()] = result

    def v2_runner_on_ok(self, result, *args, **kwargs):
        """
        成功执行收集结果函数
        :param result: 执行结果
        :param args: 
        :param kwargs: 
        :return: 
        """
        self.host_ok[result._host.get_name()] = result

    def v2_runner_on_failed(self, result, *args, **kwargs):
        """
        执行失败收集结果函数
        :param result: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        self.host_failed[result._host.get_name()] = result


class PlayBookResultsCollector(CallbackBase):
    """
    PlayBook结果收集类
    """
    CALLBACK_VERSION = 2.0

    def __init__(self, taskList, *args, **kwargs):
        super(PlayBookResultsCollector, self).__init__(*args, **kwargs)
        self.task_ok = {}
        self.task_skipped = {}
        self.task_failed = {}
        self.task_status = {}
        self.task_unreachable = {}

    def v2_runner_on_ok(self, result, *args, **kwargs):
        if taskList.has_key(result._host.get_name()):
            data = {}
            data['task'] = str(result._task).replace("TASK: ", "")
            taskList[result._host.get_name()].get('ok').append(data)
        self.task_ok[result._host.get_name()] = taskList[result._host.get_name()]['ok']

    def v2_runner_on_failed(self, result, *args, **kwargs):
        data = {}
        msg = None
        if taskList.has_key(result._host.get_name()):
            data['task'] = str(result._task).replace("TASK: ", "")
            msg = result._result.get('stderr')
            if msg is None:
                results = result._result.get('results')
                if result:
                    task_item = {}
                    for rs in results:
                        msg = rs.get('msg')
                        if msg:
                            task_item[rs.get('item')] = msg
                            data['msg'] = task_item
                    taskList[result._host.get_name()]['failed'].append(data)
                else:
                    msg = result._result.get('msg')
                    data['msg'] = msg
                    taskList[result._host.get_name()].get('failed').append(data)
        else:
            data['msg'] = msg
            taskList[result._host.get_name()].get('failed').append(data)
        self.task_failed[result._host.get_name()] = taskList[result._host.get_name()]['failed']

    def v2_runner_on_unreachable(self, result):
        self.task_unreachable[result._host.get_name()] = result

    def v2_runner_on_skipped(self, result):
        if taskList.has_key(result._host.get_name()):
            data = {}
            data['task'] = str(result._task).replace("TASK: ", "")
            taskList[result._host.get_name()].get('skipped').append(data)
        self.task_ok[result._host.get_name()] = taskList[result._host.get_name()]['skipped']

    def v2_playbook_on_stats(self, stats):
        hosts = sorted(stats.processed.keys())
        for h in hosts:
            t = stats.summarize(h)
            self.task_status[h] = {
                "ok": t['ok'],
                "changed": t['changed'],
                "unreachable": t['unreachable'],
                "skipped": t['skipped'],
                "failed": t['failures']
            }


class ANSRunner(object):
    """
    自定义的ansible执行类
    """

    def __init__(self, resource, *args, **kwargs):
        self.resource = resource
        self.inventory = None  # 资源清单对象
        self.variable_manager = None
        self.loader = None
        self.options = None
        self.passwords = None
        self.callback = None
        self.__initializeData()
        self.results_raw = {}

    def __initializeData(self):
        """
        初始化Ansible组件对象函数
        :return: 
        """
        Options = namedtuple('Options', ['connection', 'module_path', 'forks', 'timeout','sudo',
                                         'ask_pass', 'private_key_file', 'ssh_common_args', 'ssh_extra_args',
                                         'sftp_extra_args',
                                         'scp_extra_args', 'become', 'become_method', 'become_user', 'ask_value_pass',
                                         'verbosity',
                                         'check', 'listhosts', 'listtasks', 'listtags', 'syntax','ask_sudo_pass', 'sudo_user', 'remote_user'])


        # Options = namedtuple('Options',
        #                      ['connection',
        #                       'remote_user',
        #                       'ask_sudo_pass',
        #                       'verbosity',
        #                       'ack_pass',
        #                       'module_path',
        #                       'forks',
        #                       'become',
        #                       'become_method',
        #                       'become_user',
        #                       'check',
        #                       'listhosts',
        #                       'listtasks',
        #                       'listtags',
        #                       'syntax',
        #                       'sudo_user',
        #                       'sudo'])
        # 初始化需要的对象
        # options = Options(connection='smart',
        #                   remote_user='root',
        #                   ack_pass=True,
        #                   sudo_user='root',
        #                   forks=5,
        #                   sudo='yes',
        #                   ask_sudo_pass=False,
        #                   verbosity=5,
        #                   module_path=None,
        #                   become=True,
        #                   become_method='sudo',
        #                   become_user='root',
        #                   check=None,
        #                   listhosts=None,
        #                   listtasks=None,
        #                   listtags=None,
        #                   syntax=None)


        self.variable_manager = VariableManager()  # 创建VariableManager对象
        self.loader = DataLoader()  # 创建DataLoader组件对象，DataLoader组件主要用来读取YAML或者JSON上下文，从给定的文件中
        self.options = Options(connection='paramiko', module_path=None, forks=100, timeout=10, ask_pass=None,
                               private_key_file=None, ssh_common_args=None,
                               ssh_extra_args=None,
                               sftp_extra_args=None, scp_extra_args=None, become=None, become_method='sudo',
                               become_user='admin', ask_value_pass=False, verbosity=None, check=False, listhosts=False,
                               listtasks=False, listtags=False, syntax=False,ask_sudo_pass=True , sudo='no', sudo_user='admin', remote_user='admin')
        # self.options = options
        Options = namedtuple('Options',
                             ['connection',
                              'remote_user',
                              'ask_sudo_pass',
                              'verbosity',
                              'ack_pass',
                              'module_path',
                              'forks',
                              'become',
                              'become_method',
                              'become_user',
                              'check',
                              'listhosts',
                              'listtasks',
                              'listtags',
                              'syntax',
                              'sudo_user',
                              'sudo'])
        # 初始化需要的对象
        self.options = Options(connection='ssh',
                          remote_user='root',
                          ack_pass=None,
                          sudo_user='root',
                          forks=5,
                          sudo='yes',
                          ask_sudo_pass=False,
                          verbosity=5,
                          module_path=None,
                          become=True,
                          become_method='sudo',
                          become_user='root',
                          check=None,
                          listhosts=None,
                          listtasks=None,
                          listtags=None,
                          syntax=None)
        self.passwords = dict(sshpass=None, becomepass=None)
        # 创建Inventory（资源清单）对象
        self.inventory = MyInventory(self.resource, self.loader, self.variable_manager).inventory
        self.variable_manager.set_inventory(self.inventory)

    def run_model(self, host_list, module_name, module_args):
        """
        执行andible ad-hoc模块
        module_name: 模块名
        module_args: 模块参数
        """
        play_source = dict(
            name="Ansible Play",
            hosts=host_list,
            gather_facts='no',
            tasks=[dict(action=dict(module=module_name, args=module_args))]
        )
        # 创建play对象
        play = Play().load(play_source, variable_manager=self.variable_manager, loader=self.loader)
        tqm = None
        # 创建结果收集对象
        self.callback = ModelResultsCollector()
        try:
            tqm = TaskQueueManager(
                inventory=self.inventory,
                variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options,
                passwords=self.passwords,
            )
            tqm._stdout_callback = self.callback
            result = tqm.run(play)
        finally:
            if tqm is not None:
                tqm.cleanup()

    def run_playbook(self, host_list, playbook_path, ):
        """
        run ansible palybook
        """
        global taskList
        taskList = {}
        for host in host_list:
            taskList[host] = {}
            taskList[host]['ok'] = []
            taskList[host]['failed'] = []
            taskList[host]['skppied'] = []
        try:
            self.callback = PlayBookResultsCollector(taskList)
            executor = PlaybookExecutor(
                playbooks=[playbook_path], inventory=self.inventory, variable_manager=self.variable_manager,
                loader=self.loader,
                options=self.options, passwords=self.passwords,
            )
            executor._tqm._stdout_callback = self.callback
            executor.run()
        except Exception as e:
            return False

    def get_model_result(self):
        """
        结果手机
        :return: 返回结果字符串类似如下格式
                    {
                      "unreachable": {},
                      "success": {},
                      "failed": {}
                    }
        """
        self.results_raw = {'success': {}, 'failed': {}, 'unreachable': {}}
        for host, result in self.callback.host_ok.items():
            self.results_raw['success'][host] = result._result

        for host, result in self.callback.host_failed.items():
            self.results_raw['failed'][host] = result._result

        for host, result in self.callback.host_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        # return json.dumps(self.results_raw, indent=2)
        return self.results_raw

    def get_playbook_result(self):
        self.results_raw = {'skipped': {}, 'failed': {}, 'ok': {}, "status": {}, 'unreachable': {}}

        for host, result in self.callback.task_ok.items():
            self.results_raw['ok'][host] = result

        for host, result in self.callback.task_failed.items():
            self.results_raw['failed'][host] = result


        for host, result in self.callback.task_status.items():
            self.results_raw['status'][host] = result

        for host, result in self.callback.task_skipped.items():
            self.results_raw['skipped'][host] = result

        for host, result in self.callback.task_unreachable.items():
            self.results_raw['unreachable'][host] = result._result
        return json.dumps(self.results_raw)


if __name__ == '__main__':
    # resource = {
    #     "dynamic_host": {  # 定义的动态主机名，需要跟playbook里面的hosts对应
    #         "hosts": [
    #             {"hostname": "59.110.216.100", "port": "22", "username": "root", "password": "!Jesus@smart8345"},
    #         ],
    #     }
    # }
    resource = [{"hostname": "60.34.40.1", "port": "22", "username": "admin", "password": "bsszyh@1qaz!"}]

    rbt = ANSRunner(resource)  # resource可以是列表或者字典形式，如果做了ssh-key认证，就不会通过账户密码方式认证
    rbt.run_model(host_list=["default_group"], module_name='shell', module_args="hostname")
    data = rbt.get_model_result()
    # print(data['unreachable']['60.34.40.1']['msg'])
    print(json.dumps(data, indent=2))