var show_num = 9,
    view_more = 9;

function viewMore() {
    var size_list = $(".news-content .news-div").length;
    $('.news-content .news-div:lt('+show_num+')').show();
    if(show_num >= size_list) {
        $(".btn-view-more").parent().hide();
    }
}
$(document).ready(function(){
    $(".news-div").css('display','none');

    viewMore();

    $(".btn-view-more").click(function() {
        show_num += view_more;
        viewMore();
    });    
});