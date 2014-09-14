$(document).ready(function(){
	$(".unselected").mouseover(
			function(e) {
				$(this).addClass("over");
				return true;
			});
	
	$(".unselected").mouseout(
			function(e) {
				$(this).removeClass("over");
				return true;
			});

	$("#arrow_message_nav").bind(
			"click",
			function(e) {
				$("#message_nav_inner_box").slideToggle("normal");
				$(this).toggleClass("arrowup");
				$(this).toggleClass("arrowdown");
				return true;
			});

	$("#arrow_article_nav").bind(
			"click",
			function(e) {
				$("#article_nav_inner_box").slideToggle("normal");
				$(this).toggleClass("arrowup");
				$(this).toggleClass("arrowdown");
				return true;
			});

	$("#arrow_participation_nav").bind(
			"click",
			function(e) {
				$("#participation_nav_inner_box").slideToggle("normal");
				$(this).toggleClass("arrowup");
				$(this).toggleClass("arrowdown");
				return true;
			});

	$("#arrow_sortie_nav").bind(
			"click",
			function(e) {
				$("#sortie_nav_inner_box").slideToggle("normal");
				$(this).toggleClass("arrowup");
				$(this).toggleClass("arrowdown");
				return true;
			});

	$("#arrow_gallery_nav").bind(
			"click",
			function(e) {
				$("#gallery_nav_inner_box").slideToggle("normal");
				$(this).toggleClass("arrowup");
				$(this).toggleClass("arrowdown");
				return true;
			});

	$("#arrow_comment_nav").bind(
			"click",
			function(e) {
				$("#comment_nav_inner_box").slideToggle("normal");
				$(this).toggleClass("arrowup");
				$(this).toggleClass("arrowdown");
				return true;
			});

});
