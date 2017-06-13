var KidsFunction = (function ($) {
    var helio_kids = function () {
        var _self = this;
        var show_num = {};
        var first_show = 5,
            view_more = 5;

        this.initEventPage = function () {
            $(".tab-content .tab-pane.view-more-content").each(function(){
                var id = $(this).attr("id");
                show_num[id] = first_show;
                _self.viewMore($(this));
            });
            $(".btn-view-more").click(function() {
                var element_content = $(this).parent().closest(".view-more-content");
                var id = $(element_content).attr("id");
                show_num[id] += view_more;
                _self.viewMore(element_content);
            });     
        }
        this.viewMore = function (element) {
            var id = $(element).attr("id");
            var size_list = $(element).find(".item-line").length;
            var show_lengh =  show_num[id];
            $(element).find('.item-line:lt('+show_lengh+')').show();
            if(show_lengh >= size_list) {
                $(element).find(".btn-view-more").hide();
            }
            show_num[id] = show_lengh;
        }
    }
    return helio_kids;
})(jQuery);

(function (kids, $) {
    $(document).ready(function(){
        kids.initEventPage();
    });
})(new KidsFunction(), jQuery);