var show_num = {},
    first_show = 5,
    view_more = 5;

function viewMore (element) {
    var id = $(element).attr("id");
    var size_list = $(element).find(".faq-detail").length;
    var show_lengh =  show_num[id];
    $(element).find('.faq-detail:lt('+show_lengh+')').show();
    if(show_lengh >= size_list) {
        $(element).find(".btn-view-more").hide();
    }
    show_num[id] = show_lengh;
}
function toggleIcon(e) {
    $(e.target)
        .prev('.panel-heading')
        .find(".more-less")
        .toggleClass('fa-chevron-circle-down fa-chevron-circle-up');
}
$(document).ready(function(){
    $(".faq-detail").css('display','none');

    $(".faqs_category:first").addClass('active');
    $(".faqs-content:first").addClass('active');

    $(".tab-content .tab-pane.view-more-content").each(function(){
        var id = $(this).attr("id");
        show_num[id] = first_show;
        viewMore($(this));
    });

    $(".btn-view-more").click(function() {
        var element_content = $(this).parent().closest('.view-more-content');
        var size_list = $(element_content).find(".item-line").length;
        var id = $(element_content).attr("id");
        show_num[id] += view_more;
        viewMore(element_content);
    });

    $('.panel-group').on('hidden.bs.collapse', toggleIcon);
    $('.panel-group').on('shown.bs.collapse', toggleIcon);
});