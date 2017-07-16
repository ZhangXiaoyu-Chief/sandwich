/**
 * Created by zhangxiaoyu on 2017/7/16.
 */
/**
 * Created by zhangxiaoyu on 2017/6/15.
 */
angular.module('echarts').factory('Echarts', function () {

    var pie_options = {
        toolbox: {
            show: true,
            feature: {
                saveAsImage: {}
            }
        },
        title: {
            text: '项目服务器资产统计'
        },
        tooltip: {
            trigger: 'item',
            formatter: "{a} <br/>{b}: {c} ({d}%)"
        },
        legend: {
            orient: 'vertical',
            x: 'right',
            y: 'bottom',
            data: ['直接访问', '邮件营销', '联盟广告', '视频广告', '搜索引擎']
        },
        series: [
            {
                name: '服务器数量',
                type: 'pie',
                radius: ['60%', '80%'],
                avoidLabelOverlap: false,
                label: {
                    normal: {
                        show: false,
                        position: 'center'
                    },
                    emphasis: {
                        show: true,
                        textStyle: {
                            fontSize: '30',
                            fontWeight: 'bold'
                        }
                    }
                },
                labelLine: {
                    normal: {
                        show: false
                    }
                },
                data: [
                    {value: 335, name: '直接访问'},
                    {value: 310, name: '邮件营销'},
                    {value: 234, name: '联盟广告'},
                    {value: 135, name: '视频广告'},
                    {value: 1548, name: '搜索引擎'}
                ]
            }
        ]
    };
    return {
        pie_options: pie_options,
    };
});

