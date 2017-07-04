/**
 * Created by zhangxiaoyu on 2017/7/4.
 */

angular.module('groupList').component('groupList',{
    templateUrl: '/static/app/account/group-list/group-list.template.html',
    controller: ['$http', 'Toastr', function ($http, Toastr) {
        var self = this;
        this.loading = false;
        this.get_data = function () {
            self.loading = true;
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
        this.init_create_form_data = function (form) {
            self.create_form_data = {
                "name": ""
            };
            form.name.$dirty = false;
            form.name.$pristine = true;
        };
        this.create_group = function (form) {
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
                $http.post("/api/group/create/", request_data, postCfg)
                    .then(function (response) {
                        self.loading = false
                        Toastr.messager["success"]("创建用户组成功", "成功");
                        self.get_data();
                        $('#create-modal').modal('hide');
                    }, function (response) {
                        self.loading= false;
                        Toastr.handle(response, "创建用户组");
                    });
            }

        };
    }]
});
