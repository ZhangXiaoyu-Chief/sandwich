/**
 * Created by zhangxiaoyu on 2017/6/23.
 */

angular.module('userList').component('userList', {
    templateUrl: '/static/app/account/user-list/user-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        self.reader = new FileReader();
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
                // var username = $('#username').val();
                // var password = $('#password').val();
                // var nickname = $('#nickname').val();
                // var email = $('#email').val();
                // var is_superuser = $('#superuser').prop("checked")
                // var active = $('#actvie').prop("checked")
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
        // this.check_superuser = function () {
        //     console.log($("#checkbox1").prop("checked"))
        // }
        this.upload_avatar = function (form) {
            $http({
                url: '/api/upload/upload_avatar/',
                method: 'POST',
                headers: {
                    'Content-Type': undefined
                },
                transformRequest: function() {
                    var formData = new FormData();
                    formData.append('file', $('#avatar')[0].files[0]  );
                    return formData;
                }
            }).then(function (response) {
                self.create_form_data.avatar = response.data.data;   //返回上传后所在的路径
            }, function (response) {
                Toastr["error"]("上传文件失败", "错误");
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
        // this.init_create_form_data();
    }]
});
