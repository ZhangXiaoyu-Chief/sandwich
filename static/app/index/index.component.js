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

        $http.get("/api/dashboard/business_unit_count/").then(function (response) {
            var myChart = echarts.init(document.getElementById('project-server-charts'));
            // 指定图表的配置项和数据
            var option = Echarts.pie_options;
            option.title.text = '项目资源统计';
            option.legend.data = response.data.data.legend;
            // console.log(option.seri)
            option.series[0].data = response.data.data.data;
            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        });
        $http.get("/api/dashboard/os_relese_count/").then(function (response) {

            // 指定图表的配置项和数据
            var option = Echarts.pie_options;
            option.title.text = '操作系统版本统计';
            option.legend.data = response.data.data.legend;
            // console.log(option.seri)
            option.series[0].data = response.data.data.data;
            // 使用刚指定的配置项和数据显示图表。
            $("#os-release-charts").width($("#project-server-charts").width())
            var myChart2 = echarts.init(document.getElementById('os-release-charts'));

            myChart2.setOption(option);
            myChart2.resize();
        });

    }]
});
