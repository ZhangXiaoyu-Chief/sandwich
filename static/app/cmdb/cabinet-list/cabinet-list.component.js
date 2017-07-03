/**
 * Created by zhangxiaoyu on 2017/7/1.
 */
angular.module('cabinetList').component('cabinetList', {
    templateUrl: '/static/app/cmdb/cabinet-list/cabinet-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        this.num_page = 1;
        this.page = 1;
        this.per_page = 20;
        this.loading = false;
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/cabinet/list/?page=' + self.page + '&per_page=' + self.per_page).then(function (response) {
                self.cabinets = response.data.data;
                self.num_page = response.data.total_page;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"获取机柜列表");
                self.loading = false;
            });
            $http.get('/api/machineroom/list/').then(function (response) {
                self.machinerooms_select = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"获取机房列表");
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
                number: "",
                machineroom:self.machinerooms_select[0].id,
                slotcount: 0,
                memo: "",
            };
            $("#machineroom").val(self.machinerooms_select[0].id)
            $("#machineroom").select2({
                language: "zh-CN", //设置 提示语言
                width: "100%", //设置下拉框的宽度
            });

            form.number.$dirty = false;
            form.number.$pristine = true;
        };
        this.create_cabinet = function (form) {
            if (!form.$invalid) {
                self.loading = true
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.create_form_data;
                $http.post("/api/cabinet/create/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false;
                        Toastr.messager["success"]("创建成功", "成功");
                        self.get_data();
                        $('#create-model').modal('hide');
                    }, function (response) {
                        // 获取数据失败执行
                        Toastr.handle(response, "创建机柜");
                        self.loading = false;
                    });
            }
        };
        this.delete_cabinet = function (cabinet_id) {
            swal({
				title: "确认删除",
				text: "确认要删除该机柜吗？",
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
                var request_data = {'id':cabinet_id};
                self.loading = true;
                $http.post("/api/cabinet/delete/", request_data, postCfg)
                    .then(function (response) {
                        self.get_data();
                        self.loading = false;
                        Toastr.messager["success"]("删除机柜成功", "成功");
                    }, function (response) {
                        self.loading= false;
                        Toastr.handle(response,"删除机柜");
                    });
				}
			});
        };
    }]
});