$(document).ready(function(){
	$(".linktoexpandarticle").bind(
			"click",
			function(e) {
				$("#articlebody" + $(this).attr('id')).slideToggle("normal", 
				function() {
					var id = $(this).attr('id').substring(11);
					$("#arrow_article_" + id).toggleClass("arrowup");
					$("#arrow_article_" + id).toggleClass("arrowdown");
				});
				return true;
			});

	$(".linktodeletearticle").bind(
			"click",
			function(e) {
				if (confirm('Confirmer la suppression de cet article ?')) {
					window.location = SITE_ROOT + "article/" + $(this).attr('id') + "/delete/" ;
				}
				return true;
			});
});
