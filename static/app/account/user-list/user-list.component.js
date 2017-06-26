/**
 * Created by zhangxiaoyu on 2017/6/23.
 */

angular.module('userList').component('userList', {
    templateUrl: '/static/app/account/user-list/user-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        self.reader = new FileReader();
        // self.avatar = "static/images/default-user.png";
        self.avatar = "static/images/default-user.png";
        this.get_status_label = function (status) {
            if (status) {
                return "label-success";
            } else {
                return "label-danger";
            }
        };
        this.get_status_str = function (status) {
            if (status) {
                return "活动";
            } else {
                return "禁用";
            }
        };
        this.get_usertype = function (status) {
            if (status) {
                return "超级用户";
            } else {
                return "普通用户";
            }
        };
        this.loading = false;
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/account/list/').then(function (response) {
                self.users = response.data.data;
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
        this.create_user = function (form) {
            if (!form.$invalid) {
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.create_form_data;
                self.loading = true
                $http.post("/api/account/create/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false
                        Toastr["success"]("创建用户成功", "成功");
                        self.get_data();
                    }, function (response) {
                        self.loading= false
                        if (response.status === 401) {
                            window.location.href = response.data.data.login_url
                        }
                        if(response.status===403){
                            Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                        }
                        if(response.status===500){
                            Toastr["error"]("创建用户失败", "未知错误");
                        }
                    });
            }

        };
        this.edit_user = function (form) {
            if (!form.$invalid) {
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.edit_form_data;
                self.loading = true;
                $http.post("/api/account/change/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false
                        Toastr["success"]("编辑用户成功", "成功");
                        self.get_data();
                    }, function (response) {
                        self.loading= false
                        if (response.status === 401) {
                            window.location.href = response.data.data.login_url
                        }
                        if(response.status===403){
                            Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                        }
                        if(response.status===500){
                            Toastr["error"]("编辑用户失败", "未知错误");
                        }
                        if(response.status===416){
                            Toastr["error"]("用户名已经存在", "错误");
                        }
                        if(response.status===404){
                            Toastr["error"]("要编辑的用户不存在或已被删除", "错误");
                        }
                    });
            }

        };
        // this.check_superuser = function () {
        //     console.log($("#checkbox1").prop("checked"))
        // }
        this.upload_avatar = function (form,selecter) {
            $http({
                url: '/api/upload/upload_avatar/',
                method: 'POST',
                headers: {
                    'Content-Type': undefined
                },
                transformRequest: function() {
                    var formData = new FormData();
                    formData.append('file', $(selecter)[0].files[0]  );
                    return formData;
                }
            }).then(function (response) {
                // self.create_form_data.avatar = response.data.data;   //返回上传后所在的路径
                self.avatar = response.data.data;   //返回上传后所在的路径
            }, function (response) {
                Toastr["error"]("上传头像失败", "错误");
            });
        };
        this.init_create_form_data = function (form) {
            self.create_form_data = {
                "username": "",
                "password": "",
                "password2": "",
                "nickname": "",
                "avatar": "static/images/default-user.png",
                "email": "",
                "is_superuser": false,
                "active": true,
            };
            // self.avatar = "static/images/default-user.png";
            form.username.$dirty = false;
            form.username.$pristine = true;
            form.password.$dirty = false;
            form.password.$pristine = true;
            // form.nickname.$dirty = false;
            // form.nickname.$pristine = true;
        };
        this.disable = function (user_id) {
            var postCfg = {
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                transformRequest: function (data) {
                    return $.param(data);
                }
            };
            var request_data = {"user_id": user_id}
            self.loading = true;
            $http.post("/api/account/disable/", request_data, postCfg).then(function (response) {
                self.loading = false;
                Toastr["success"]("禁用用户成功", "成功");
                self.get_data();
            }, function (response) {
                self.loading= false;
                if (response.status === 401) {
                    window.location.href = response.data.data.login_url
                }
                if(response.status===403){
                    Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                }
                if(response.status===500){
                    Toastr["error"]("禁用用户失败", "未知错误");
                }
                if(response.status===404){
                    Toastr["error"]("要禁用的用户不存在或已被删除", "错误");
                }
            });
        };
        this.enable = function (user_id) {
            var postCfg = {
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                transformRequest: function (data) {
                    return $.param(data);
                }
            };
            var request_data = {"user_id": user_id}
            self.loading = true;
            $http.post("/api/account/enable/", request_data, postCfg).then(function (response) {
                self.loading = false;
                Toastr["success"]("启用用户成功", "成功");
                self.get_data();
            }, function (response) {
                self.loading= false;
                if (response.status === 401) {
                    window.location.href = response.data.data.login_url
                }
                if(response.status===403){
                    Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                }
                if(response.status===500){
                    Toastr["error"]("启用用户失败", "未知错误");
                }
                if(response.status===404){
                    Toastr["error"]("要启用的用户不存在或已被删除", "错误");
                }
            });
        };
        this.init_edit_form_data = function (form, user_id) {
            self.loading = true;
            $http.get("/api/account/user/?user_id=" + user_id).then(function (response) {
                self.edit_form_data = response.data.data;
                self.avatar = response.data.data.avatar;
                self.loading = false;
            }, function (response) {
                self.loading = false;
                self.loading= false;
                if (response.status === 401) {
                    window.location.href = response.data.data.login_url
                }
                if(response.status===403){
                    Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
                }
                if(response.status===500){
                    Toastr["error"]("获取用户信息失败", "未知错误");
                }
                if(response.status===404){
                    Toastr["error"]("要编辑的用户不存在或已被删除", "错误");
                }
            });
        };
        // this.init_create_form_data();
    }]
});
