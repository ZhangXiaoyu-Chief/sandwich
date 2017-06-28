/**
 * Created by zhangxiaoyu on 2017/6/15.
 */
angular.
  module('toastr').
    factory('Toastr', function () {
        var mytoastr = toastr;
        var self = this
        mytoastr.options = {
          "closeButton": true,
          "debug": false,
          "positionClass": "toast-bottom-right",
          "onclick": null,
          "showDuration": "1000",
          "hideDuration": "1000",
          "timeOut": "3000",
          "extendedTimeOut": "1000",
          "showEasing": "swing",
          "hideEasing": "linear",
          "showMethod": "fadeIn",
          "hideMethod": "fadeOut"
        };
        var message_handle = function (response, action) {
            mytoastr.options = {
                      "closeButton": true,
                      "debug": false,
                      "positionClass": "toast-bottom-right",
                      "onclick": null,
                      "showDuration": "1000",
                      "hideDuration": "1000",
                      "timeOut": "3000",
                      "extendedTimeOut": "1000",
                      "showEasing": "swing",
                      "hideEasing": "linear",
                      "showMethod": "fadeIn",
                      "hideMethod": "fadeOut"
                    };
            if (response.status === 401) {
                window.location.href = response.data.data.login_url
            }
            if(response.status === 403){
                mytoastr["error"]("对不起，您没有执行此操作的权限", "权限错误");
            }
            if(response.status === 416){
                mytoastr["error"](action + "失败，违反某些字段的唯一性约束", "错误");
            }
            if(response.status === 404){
                mytoastr["error"](action + "失败，要操作的对象不存在或已经删除", "错误");
            }
            if(response.status === 500){
                mytoastr["error"](action + "失败", "未知错误");
            }
        };
        return {
            messager: mytoastr,
            handle: message_handle
        };
});
