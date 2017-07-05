from cmdb import models


class AssetHandler(object):
    def __init__( self, request, asset_data,project_id=0, created_by='auto'):
        self.asset_data = asset_data
        self.created_by = created_by
        self.request = request
        self.project_id = project_id

    def log_handler(self,event_type, component=None, detail=""):
        user = self.request.user.username if self.request.user else None
        new_log_obj = models.EventLog(asset= self.asset_obj,
                                      event_type=event_type,
                                      operater=user,
                                      component=component,
                                      detail=detail)
        new_log_obj.save()

    def create_asset(self, asset_type="server"):
        """
        调用相应资产的创建方法创建资产
        invoke asset create function according to it's asset type
        :return:
        """
        manufactory_obj = self._create_or_update_manufactory()
        print(self.project_id)
        project_obj = models.BusinessUnit.objects.filter(id = self.project_id).first()
        self.asset_obj = models.Asset(asset_type="server",
                                      name=self.asset_data.get("essential_information").get("hostname"),
                                      sn=self.asset_data.get("essential_information").get("SN"),
                                      manufactory=manufactory_obj,
                                      status=0,
                                      business_unit=project_obj
                                      )
        self.asset_obj.save()
        func = getattr(self, '_create_%s' % asset_type)
        create_obj = func()
        return create_obj

    def _create_server(self):
        self._create_server_info()
        self._create_cpu_info()
        self._create_ram_info()
        self._create_nic_info()
        self._create_disk_info()

    def _create_server_info(self):
        server_obj = models.Server(asset=self.asset_obj,
                                   created_by=self.created_by,
                                   kernel_release=self.asset_data.get("essential_information").get("kernel_release"),
                                   os_type=self.asset_data.get("essential_information").get("os_type"),
                                   os_distribution=self.asset_data.get("essential_information").get("os_distribution"),
                                   model=self.asset_data.get("essential_information").get("model"),
                                   os_release=self.asset_data.get("essential_information").get("os_release"),
                                   )
        logmsg = "创建服务器%s" % self.asset_obj.name
        self.log_handler(0, detail=logmsg)
        server_obj.save()

    def _create_cpu_info(self):

        cpu_obj = models.CPU(asset=self.asset_obj,
                             model=self.asset_data.get("cpu_information").get("cpu_model"),
                             count=self.asset_data.get("cpu_information").get("cpu_count"),
                             core_count=self.asset_data.get("cpu_information").get("cpu_core_count"),
                             )
        cpu_obj.save()
        logmsg = "新增CPU，型号：%s，数量(个)： %s" % (cpu_obj.model, cpu_obj.count)
        self.log_handler(2, detail=logmsg)

    def _create_nic_info(self):
        for nic_info in self.asset_data.get("interfaces_information"):
            if not (nic_info.get("name") == "lo" or nic_info.get("ip_address") == "127.0.0.1"):
                nic_obj = models.NIC(asset=self.asset_obj,
                                     name=nic_info.get("name"),
                                     netmask=nic_info.get("netmask"),
                                     ip_address=nic_info.get("ip_address"),
                                     ip_address_v6=nic_info.get("ip_address_v6"),
                                     mac_address=nic_info.get("macaddress")
                                     )
                nic_obj.save()
                logmsg = "新增网卡，网卡名：%s IP地址：%s" % (nic_obj.name, nic_obj.ip_address)
                self.log_handler(2, detail=logmsg)

    def _create_disk_info(self):
        for disk_info in self.asset_data.get("disk_information"):
            # if not (nic_info.get("name") == "lo" or nic_info.get("ip_address") == "127.0.0.1"):
            disk_obj = models.Disk(asset=self.asset_obj,
                                  name=disk_info.get("name"),
                                  capacity=disk_info.get("capacity"),
                                  )
            disk_obj.save()
            logmsg = "新增硬盘，硬盘名：%s 容量(MB)：%s" % (disk_obj.name, disk_obj.capacity)
            self.log_handler(2, detail=logmsg)

    def _create_ram_info(self):
        ram_obj = models.RAM(asset=self.asset_obj,
                             capacity=self.asset_data.get("memory_information").get("capacity")
                             )
        ram_obj.save()
        logmsg = "新增内存，容量：%s MB" % ram_obj.capacity
        self.log_handler(2, detail=logmsg)

    def _create_or_update_manufactory(self):
        manufactory = self.asset_data.get("essential_information").get("manufactory")
        manufactory_obj = models.Manufactory.objects.filter(name=manufactory).first()
        if manufactory_obj:
            return manufactory_obj
        else:
            new_manufatory = models.Manufactory(name=manufactory)
            new_manufatory.save()
            return new_manufatory
