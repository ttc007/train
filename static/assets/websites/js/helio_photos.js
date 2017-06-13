var show_num = 8,
    view_more = 3;

function viewMore() {
    var size_list = $(".photos-section .box").length;
    $('.photos-section .box:lt('+show_num+')').show();

    if(show_num >= size_list) {
        $(".box-view-more").hide();
    }
}
$(document).ready(function(){
    $(".box").css('display','none');

    viewMore();
    $(".box-view-more").click(function() {
        show_num += view_more;
        viewMore();
    });   
    $(".view-images-btn").click(function() {
        var param = {
            album_id: $(this).attr("id")
        }
        $.ajax({
            type: 'POST',
            url: '/vi/list-photos-by-album/',
            dataType: 'json',
            data: param,
            success: function (data) {
                $("#slider .slides").html("");
                $("#carousel .slides").html("");
                $(".modal-body").html('<div id="slider" class="flexslider"> <ul class="slides"></ul></div>' 
                                        + '<div id="carousel" class="flexslider"> <ul class="slides"></ul></div>')
                
                if(data && data.length > 0 ) {
                    for (var i = data.length - 1; i >= 0; i--) {
                        $("#slider .slides").append("<li> <img src='"+ MEDIA_URL + data[i].image +"'/></li>");
                        $("#carousel .slides").append("<li><img src='"+ MEDIA_URL + data[i].image +"'/></li>");
                        
                    }
                    $('#images_modal').modal('show');
                } else {
                    alert("No image in album");
                }
                
            },
            error: function(error) {
                alert("Internal Error");
            }
        });
    });


    $('#images_modal').on('shown.bs.modal', function() {
        $('#carousel').flexslider({
            animation: "slide",
            controlNav: false,
            animationLoop: false,
            slideshow: false,
            itemWidth: 170,
            itemMargin: 0,
            minItems: 2,
            maxItems: 4,
            asNavFor: '#slider'
        });

        $('#slider').flexslider({
            animation: "slide",
            controlNav: false,
            animationLoop: false,
            slideshow: false,
            sync: "#carousel",
            start: function(slider){
                $(".cur-slide").text(slider.currentSlide+1);
                $(".total-slide").text(slider.count);
            },
            after: function(slider){
                $(".cur-slide").text(slider.currentSlide+1);
            }
        });
    });

    $(".box").hover(
        function() {
            $(this).find(".view-all").show();
        }, function() {
            $(this).find(".view-all").hide();
        }
    );
});