$(document).ready(function(){
	$(".linktocomment").bind(
			"click",
			function(e) {
				var id = $(this).attr('id');
				var type = $(this).attr('type');
				var comment = '#comment_'+type+'_'+id;
				$(comment).toggle();
				return true;
			});

	$(".linktodeletecomment").bind(
			"click",
			function(e) {
				if (confirm('Confirmer la suppression de ce commentaire ?')) {
					window.location = SITE_ROOT + "comment/" + $(this).attr('id') + "/delete/" ;
				}
				return true;
			});
});
