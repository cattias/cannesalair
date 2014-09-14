$(document).ready(function(){
	$("#divpassword").bind(
			"click",
			function(e) {
				$('#password_dialog').load(SITE_ROOT + 'account/profil/changepassword/');
				$('#password_dialog').dialog( {
					bgiframe : true,
			        modal : true,
			        autoOpen : false,
			        width : 600,
			        beforeclose: function(event, ui) {
						$('#password_dialog').html('');
					},
			        buttons : {
			            "Save" : function() {
							if ($('#id_pass1').val() == $('#id_pass2').val()) {
								$('#password_form').submit();
								$(this).dialog("close");
							} else {
								alert('Password don\'t match !');
							}
			            }
			        }
			    });
				$('#password_dialog').dialog('open');
				return true;
			});

});
