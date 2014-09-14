$(document).ready(function(){
	
    $('.chat_user').mouseover(
			function(e) {
				$(this).addClass("over");
				return true;
			});

    $('.chat_user').mouseout(
			function(e) {
				$(this).removeClass("over");
				return true;
			});

    $('.chat_user').bind(
    		"click",
			function(e) {
				alert('Chat coming soon !');
				return true;
			});

    $('.chat_user_off').mouseover(
			function(e) {
				$(this).addClass("over");
				return true;
			});

    $('.chat_user_off').mouseout(
			function(e) {
				$(this).removeClass("over");
				return true;
			});

    $('.chat_user_off').bind(
    		"click",
			function(e) {
				window.location = SITE_ROOT+"account/profil/"+$(this).attr('id')+"/view/";
				return true;
			});

});
