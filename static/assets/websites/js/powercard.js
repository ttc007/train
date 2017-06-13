var show_num = 5,
    view_more = 5;
var en_button = {
	'show_more' : 'SHOW MORE',
	'show_less' : 'SHOW LESS'
}
var vi_button = {
	'show_more' : 'XEM ĐẦY ĐỦ',
	'show_less' : 'THU GỌN'
}
// var show_more_vi = 'XEM ĐẦY ĐỦ',
// 	show_more_en = 'SHOW MORE';
// var show_less_vi = 'THU GỌN',
// 	show_less_en = 'SHOW LESS';


function viewMore() {
    var size_list = $(".faqs-section .faq-detail").length;
    $('.faqs-section .faq-detail:lt('+show_num+')').show();
    if(show_num >= size_list) {
        $(".btn-view-more").hide();
    }
}

$(document).ready( function() {
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
	// var show_more,
	// 	show_less;
	var btn_view_more={}
	if(lang_code == "en") {
		btn_view_more = en_button;
	} else {
		btn_view_more = vi_button;
	}
	$(".view-full").click(function(){
		var powercard_content = $(this).parent().parent().find(".card-description");
		if($(powercard_content).hasClass("height-limit")) {
			$(powercard_content).removeClass("height-limit");
			$(this).html(btn_view_more["show_less"] + '<br> <i class="glyphicon glyphicon-chevron-up">');
		} else {
			$(powercard_content).addClass("height-limit");
			$(this).html(btn_view_more["show_more"] + '<br> <i class="glyphicon glyphicon-chevron-down">');
		}
	});
});