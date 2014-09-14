
function selection(image) {
	$(image).toggleClass("selected");
	$(image).toggleClass("unselected");
	manageselection(image);
}

function manageselection(image) {
	var hash = $(image).next("input:hidden").val();
	if ($(image).hasClass("selected")){
		var ul = document.querySelector("#choixphotosform>ul");
		var li = document.createElement("li");
		li.id = "hidden_" + hash;
		ul.appendChild(li);

		var input = document.createElement("input");
		input.type = "hidden";
		input.name = "imageid";
		input.value = hash;
		li.appendChild(input);
	} else {
		$("#hidden_"+hash).remove();
	}
}

function selection_full() {
	var images = document.querySelectorAll("img.unselected");
	for (i = 0; i < images.length; i++) {
		image = images[i];
		$(image).addClass("selected");
		$(image).removeClass("unselected");
		manageselection(image);
	}
}

function selection_empty() {
	var images = document.querySelectorAll("img.selected");
	for (i = 0; i < images.length; i++) {
		image = images[i];
		$(image).removeClass("selected");
		$(image).addClass("unselected");
		manageselection(image);
	}
}
