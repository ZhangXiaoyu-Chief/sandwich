/**
 * Created by zhangxiaoyu on 2017/6/15.
 */
angular.
  module('toastr').
    factory('Toastr', function () {
        var mytoastr = toastr;
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
        return mytoastr;
})
