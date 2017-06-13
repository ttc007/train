var show_num = 9,
    view_more = 9;

function viewMore() {
    var size_list = $(".experiences-content .experiences-div").length;
    $('.experiences-content .experiences-div:lt('+show_num+')').show();
    if(show_num >= size_list) {
        $(".btn-view-more").parent().hide();
    }
}
$(document).ready(function(){
    $(".experiences-div").css('display','none');

    viewMore();

    $(".btn-view-more").click(function() {
        show_num += view_more;
        viewMore();
    });    
});