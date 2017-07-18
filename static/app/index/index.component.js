/**
 * Created by zhangxiaoyu on 2017/6/15.
 */

angular.module('index').component('index', {
    templateUrl: '/static/app/index/index.template.html',
    controller: ['$http', 'Echarts',function ServerlistListController($http, Echarts) {
        'use strict';
        var self = this;
        $('.carousel').carousel({
            interval: 5000
        });
        this.dashboard_info = {

        };
        this.log_loader = false;
        this.project_count_loader = false;
        this.status_count_loader = false;
        this.release_count_loader = false;



        $http.get("/api/dashboard/info/").then(function (response) {

            // 指定图表的配置项和数据
            self.dashboard_info = response.data.data;
        });
        this.get_asset_count = function () {
            console.log(12121)
            self.project_count_loader = true;
            $http.get("/api/dashboard/business_unit_count/").then(function (response) {
                var projectChart = echarts.init(document.getElementById('project-server-charts'));
                // 指定图表的配置项和数据
                var option = Echarts.pie_options;
                option.title.text = '项目资源统计';
                option.legend.data = response.data.data.legend;
                // console.log(option.seri)
                option.series[0].data = response.data.data.data;
                // 使用刚指定的配置项和数据显示图表。
                projectChart.setOption(option);
                self.project_count_loader = false;
            });
            self.release_count_loader = true
            $http.get("/api/dashboard/os_relese_count/").then(function (response) {

                // 指定图表的配置项和数据
                var option = Echarts.pie_options;
                option.title.text = '操作系统版本统计';
                option.legend.data = response.data.data.legend;
                // console.log(option.seri)
                option.series[0].data = response.data.data.data;
                // 使用刚指定的配置项和数据显示图表。
                $("#os-release-charts").width($("#project-server-charts").width())
                var releaseChart = echarts.init(document.getElementById('os-release-charts'));

                releaseChart.setOption(option);
                self.release_count_loader = false
            });
            self.status_count_loader = true;
            $http.get("/api/dashboard/status_count/").then(function (response) {

                // 指定图表的配置项和数据
                var option = Echarts.pie_options;
                option.title.text = '状态统计';
                option.legend.data = response.data.data.legend;
                // console.log(option.seri)
                option.series[0].data = response.data.data.data;
                // 使用刚指定的配置项和数据显示图表。
                $("#status-charts").width($("#project-server-charts").width())
                var statusChart = echarts.init(document.getElementById('status-charts'));

                statusChart.setOption(option);
                self.status_count_loader = false;
            });
        };
        this.get_asset_log = function () {
            this.log_loader= true
            $http.get("/api/dashboard/asset_log/").then(function (response) {

                // 指定图表的配置项和数据
                self.asset_logs = response.data.data;
                self.log_loader= false;
            });

        };
        this.get_asset_log();
        this.get_asset_count();


    }]
});
