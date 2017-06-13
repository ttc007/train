$(document).ready(function () {
    function check_if_in_view() {
        var window_height = $(window).height();
        var window_top = $(window).scrollTop();
        var window_bottom_position = (window_top + window_height);

        $.each($('.animation-element'), function () {
            var $element = $(this);
            var element_height = $element.outerHeight();
            var element_top = $element.offset().top;
            var element_bottom = (element_top + element_height);
            var math_element = Math.ceil(($(window).height() * 0.30) * 2);
            if (window_top >= element_top - math_element && window_top < element_top + element_height - math_element) {
                $element.addClass('animated');
            } else {
                $element.removeClass('animated');
            }
        });
    }
    $(window).on('scroll resize', check_if_in_view);
    check_if_in_view();
});