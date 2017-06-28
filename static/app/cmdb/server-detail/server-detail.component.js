/**
 * Created by zhangxiaoyu on 2017/6/21.
 */
angular.module('serverDetail').component('serverDetail', {
    templateUrl: '/static/app/cmdb/server-detail/server-detail.template.html',
    controller: ['$http','$routeParams', 'Toastr', function ($http,$routeParams, Toastr) {
        var self = this;
        this.loading = false;
        this.labels = {
            '在线':"label-success",
            '已下线':"label-default",
            '未知':"label-warning",
            '故障':"label-danger",
            '备用':"label-info",
            '报废':"label-default"
        };
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/server/detail/?id=' + $routeParams.assetId).then(function (response) {
                self.server = response.data.data;
                self.loading = false;
            }, function (response) {
                // console.log(response.status)
                Toastr.handle(response,"查看服务器")
                self.loading = false;
            });
        };
        this.get_data();
    }]
});