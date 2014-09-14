$(document).ready(function(){
	$("#new_thread_link").bind(
			"click",
			function(e) {
				$('#new_thread_dialog').load(
						SITE_ROOT + 'forum/f/'+ $(this).attr('value') +'/add/');
				$('#new_thread_dialog').dialog( {
					bgiframe : true,
			        modal : true,
			        autoOpen : false,
			        width : 800,
			        beforeclose: function(event, ui) {
						$('#new_thread_dialog').html('');
					},
			        buttons : {
			            "Save" : function() {
							$('#newthreadform').submit();
			                $(this).dialog("close");
			            }
			        }
			    });
				$('#new_thread_dialog').dialog('open');
				return true;
			});

});
