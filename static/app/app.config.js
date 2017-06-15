/**
 * Created by zhangxiaoyu on 2017/6/14.
 */

'use strict';

angular.
  module('sandwichApp').
  config(['$locationProvider', '$routeProvider',
    function config($locationProvider, $routeProvider) {
      $locationProvider.hashPrefix('!');

      $routeProvider.
        when('/index', {
          template: '<index></index>'
        }).
        when('/servers', {
          template: '<server-list></server-list>'
        }).
        when('/phones/:phoneId', {
          template: '<phone-detail></phone-detail>'
        }).
        otherwise('/index');
    }
  ]);
