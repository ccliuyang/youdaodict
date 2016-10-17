/**
 * Created with IntelliJ IDEA.
 * User: Kongtee
 * Date: 13-5-22
 * Time: 上午11:32
 * To change this template use File | Settings | File Templates.
 */
(function ($) {
    $(function () {
        $('.reload').bind('click', function () {
            top.postMessage('reload', '*');
        });
    });
})(jQuery);