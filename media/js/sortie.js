/* French initialisation for the jQuery UI date picker plugin. */
/* Written by Keith Wood (kbwood{at}iinet.com.au) and Stéphane Nahmani (sholby@sholby.net). */
//jQuery(function($){
//	$.datepicker.regional['fr'] = {
//		closeText: 'Fermer',
//		prevText: '&#x3c;Pr&eacute;c',
//		nextText: 'Suiv&#x3e;',
//		currentText: 'Courant',
//		monthNames: ['Janvier','F&eacute;vrier','Mars','Avril','Mai','Juin',
//		'Juillet','Aout','Septembre','Octobre','Novembre','D&eacute;cembre'],
//		monthNamesShort: ['Jan','F&eacute;v','Mar','Avr','Mai','Jun',
//		'Jul','Aou','Sep','Oct','Nov','D&eacute;c'],
//		dayNames: ['Dimanche','Lundi','Mardi','Mercredi','Jeudi','Vendredi','Samedi'],
//		dayNamesShort: ['Dim','Lun','Mar','Mer','Jeu','Ven','Sam'],
//		dayNamesMin: ['Di','Lu','Ma','Me','Je','Ve','Sa'],
//		weekHeader: 'Sm',
//		dateFormat: 'dd/mm/yy',
//		firstDay: 1,
//		isRTL: false,
//		showMonthAfterYear: false,
//		yearSuffix: ''};
//	$.datepicker.setDefaults($.datepicker.regional['fr']);
//});

$(document).ready(function(){

	$(".linktoexpandsortie").bind(
			"click",
			function(e) {
				$("#sortiebody" + $(this).attr('id')).slideToggle("normal", 
				function() {
					var id = $(this).attr('id').substring(10);
					$("#arrow_sortie_" + id).toggleClass("arrowup");
					$("#arrow_sortie_" + id).toggleClass("arrowdown");
				});
				return true;
			});
	
	$(".linktodeletesortie").bind(
			"click",
			function(e) {
				if (confirm('Confirmer la suppression de cette sortie ?')) {
					window.location = SITE_ROOT + "sortie/" + $(this).attr('id') + "/delete/" ;
				}
				return true;
			});

	$(".linktocr").bind(
			"click",
			function(e) {
				$('#id_cr_' + $(this).attr('id')).toggle();
				return true;
			});

	$("#previewbtn").bind(
			"click",
			function(e) {
				var $currentIFrame = $('#id_description_ifr');
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

	$("#previewbtncr").bind(
			"click",
			function(e) {
				var $currentIFrame = $('#id_compterendu_ifr');
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

//	$("#datepicker_id_date_debut").datepicker({
//		dateFormat: "yy-mm-dd",
//		onSelect: 
//		function(dateText, inst) {
//			$("#id_date_debut").val(dateText)
//			}
//	});
//	$("#datepicker_id_date_debut").datepicker($.datepicker.regional['fr']);
//	$("#datepicker_id_date_debut").datepicker('setDate', $.datepicker.parseDate( "yy-mm-dd", $("#id_date_debut").val() ) );
//
//	$("#datepicker_id_date_fin").datepicker({
//		dateFormat: "yy-mm-dd",
//		onSelect: 
//		function(dateText, inst) {
//			$("#id_date_fin").val(dateText)
//			}
//	});
//	$("#datepicker_id_date_fin").datepicker($.datepicker.regional['fr']);
//	$("#datepicker_id_date_fin").datepicker('setDate', $.datepicker.parseDate( "yy-mm-dd", $("#id_date_fin").val() ) );
});
