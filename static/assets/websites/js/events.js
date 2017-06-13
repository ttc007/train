var EventsFunction = (function ($) {
    var helio_events = function () {
        var _self = this;
        var show_num = 4,
            view_more = 4;
        this.initElementPage = function() {
            _self.eventsCoursel();

            $(".event-class").each(function() {
                _self.event_function($(this));
            });

            $(".event-class.future-class .countdown").each(function(){
                var start_time = $(this).find(".start_datetime").text();
                $(this).countdown(start_time, function(event) {
                    $(this).find(".days").find(".current").text(event.strftime('%D'));
                    $(this).find(".hours").find(".current").text(event.strftime('%H'));
                    $(this).find(".minutes").find(".current").text(event.strftime('%M'));
                    $(this).find(".seconds").find(".current").text(event.strftime('%S'));
                });
            });
        }

        this.initEventPage = function () {
            _self.viewMore();

            $(".btn-view-more").click(function() {
                show_num += view_more;
                _self.viewMore();
            });     
        }
        this.viewMore = function () {
            var size_list = $("#events_content .item-line").length;
            $('#events_content .item-line:lt('+show_num+')').show();
            if(show_num >= size_list) {
                $(".btn-view-more").hide();
            }
        }
        this.eventsCoursel = function() {
            /*current Month display slide*/
            var current_date = new Date($.now());
            var m = current_date.getMonth() + 1, 
                is_active = false;
                m = m > 9 ? m : "0" + m;
            var m_y_current = current_date.getFullYear() + "_" + m;

            $(".event-month").each(function() {
                if($(this).attr('value') >=  m_y_current) {
                    $(this).addClass("active");
                    $(".events-list-by-month").eq($(this).index()).addClass("active");
                    is_active = true;
                    return false;
                }
            });
            if(is_active == false) {
                $(".event-month:last").addClass("active");
                $(".events-list-by-month:last").addClass("active");
            }
            /*end current Month display slide*/

            $('.events-list-by-month').each(function() {
                $(this).find(".event-item:last").addClass("active");
            });

            $('.month-carousel').carousel({
                interval: false
            });
            _self.flexCoursel('.events-list-by-month.active .flexslider');
            $('.month-carousel').on('slide.bs.carousel', function (e) {
                if($(e.relatedTarget).attr('class') === 'item events-list-by-month') {
                    var indexFrom = $('.month-carousel>.carousel-inner>.item.active').index();
                    var indexTo = $(e.relatedTarget).index();
                    $('.event-month').eq(indexFrom).hide();
                    $('.event-month').eq(indexTo).show();

                    _self.flexCoursel($(e.relatedTarget).find('.flexslider'));
                }
            });
        }
        this.flexCoursel = function(element) {
            if(!$(element).hasClass("complete")) {
                var items_length = $(element).find('.item-flex').length;
                var max_items = 7;
                if(items_length < 7)  {
                    max_items = items_length;
                }

                $(element).flexslider({
                    animation: "slide",
                    animationSpeed: 400,
                    animationLoop: false,
                    itemWidth: 160,
                    itemMargin: 3,
                    minItems: 2,
                    maxItems: max_items,
                    start: function(slider){
                        if (slider.last === 0) {
                            slider.directionNav.addClass("flex-disabled");
                        }
                    }
                });
                $(element).addClass("complete");
            }
        }

        this.event_function = function(event_class) {
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
    }
    return helio_events;
})(jQuery);

(function (events, $) {
    $(document).ready(function(){
        events.initElementPage()
        events.initEventPage();
    });
})(new EventsFunction(), jQuery);