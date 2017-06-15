/**
 * Created by zhangxiaoyu on 2017/5/3.
 */


angular.
  module('serverList').
  component('serverList', {
    templateUrl: '/static/app/cmdb/server-list/server-list.template.html',
    controller: function ServerlistListController($http) {
      var self = this;
      self.labels ={
          '在线':"label-success",
          '已下线':"label-default",
          '未知':"label-warning",
          '故障':"label-danger",
          '备用':"label-info",
          '报废':"label-default",
      };
      self.orderProp = 'age';

      $http.get('/cmdb/server_list/').then(function(response) {
        self.servers = response.data;
      });
    }
  });
