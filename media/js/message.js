$(document).ready(function(){
	$("#previewbtn").bind(
			"click",
			function(e) {
				var $currentIFrame = $('#id_contenu_ifr');
				var content = $currentIFrame.contents().find('body').html();
				$('#post_preview').html(content);
				$('#post_preview').dialog( {
					bgiframe : true,
					width : 800,
			        modal : true,
			        autoOpen : false,
			        beforeclose: function(event, ui) {
						$('#post_preview').html('');
					}
			      });
				$('#post_preview').dialog('open');
				return true;
			});

});
