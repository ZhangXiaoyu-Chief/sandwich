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
                Toastr.handle(response,"获取用户列表");
                self.loading = false;
            });
            $http.get('/api/group/list/').then(function (response) {
                self.groups = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"获取用户组列表");
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
                self.loading = true;
                request_data.avatar = self.avatar;
                var group = $('#group').val()
                if(group){
                    request_data.group = $('#group').val().toString();
                }else {
                    request_data.group = [];
                }

                $http.post("/api/account/create/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false
                        Toastr.messager["success"]("创建用户成功", "成功");
                        self.get_data();
                        $('.bs-example-modal-lg').modal('hide');
                    }, function (response) {
                        self.loading= false;
                        Toastr.handle(response, "创建用户");
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
                request_data.group = $('#new_group').val().toString();
                request_data.avatar = self.avatar;
                self.loading = true;
                $http.post("/api/account/change/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false;
                        Toastr.messager["success"]("编辑用户成功", "成功");
                        $('.edit-model').modal('hide');
                        self.get_data();
                    }, function (response) {
                        self.loading= false;
                        Toastr.handle(response, "编辑用户");
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
                Toastr.messager["error"]("上传头像失败", "错误");
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
                "status": true,
            };
            self.avatar = "static/images/default-user.png";
            form.username.$dirty = false;
            form.username.$pristine = true;
            form.password.$dirty = false;
            form.password.$pristine = true;
            $('#group').selectpicker({
                // 'selectedText': 'cat',
                'noneSelectedText': '请选择用户组'
            });
            $('#group').selectpicker('val',[]);
        };
        // this.disable = function (user_id) {
        //     var postCfg = {
        //         headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        //         transformRequest: function (data) {
        //             return $.param(data);
        //         }
        //     };
        //     var request_data = {"user_id": user_id}
        //     self.loading = true;
        //     $http.post("/api/account/disable/", request_data, postCfg).then(function (response) {
        //         self.loading = false;
        //         Toastr["success"]("禁用用户成功", "成功");
        //         self.get_data();
        //     }, function (response) {
        //         self.loading= false;
        //         if (response.status === 401) {
        //             window.location.href = response.data.data.login_url
        //         }
        //         if(response.status===403){
        //             Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
        //         }
        //         if(response.status===500){
        //             Toastr["error"]("禁用用户失败", "未知错误");
        //         }
        //         if(response.status===404){
        //             Toastr["error"]("要禁用的用户不存在或已被删除", "错误");
        //         }
        //     });
        // };
        // this.enable = function (user_id) {
        //     var postCfg = {
        //         headers: {'Content-Type': 'application/x-www-form-urlencoded'},
        //         transformRequest: function (data) {
        //             return $.param(data);
        //         }
        //     };
        //     var request_data = {"user_id": user_id}
        //     self.loading = true;
        //     $http.post("/api/account/enable/", request_data, postCfg).then(function (response) {
        //         self.loading = false;
        //         Toastr["success"]("启用用户成功", "成功");
        //         self.get_data();
        //     }, function (response) {
        //         self.loading= false;
        //         if (response.status === 401) {
        //             window.location.href = response.data.data.login_url
        //         }
        //         if(response.status===403){
        //             Toastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
        //         }
        //         if(response.status===500){
        //             Toastr["error"]("启用用户失败", "未知错误");
        //         }
        //         if(response.status===404){
        //             Toastr["error"]("要启用的用户不存在或已被删除", "错误");
        //         }
        //     });
        // };
        this.change_status = function(user){
            var postCfg = {
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                transformRequest: function (data) {
                    return $.param(data);
                }
            };
            var request_data = {"user_id": user.id,"status": ! user.status};
            var action="禁用";
            if(!user.status){
                action="启用";
            }
            self.loading = true;
            $http.post("/api/account/change_status/", request_data, postCfg).then(function (response) {
                self.loading = false;
                Toastr.messager["success"](action + "用户成功", "成功");
                self.get_data();

            }, function (response) {
                self.loading= false;
                Toastr.handle(response, action + "用户");
            });

        };
        this.init_edit_form_data = function (form, user_id) {
            self.loading = true;
            $http.get("/api/account/user/?user_id=" + user_id).then(function (response) {
                self.edit_form_data = response.data.data;
                self.avatar = response.data.data.avatar;
                self.loading = false;
                var group_list =[]
                for(i=0;i<response.data.data.group.length;i++){
                    group_list.push(response.data.data.group[i].id)
                }
                $('#new_group').selectpicker({
                    // 'selectedText': 'cat',
                    'noneSelectedText': '请选择用户组'
                });
                $('#new_group').selectpicker('val',group_list);
            }, function (response) {
                self.loading = false;
                Toastr.handle(response, "编辑用户");
            });
            form.edit_username.$dirty = false;
            form.edit_username.$pristine = true;

        };
        this.init_pass_form_data = function (form, user_id) {
            self.pass_form_data = {
                "user_id": user_id,
                "newpassword": "",
                "newpassword2": ""
            };
            form.newpassword.$dirty = false;
            form.newpassword.$pristine = true;
            form.newpassword2.$dirty = false;
            form.newpassword2.$pristine = true;
        };
        this.change_password = function (form) {
            if (!form.$invalid) {
                var postCfg = {
                    headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                    transformRequest: function (data) {
                        return $.param(data);
                    }
                };
                var request_data = self.pass_form_data;
                self.loading = true;
                $http.post("/api/account/changepwd/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false;
                        Toastr.messager["success"]("密码修改成功", "成功");
                    }, function (response) {
                        Toastr.handle(response, "修改");
                    });
            }
        };
        this.get_group_display = function (user) {
            var group_list =[]
            for(i=0;i<user.group.length;i++){
                group_list.push(user.group[i].name)
            }
            return group_list.toString()
        };
        // this.init_create_form_data();
    }]
});
