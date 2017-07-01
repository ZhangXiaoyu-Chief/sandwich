/**
 * Created by zhangxiaoyu on 2017/6/30.
 */
angular.module('machineroomList').component('machineroomList', {
    templateUrl: '/static/app/cmdb/machineroom-list/machineroom-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        this.num_page = 1;
        this.page = 1;
        this.per_page = 20;
        this.loading = false;
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/machineroom/list/?page=' + self.page + '&per_page=' + self.per_page).then(function (response) {
                self.machinerooms = response.data.data;
                self.num_page = response.data.total_page;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"获取机房列表");
                self.loading = false;
            });
            $http.get('/api/datacenter/list/?page=' + self.page + '&per_page=' + 0).then(function (response) {
                self.datacenters_select = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"获取数据中心");
                self.loading = false;
            });
            $http.get('/api/account/list/').then(function (response) {
                self.admins_select = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                self.loading = false;
            });

        };
        this.get_data();
        this.get_pages = function () {
            var pages = [];
            for (var i = 1; i <= this.num_page; i++) {
                pages.push(i);
            }
            return pages;
        };
        this.change_page = function (page) {
            if (this.page !== page) {
                this.page = page;
                this.get_data();
            }
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
        this.is_active = function (p) {
            if (p === self.page) {
                return 'active';
            } else {
                return "";
            }
        };
        this.init_create_form_data = function (form) {
            // self.loading = true;
            $.fn.modal.Constructor.prototype.enforceFocus = function() {};
            self.create_form_data = {
                name: "",
                datacenter:0,
                contact: "",
                admin: 0,
                memo: "",
                address:""
            };
            $("#datacenter").val(0)
            $("#datacenter").select2({
                language: "zh-CN", //设置 提示语言
                width: "100%", //设置下拉框的宽度
            });
            $("#admin").val(0)
            $("#admin").select2({
                language: "zh-CN", //设置 提示语言
                width: "100%", //设置下拉框的宽度
            });
            form.name.$dirty = false;
            form.name.$pristine = true;
        };
        this.init_change_form_data = function (form, machineroom) {
            // self.loading = true;
            $.fn.modal.Constructor.prototype.enforceFocus = function() {};
            self.change_form_data = {
                id: machineroom.id,
                name: machineroom.name,
                datacenter_id: machineroom.datacenter_id,
                contact: machineroom.contact,
                admin: machineroom.admin_id,
                memo: machineroom.memo,
                address: machineroom.address
            };
            $("#new_datacenter").val(machineroom.datacenter_id)
            $("#new_datacenter").select2({
                language: "zh-CN", //设置 提示语言
                width: "100%", //设置下拉框的宽度
            });
            $("#new_admin").val(machineroom.admin_id)
            $("#new_admin").select2({
                language: "zh-CN", //设置 提示语言
                width: "100%", //设置下拉框的宽度
            });
            form.new_name.$dirty = false;
            form.new_name.$pristine = true;
        };
        this.create_machineroom = function (form) {
            if (!form.$invalid) {
                self.loading = true
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.create_form_data;
                $http.post("/api/machineroom/create/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false;
                        Toastr.messager["success"]("创建成功", "成功");
                        self.get_data();
                        $('#create-model').modal('hide');
                    }, function (response) {
                        // 获取数据失败执行
                        Toastr.handle(response, "创建机房");
                        self.loading = false;
                    });
            }

        };
        this.delete_machineroom = function (machineroom_id) {
            swal({
				title: "确认删除",
				text: "确认要删除该机房吗？删除会连同删除所有机柜等!",
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
                var request_data = {'id':machineroom_id};
                self.loading = true;
                $http.post("/api/machineroom/delete/", request_data, postCfg)
                    .then(function (response) {
                        self.get_data();
                        self.loading = false;
                        Toastr.messager["success"]("删除机房成功", "成功");
                    }, function (response) {
                        self.loading= false;
                        Toastr.handle(response,"删除机房");
                    });
				}
			});
        };
        this.change_machineroom = function (form) {
            if (!form.$invalid) {

                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.change_form_data;
                self.loading = true;
                $http.post("/api/machineroom/change/", request_data, postCfg)
                .then(function (response) {
                    self.loading = false;
                    Toastr.messager["success"]("修改成功", "成功");
                    self.get_data();
                    $('#change-model').modal('hide');
                }, function (response) {
                    // 获取数据失败执行
                    Toastr.handle(response, "编辑机房");
                    self.loading = false;
                });
            }

        };

    }]
});