var PlayFunction = (function ($) {
    var helio_play = function () {
        var _self = this;
        var show_num = 4,
            view_more = 4;

        this.initEventPage = function () {
            var url = window.location.href;
            var section_active = url.substring(url.lastIndexOf('/') + 2);
            $(".tab-content .tab-pane.view-more-content").each(function(){
                var id = $(this).attr("id");
                if($(this).hasClass(section_active)) {
                    $(".play-btn-group li").removeClass("active");
                    $(".tab-content .tab-pane").removeClass("active");
                    $(".tab-content ." + section_active).addClass("active");
                    $(".play-btn-group ."+ section_active).parent().addClass("active");
                }

                _self.viewMore();
            });
            $(".btn-view-more").click(function() {
                show_num += view_more;
                _self.viewMore();
            });
            $(".tab-content .tab-pane.view-more-content").each(function(){
                _self.initCoursel($(this).find('.carousel'));
            });
            $( window ).resize(function() {
                $(".tab-content .tab-pane.view-more-content").each(function(){
                    _self.initCoursel($(this).find('.carousel'));
                });
            });
        }
        this.initCoursel = function (element) {
            $(element).html($(element).parent().find('.carousel-tmp').html());
            var content_width = $(".container").width(),
                w = content_width * 0.675,
                h = w / 1.8,
                h_carousel = h + 200,
                h_bw = h/2 - 20;
            $(element).carousel({
                carouselWidth: content_width,
                carouselHeight: h_carousel,
                directionNav:true,    
                shadow:false, 
                frontWidth:w,
                frontHeight:h,
                hMargin: 0.3,
                vMargin: 0.8,
                short_description: true,
                mouse:false
            });
            $(element).find(".prevButton").css('top', h_bw + 'px');
            $(element).find(".nextButton").css('top', h_bw + 'px');
        }
        this.viewMore = function (element) {
            var size_list = $("#promotion_content .item-line").length;
            $('#promotion_content .item-line:lt('+show_num+')').show();
            if(show_num >= size_list) {
                $(".btn-view-more").hide();
            }
        }
    }
    return helio_play;
})(jQuery);

(function (play, $) {
    $(document).ready(function(){
        play.initEventPage();
    });
})(new PlayFunction(), jQuery);