/**
 * Created by zhangxiaoyu on 2017/7/20.
 */


angular.module('monitorIndex').component('monitorIndex', {
    templateUrl: '/static/app/monitor/monitor-index/monitor-index.template.html',
    controller: ['$http', 'Toastr','Echarts', function ($http, Toastr,Echarts) {
        var self = this;
        this.get_host_tree = function () {
            self.loading = true;
            $http.get('/api/server/host_tree').then(function (response) {
                self.host_tree = response.data.data;
                self.loading = false;
                var tree_data = []
                $.each(self.host_tree, function (k,v) {
                    var children_list = []
                    for(var i=0;i<v.length;i++){
                        children_list.push({
                            "id":"host-" + v[i].name,
                            "text": v[i].name +"(" + v[i].management_ip +")"
                        });
                    }
                    var father_node = {
                        "id":"project"+k,
                        "text":k,
                        "state": {
                            "opened": false,          //展示第一个层级下面的node
                            "disabled": false         //该根节点不可点击
                        },
                        "children":children_list
                    };
                    tree_data.push(father_node);


                });
                $("#host-treeview").jstree({
                    'core' : {
                        "multiple" : false,
                        'data' : tree_data,
                        'dblclick_toggle': false          //禁用tree的双击展开
                    }
                });

                $('#host-treeview').on("select_node.jstree", function (event, data) {
                    if("node" in data){
                        if(data.node.id.indexOf("host")===0){
                            var hostname = data.node.id.substring(5)
                            $http.get('/api/monitor/graphs/?hostname='+hostname).then(function (response) {
                                self.graphs = response.data.data;
                                if(self.graphs.length ===0){
                                    Toastr.messager["error"]("该主机不在监控范围或没有图形", "获取监控图表失败");
                                }
                            }, function (response) {
                                self.graphs=[];
                                Toastr.handle(response, "获取监控图表");
                            });
                        }
                    }
                });
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response,"查看服务器列表");
                self.loading = false;
            });
        };
        this.get_host_tree();
        this.render_chart = function(i,chart_data){
            if(chart_data.graph_type !== "2"){
                var option = Echarts.monitor_line_options;
                option.title.text = chart_data.name;
                option.legend.data = chart_data.legend;
                option.xAxis.data = chart_data.x_axis;
                option.series = chart_data.series;
                var myChart = echarts.init(document.getElementById("" +chart_data.graphid));

                myChart.setOption(option);
            }else {
                var option = Echarts.pie_options;
                option.title.text = chart_data.name;
                option.legend.data = chart_data.legend;
                // console.log(option.seri)
                option.series[0].data = chart_data.series;
                var myChart = echarts.init(document.getElementById("" +chart_data.graphid));
                myChart.setOption(option);
            }

        };
    }]
}).directive('repeatFinish',["$timeout", function($timeout){
    return {
        link: function (scope, element, attr) {
            if (scope.$last == true) {
                $timeout(function () {
                    $.each(scope.$parent.$ctrl.graphs, scope.$parent.$ctrl.render_chart);
                });
            }
        }
    };
}]);