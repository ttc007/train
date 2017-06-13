$(document).ready(function() {
	$('.user_choose').multiSelect({
		selectableHeader: "<div class='ms-header'><label>User</label></div>",
		selectionHeader: "<div class='ms-header'><label>Selected</label></div>"
	});

	$("#save-btn").click(function() {
    	var param = {
            promotion_id: $("#promotion_id").val(), 
            list_user: $('.user_choose').val()
        }
    	$.ajax({
			type: 'POST',
			url: '/vi/update-promotions-user/',
			dataType: 'json',
			data: param,
			success: function (data) {
				$("#message_success").fadeIn('slow').delay(5000).fadeOut('slow');
			},
	        error : function(jqXHR, textStatus, errorThrown) {
	            alert("Error: " + textStatus + ": " + errorThrown);
	        }
  		});
    });
});