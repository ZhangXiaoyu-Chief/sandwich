/**
 * Created by zhangxiaoyu on 2017/5/3.
 */


angular.module('serverList').component('serverList', {
    templateUrl: '/static/app/cmdb/server-list/server-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        this.labels = {
            '在线': "label-success",
            '已下线': "label-default",
            '未知': "label-warning",
            '故障': "label-danger",
            '备用': "label-info",
            '报废': "label-default"
        };
        this.num_page = 1;
        this.page = 1;
        this.per_page = 20;
        this.search_input = "";
        this.search = "";
        this.search_data = "";
        this.loading = false;


        this.get_pages = function () {
            var pages = [];
            for (var i = 1; i <= this.num_page; i++) {
                pages.push(i);
            }
            return pages;
        };
        this.is_active = function (p) {
            if (p === self.page) {
                return 'active';
            } else {
                return "";
            }
        };
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/server/list/?page=' + self.page + '&per_page=' + self.per_page + '&search=' + self.search_data).then(function (response) {
                self.servers = response.data.data;
                self.num_page = response.data.total_page;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"查看服务器列表");
                self.loading = false;
            });
            $http.get('/api/project/list/').then(function (response) {
                self.projects = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"获取项目列表");
                self.loading = false;
            });
        };
        this.get_data();
        this.change_page = function (page) {
            if (this.page !== page) {
                this.page = page;
                this.get_data();
            }
        };
        this.search = function (e) {
            self.search_data = self.search_input;
            self.page = 1;
            self.get_data();
        };
        this.previous_page = function (e) {
            if (self.page > 1) {
                self.page -= 1;
            }
        };
        this.next_page = function () {
            if (self.page < self.num_page) {
                self.page += 1;
            }
        };
        this.init_create_form_data = function (form) {
            self.create_form_data = {
                ipaddresses: "",
                port: 22,
                username: "root",
                password: "",
                project:0
            };
            $.fn.modal.Constructor.prototype.enforceFocus = function () {};
            console.log(self.projects[0].id)
            $("#project").val(self.projects[0].id)
            $("#project").select2({
                width: "100%", //设置下拉框的宽度
            });

            // $("#project").trigger('change')
            form.ipaddresses.$dirty = false;
            form.ipaddresses.$pristine = true;
            form.password.$dirty = false;
            form.password.$pristine = true;
        };
        this.create_host = function (form) {
            if (!form.$invalid) {
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };

                var request_data = self.create_form_data
                $('#create-model').modal('hide');

                $http.post("/api/server/create/", request_data, postCfg)
                    .then(function (response) {
                        self.get_data();
                        $.each(response.data.data, function (index, data) {
                            var level = "success";
                            if (data.status) {
                                level = "success";
                            } else {
                                level = "error";
                            }
                            Toastr.messager[level](data.msg, data.ipaddress);
                        });
                    });
            }

        };
        this.delete_host = function (server_id) {
            swal({
				title: "确认删除",
				text: "确认要删除该服务器吗？删除会连同删除所有信息包括操作日志!",
				type: "warning",
				showCancelButton: true,
				confirmButtonColor: "#DD6B55",
				confirmButtonText: "确认删除",
				cancelButtonText: "取消",
				closeOnConfirm: true,
				closeOnCancel: true
			}, function(isConfirm) {
				if(isConfirm) {
				    var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = {'server_id':server_id};
                self.loading = true;
                $http.post("/api/server/delete/", request_data, postCfg)
                    .then(function (response) {
                        self.get_data();
                        self.loading = false;
                        Toastr.messager["success"]("删除服务器成功", "成功");
                    }, function (response) {
                        self.loading= false;
                        Toastr.handle(response,"删除服务器");
                    });
				}
			});
        };
        // this.init_create_form_data();
    }]
});
