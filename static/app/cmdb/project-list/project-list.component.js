/**
 * Created by zhangxiaoyu on 2017/6/27.
 */


angular.module('projectList').component('projectList', {
    templateUrl: '/static/app/cmdb/project-list/project-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        this.num_page = 1;
        this.page = 1;
        this.per_page = 20;
        this.loading = false;


        this.get_pages = function () {
            var pages = [];
            for (var i = 1; i <= this.num_page; i++) {
                pages.push(i);
            }
            return pages;
        };
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/project/list/?page=' + self.page + '&per_page=' + self.per_page).then(function (response) {
                self.projects = response.data.data;
                self.num_page = response.data.total_page;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                if (response.status === 401) {
                    window.location.href = response.data.data.login_url
                }
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
            self.loading = true;
            $http.get('/api/project/list/?page=' + self.page + '&per_page=0').then(function (response) {

                self.loading = false;
                self.projects_select = response.data.data;

            }, function (response) {
                // 获取数据失败执行
                if (response.status === 401) {
                    window.location.href = response.data.data.login_url
                }
                self.loading = false;
            });

            $.fn.modal.Constructor.prototype.enforceFocus = function() {};
            self.create_form_data = {
                name: "",
                parent: 0,
                memo: "",
            };
            $("#parent").val(0)
            $(".js-example-basic-single").select2({
                language: "zh-CN", //设置 提示语言
                width: "100%", //设置下拉框的宽度
            });
            form.name.$dirty = false;
            form.name.$pristine = true;
        };
        this.create_project = function (form) {
            if (!form.$invalid) {
                self.loading = true
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.create_form_data;
                $http.post("/api/project/create/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false;
                        Toastr["success"]("创建成功", "成功");
                        self.get_data();
                        $('.bs-example-modal-lg').modal('hide');
                    }, function (response) {
                        // 获取数据失败执行
                        if (response.status === 401) {
                            window.location.href = response.data.data.login_url
                        }
                        if(response.status===403){
                            Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                        }
                        if(response.status===416){
                            Toastr["error"]("创建项目失败，项目名称已经存在", "错误");
                        }
                        if(response.status===500){
                            Toastr["error"]("创建项目失败", "未知错误");
                        }
                        self.loading = false;
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
                        Toastr["success"]("删除服务器成功", "成功");
                    }, function (response) {
                        self.loading= false;
                        if (response.status === 401) {
                            window.location.href = response.data.data.login_url
                        }
                        if(response.status===403){
                            Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                        }
                        if(response.status===500){
                            Toastr["error"]("删除服务器失败", "未知错误");
                        }
                        if(response.status===404){
                            Toastr["error"]("要删除的服务器不存在或已被删除", "错误");
                        }
                    });
				}
			});
        };
        // this.init_create_form_data();
    }]
});
