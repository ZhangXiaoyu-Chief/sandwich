/**
 * Created by zhangxiaoyu on 2017/5/3.
 */


angular.
  module('serverList').
  component('serverList', {
    templateUrl: '/static/app/cmdb/server-list/server-list.template.html',
    controller: ['$http','Toastr', function ($http, Toastr) {
      var self = this;
      this.labels = {
          '在线':"label-success",
          '已下线':"label-default",
          '未知':"label-warning",
          '故障':"label-danger",
          '备用':"label-info",
          '报废':"label-default"
      };
      this.num_page = 1;
      this.page = 1;
      this.per_page = 20;
      this.search_input = "";
      this.search = "";

      this.get_pages = function () {
          var pages = [];
          for(var i=1;i<=this.num_page;i++){
              pages.push(i);
          }
          return pages;
      };
      this.is_active = function (p) {
          if(p === self.page){
              return 'active';
          }else {
              return "";
          }
      };
      this.get_data = function () {
          $http.get('/api/server/list/?page=' + self.page + '&per_page=' + self.per_page + '&search=' + self.search_data).then(function(response) {
            self.servers = response.data.data;
            self.num_page = response.data.total_page;
          }, function () {
              // 获取数据失败执行
          });
      };
      this.get_data();
      this.change_page = function (page) {
          if(this.page !== page){
              this.page = page;
              this.get_data();
          }
      };
      this.search = function (e) {
          self.search_data = self.search_input;
          self.page = 1;
          self.get_data();
      };
      this.previous_page = function (e) {
          if(self.page >1){
              self.page -= 1;
          }
      };
      this.next_page = function () {
          if(self.page < self.num_page){
              self.page += 1;
          }
      };
    }]
  });
