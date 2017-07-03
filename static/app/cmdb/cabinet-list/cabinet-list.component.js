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
    }]
});