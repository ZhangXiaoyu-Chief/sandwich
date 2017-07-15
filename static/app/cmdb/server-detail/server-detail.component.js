/**
 * Created by zhangxiaoyu on 2017/6/21.
 */
angular.module('serverDetail').component('serverDetail', {
    templateUrl: '/static/app/cmdb/server-detail/server-detail.template.html',
    controller: ['$http', '$routeParams', 'Toastr', function ($http, $routeParams, Toastr) {
        var self = this;
        this.loading = false;
        $('.datepicker').datepicker({
            autoclose: true,
            format: 'yyyy-mm-dd',
            todayHighlight: true
        });
        this.labels = {
            '在线': "label-success",
            '已下线': "label-default",
            '未知': "label-warning",
            '故障': "label-danger",
            '备用': "label-info",
            '报废': "label-default"
        };
        this.form_data = {
            "base": {
                "asset_num": "",
                "status": "0"
            }
        };
        this.edit_form_display = {
            "base.asset_num": false
        };

        this.edit_field = function (field_name) {
            this.edit_form_display[field_name] = true;
            $("#cabinet").val(self.form_data.base.cabinet)
            $("#cabinet").select2({
                width: "100%", //设置下拉框的宽度
            });
            $("#business_unit").val(self.form_data.base.business_unit)
            $("#business_unit").select2({
                width: "100%", //设置下拉框的宽度
            });
            $("#admin").val(self.form_data.base.admin)
            $("#admin").select2({
                width: "100%", //设置下拉框的宽度
            });
            $("#operation").val(self.form_data.base.operation)
            $("#operation").select2({
                width: "100%", //设置下拉框的宽度
            });
            $("#tags").tagsinput();

        };
        this.edit_field_submit = function (field_name) {
            // self.loading = true;
            var keys = field_name.split(".")
            var postCfg = {
                headers: {'Content-Type': 'application/x-www-form-urlencoded'},
                transformRequest: function (data) {
                    return $.param(data);
                }
            };
            if(this.form_data[keys[0]][keys[1]]===this.server[keys[0]][keys[1]]){
                this.edit_form_display[field_name] = false;
                return;
            }
            var request_data = {
                "id": this.form_data.id,
                "filed_name": field_name,
                "new_value": this.form_data[keys[0]][keys[1]]
            };
            $http.post("/api/server/change/", request_data, postCfg)
                .then(function (response) {
                    self.get_data();
                    Toastr.messager["success"]("修改成功", "成功")
                });
            this.edit_form_display[field_name] = false;

        };
        this.cancel_edit = function (field_name) {
            this.edit_form_display[field_name] = false;
            self.form_data = angular.copy(self.server)
            $("#tags").val(self.form_data.base.tags);
            $('#tags').tagsinput('destroy');
        };
        this.get_data = function () {
            self.loading = true;
            $http.get('/api/server/detail/?id=' + $routeParams.assetId).then(function (response) {
                self.server = response.data.data;
                self.form_data = angular.copy(self.server)
                self.loading = false;

            }, function (response) {
                Toastr.handle(response, "查看服务器")
                self.loading = false;
            });
            $http.get('/api/cabinet/list/').then(function (response) {
                self.cabinet_select = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response, "获取机房");
                self.loading = false;

            });
            $http.get('/api/project/list/').then(function (response) {
                self.business_unit_select = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response, "获取项目");
                self.loading = false;
            });
            $http.get('/api/account/list/').then(function (response) {
                self.user_select = response.data.data;
                self.loading = false;
            }, function (response) {
                // 获取数据失败执行
                Toastr.handle(response, "获取项目");
                self.loading = false;
            });
        };
        this.get_data();
        this.statuses = [[0, '在线'], [1, '已下线'], [2, '未知'], [3, '故障'], [4, '备用'], [5, '报废']];
    }]
});