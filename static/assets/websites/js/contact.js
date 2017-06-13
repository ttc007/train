var en_message = {
	"err_name_required": "Please input your name",
	"err_email_required": "Please input your email",
	"err_email_format": "Please input correct format email",
	"err_phone_required": "Please input your phone number",
	"err_phone_maxlength": "The phone number you just inputed is unreal",
	" err_phone_format": "Please input correct format phone number",
	"err_subject_required": "Please input the subject"
}
var vi_message = {
	"err_name_required": "Vui lòng nhập tên",
	"err_email_required": "Vui lòng nhập email",
	"err_email_format": "Vui lòng nhập đúng định dạng email",
	"err_phone_required": "Vui lòng nhập số điện thoại",
	"err_phone_maxlength": "Số máy quý khách vừa nhập là số không có thực",
	" err_phone_format": "Vui lòng nhập đúng định dạng số điện thoại",
	"err_subject_required": "Vui lòng nhập chủ đề"	
}


$(document).ready(function() {
	var contact_message= {}
	if(lang_code == "en") {
		contact_message = en_message;
	} else {
		contact_message = vi_message;
	}
	
	$("#form_contact").validate({
		rules: {
			name: "required",

			email: {
				required: true,
				email: true
			},
			phone: {
				required: true,
				maxlength: 11,
				number: true
			},
			subject: "required"
		},

		messages: {
			name: contact_message["err_name_required"],
			email: {
				required: contact_message["err_email_required"],
				email: contact_message["err_email_format"]
			},
			phone: {
				required: contact_message["err_phone_required"],
				maxlength: contact_message["err_phone_maxlength"],
				number: contact_message["err_phone_format"]
			},
			subject: contact_message["err_subject_required"]
		}
	});
	$(document).on("click","#submitbutton",function() {
	    if($('#form_contact').valid()) {
			var frm = $('#form_contact');
		    $.ajax({
		        type: frm.attr('method'),
		        url: frm.attr('action'),
		        dataType: 'json',
		        data: frm.serialize(),
		        success: function (data) {
		        	$("input").val("");
		            $("textarea").val("");
		            $("#message_success").css('display','block');
		            $("#message_error").css('display','none');
		        },
		        error: function(data) {
		        	var form_err = $.parseJSON(data.responseText);
		        	$("#errors_detail").text(JSON.stringify(form_err));
		            $("#message_error").css('display','block');
		            
		        }
		    });
		}
		else {
			$("#message_success").css('display','none');
		}
	});
});

