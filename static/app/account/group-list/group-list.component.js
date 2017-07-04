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
    }]
});
