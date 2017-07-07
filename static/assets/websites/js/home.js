function toggleIcon(e) {
    $(e.target)
        .prev('.game-section-title')
        .find(".more-less")
        .toggleClass('glyphicon glyphicon-plus glyphicon glyphicon-minus');
}

$(document).ready( function() {
    $(".carousel-inner .item:first").addClass("active");
    $(".home-carousel li:first").addClass("active");
    $(".home-carousel li:last").addClass("prev");
    $(".section-game .list-group a:first").addClass("active");
    $(".section-game .game-section-content:first").addClass("active");
    $(".game-section .game-section-content div.game-type-slide:first-child").addClass("active");
    $(".game-section div.game-right:first-child").addClass("active");
    $(".game-section .btn-custom-group li:first-child").addClass("active");
    

    
    /*menu hover*/
    $(".header .header-nav ul li ul li").hover(function(){
        $(this).parent().parent().addClass("active");
        }, function(){
        $(this).parent().parent().removeClass("active");
    });
    /*end menuhover*/

    $(".home-carousel li").each(function(index){
        $(this).attr('data-slide-to', index);
    });

    $('#myCarousel').carousel({
        interval:   4000
    });

    var vidieSlider = $('.vidieo-slider').flexslider({
        animation: "slide",
        start: function(slider){
            $(".vidieo-caption p").hide();
            $(".vidieo-caption p").eq(slider.currentSlide).show();
            $(".vidieo-list li").eq(slider.currentSlide).addClass('active');
        },
        after: function(slider){
            $(".vidieo-caption p").hide();
            $(".vidieo-caption p").eq(slider.currentSlide).show();
            $(".vidieo-list li.active").removeClass('active');
            $(".vidieo-list li").eq(slider.currentSlide).addClass('active');
        }
    });


    setInterval(function() {
        var current_active = $(".game-section .game-section-content.active div.game-type-slide.active");
        var div_img_active = $(".game-section .game-section-content.active div.game-right.active");
        var div_btn_active = $(".game-section .game-section-content.active .btn-custom-group li.active");
        current_active.removeClass("active");
        div_img_active.removeClass("active");
        div_btn_active.removeClass("active");
        if(current_active.next().next().index() == -1){
            $(".game-section .game-section-content.active div.game-type-slide:first-child").addClass("active");
            $(".game-section .game-section-content.active div.game-right:first-child").addClass("active");
            $(".game-section .game-section-content.active .btn-custom-group li:first-child").addClass("active");
        } else {
            current_active.next().addClass("active");
            div_img_active.next().addClass("active");
            div_btn_active.next().addClass("active");
        }
    }, 6000);

    $('#id_game_section').on('hidden.bs.collapse', toggleIcon);
    $('#id_game_section').on('shown.bs.collapse', toggleIcon);
    
    
    var clickEvent = false;
    $('#myCarousel').on('click', '.home-carousel a', function() {
            clickEvent = true;
            $('.home-carousel li').removeClass('active');
            $('.home-carousel li').removeClass('prev');
            $(this).parent().prev().addClass("prev");
            $(this).parent().addClass('active');
    }).on('slid.bs.carousel', function(e) {
        if(!clickEvent) {
            var count = $('.home-carousel').children().length -1;
            var current = $('.home-carousel li.active');
            current.removeClass('active').next().addClass('active');
            $('.home-carousel li').removeClass('prev');
            current.addClass("prev");
            var id = parseInt(current.data('slide-to'));
            if(count == id) {
                $('.home-carousel li').first().addClass('active');    
            }
        }
        clickEvent = false;
    }).on('click', '.left', function(e) {
            clickEvent = true;
            var current = $('.home-carousel li.active');
            current.removeClass('active').prev().addClass('active');
            $('.home-carousel li').removeClass('prev');
            $('.home-carousel li.active').prev().addClass('prev');
            var id = parseInt(current.data('slide-to'));
            if(id == 0) {
                $('.home-carousel li').last().addClass('active');    
            }
    });
    

    $("div.game-section-menu>div.list-group>a").click(function(e) {
        e.preventDefault();
        $(this).siblings('a.active').removeClass("active");
        $(this).addClass("active");
        var index = $(this).index();
        $("div.game-section>div.game-section-content").removeClass("active");
        $("div.game-section>div.game-section-content").eq(index).addClass("active");
    });
    $("#vidieo_play_modal").on("shown.bs.modal", function () {
        $('#helio_vidieo').attr('src', $(".vidieo-list li.active div").text()); //$('#helio_vidieo').attr('src')
    });
    $("#vidieo_play_modal").on("hidden.bs.modal", function () {
        $('#helio_vidieo').attr('src', ''); //$('#helio_vidieo').attr('src')
    });

    $(".list-line li").each(function(index){
        $(this).click(function () {
        vidieSlider.flexslider(index);
        vidieSlider.data('flexslider').play();
        });
    });

});