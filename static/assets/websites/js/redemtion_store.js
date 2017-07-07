var show_num =5,
    view_more = 5;

function viewMore() {
    var size_list = $(".faqs-section .faq-detail").length;
    $('.faqs-section .faq-detail:lt('+show_num+')').show();
    if(show_num >= size_list) {
        $(".btn-view-more").parent().parent().hide();
    }
}

$(document).ready(function(){
    $(".faq-detail").css('display','none');

    viewMore();

    $(".btn-view-more").click(function() {
        show_num += view_more;
        viewMore();
    });

    function toggleIcon(e) {
        $(e.target)
            .prev('.panel-heading')
            .find(".more-less")
            .toggleClass('fa-chevron-circle-down fa-chevron-circle-up');
    }
    $('.panel-group').on('hidden.bs.collapse', toggleIcon);
    $('.panel-group').on('shown.bs.collapse', toggleIcon);
    $( ".card-description" ).each(function(  ) {
        if ( $(this ).height() > 200 ) {
            $( this ).addClass("height-limit")
            $( this ).parent().parent().find(".card-div-bottom").removeClass("hidden");
        }
    });
    $(".view-full").click(function(){
        var powercard_content = $(this).parent().parent().find(".card-description");
        if($(powercard_content).hasClass("height-limit")) {
            $(powercard_content).removeClass("height-limit");
            $(this).html('THU GỌN <br> <i class="glyphicon glyphicon-chevron-up">');
        } else {
            $(powercard_content).addClass("height-limit");
            $(this).html('XEM ĐẦY ĐỦ <br> <i class="glyphicon glyphicon-chevron-down">');
        }
    });    
});

var RedemtionFunction = (function ($) {
    var redemtion_store = function () {
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
    return redemtion_store;
})(jQuery);

(function (redemtion_store, $) {
    $(document).ready(function(){
        redemtion_store.initEventPage();
    });
})(new RedemtionFunction(), jQuery);