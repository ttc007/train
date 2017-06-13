function event_function(event_class) {
    var start_time_txt = $(event_class).find(".start_datetime").text(),
        end_time_txt = $(event_class).find(".end_datetime").text(),
        start_datetime = new Date(start_time_txt),
        end_datetime = new Date(end_time_txt),
        current_date = new Date($.now());

    var event_label = "";

    if(current_date > end_datetime) {
        event_label = "finished";
    } else if (current_date < start_datetime) {
        event_label = "future";
    } else {
        event_label = "current";
    }

    $(event_class).find("."+event_label+"-event").show();
    $(event_class).addClass(event_label+ "-class");
}
$(document).ready(function(){
	var start_time_txt = $(".event-class").find(".start_datetime").text();


	event_function(".event-class");

    $('.event-class.future-class .countdown').countdown(start_time_txt, function(event) {
        $(this).find(".days").find(".current").text(event.strftime('%D'));
        $(this).find(".hours").find(".current").text(event.strftime('%H'));
        $(this).find(".minutes").find(".current").text(event.strftime('%M'));
        $(this).find(".seconds").find(".current").text(event.strftime('%S'));
    });
});