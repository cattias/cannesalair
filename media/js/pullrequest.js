$(document).ready(function(){
	$("#id_record_list_add").bind(
			"click",
			function(e) {
				var query = encodeURIComponent($('#id_record_list').val());
				if (query != '') {
					$('#id_record_list').attr("disabled", true);
					$('#indicator').css("display", "inline");
					$('#listrecord-result').load(
							SITE_ROOT + 'platinum/listrecords/?q=' + query, callback);
				}
				return true;
			});

	$("#id_record_list").bind("keypress", function(e) {
		var code = (e.keyCode ? e.keyCode : e.which);
		if (code == 13) {
			return false;
		}
	});
	
	function callback(responseText, textStatus, XMLHttpRequest) {
		  this; // dom element
		  $('#id_record_list').val('');
		  $('#id_record_list').removeAttr("disabled"); 
		  $('#indicator').css("display", "none");
    }
});
