var CoffeeFunction = (function ($) {
    var coffee = function () {
        var _self = this;
        var show_num = 4,
            view_more = 4;

        this.initEventPage = function () {
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
                // h_carousel = h + 200,
                h_bw = h/2 - 20;
            $(element).carousel({
                carouselWidth: content_width,
                carouselHeight: h,
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
    }
    return coffee;
})(jQuery);

(function (coffee, $) {
    $(document).ready(function(){
        coffee.initEventPage();
    });
})(new CoffeeFunction(), jQuery);