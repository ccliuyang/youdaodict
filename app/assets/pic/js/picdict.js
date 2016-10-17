/**
 * Created with IntelliJ IDEA.
 * User: youdao
 * Date: 13-5-16
 * Time: 上午10:09
 * To change this template use File | Settings | File Templates.
 */
(function ($) {
    var app = DAE.app;
    var $iframe = $('iframe'),
        $img = $('img');

    /**
     * 绑定事件
     */
    var bindEvent = function () {
        /**
         * 词典到图解的查词
         * @param data
         */
        // external.cppCall('setCmdFun', function (data) {
        //     if (Array.isArray(data) && data.length > 0) {
        //         var param = $.parseJSON(data[data.length - 1]);
        //         if (param.id && param.word) {
        //             var src = $iframe.attr('src');
        //             src = src.substring(0, src.lastIndexOf('/'));
        //             $iframe.attr('src', src + '/index.html?id=' + param.id + '&word=' + param.word);
        //         }
        //     }
        // });
        /**
         * 判断是否能访问服务器
         */
        $img.bind('error', function () {
            $iframe.attr('src', 'offline.html');
        });
        /**
         * 用户反馈
         */
        $('#cpp_feedback').bind('click', function () {
            var appid, appver, appVendor, indexCase, abtest;
            try {
                appid = youdao_api.getAppID();
            } catch (e) {
                appid = '';
            }
            try {
                appver = youdao_api.getAppVersionString();
            } catch (e) {
                appver = '';
            }
            try {
                appVendor = youdao_api.getVendor();
            } catch (e) {
                appVendor = '';
            }
            try {
                indexCase = $.parseJSON(window.external.cppCall("loadString", "indexTestCase"));
            } catch (e) {
                indexCase = '';
            }

            try {
                abtest = indexCase.testCase;
            } catch (e) {
                abtest = '';
            }
			abtest = abtest || '';

            var href = 'http://cidian.youdao.com/feedback.jsp?keyfrom=deskdict.picdict&appVer=' + appver +
                '&id=' + appid + '&vendor=' + appVendor + '&abTest=' + abtest;
            DAE.browse(href);
        });
        /**
         * 最小化
         */
        $('#cpp_min').click(function () {
            app.minimize();
        });
        /**
         * 关闭
         */
        $('#cpp_close').click(function () {
            app.hide();
        });
        /**
         * 窗口可用元素不能移动窗口
         */
        $('.brand, .pull-right').on('mousedown', function (e) {
            e.stopPropagation();
        });
        /**
         * 移动窗口
         */
        $('header').bind({
            mousedown: function(event){
                if(event.which == 1 && ! $(event.target).is('button')){
                    app.dragStart();
                }
            },
            mouseup: function(event){
                if(event.which == 1){
                    app.dragStop();
                }
            }
        });
        /**
         * 接收iframe传来消息
         * @param e
         */
        window.onmessage = function (event) {
            if (event.data === 'offline') {
                $iframe.attr('src', 'offline.html');
            } else if (event.data === 'reload') {
                $iframe.attr('src', 'http://dict.youdao.com/picdict/');
            }
        };
    };

    $(function () {
        bindEvent();
    });
})(jQuery);