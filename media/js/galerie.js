var COUNTER = 0;
var TOTALCOUNTER = 0;

function get_upload_progress(image) {
	return function(e) {
		// console.log("progress for " + aCanvas.id + " START !!");
		if (e.lengthComputable) {
			var percentage = Math.round((e.loaded * 100) / e.total);
			// console.log("progress for "+ aCanvas.id + "=" +
			// percentage.toString());
			$("#progress_" + image.id).html(percentage.toString() + "%");
		} else {
			// console.log("no progress for " + aCanvas.id);
		}
	};
}

function get_upload_complete(image) {
	return function(e) {
		// console.log(aCanvas.id + " DONE !!");
		$("#progress_" + image.id).html("DONE");
		COUNTER++;
		if (COUNTER == TOTALCOUNTER) {
			window.location.reload();
		}
	};
}

function uploadphotos(album) {
	// console.log("Upload for album " + album);
	var images = document.querySelectorAll("img.hiddenstuff");
	COUNTER = 0;
	TOTALCOUNTER = images.length;
	// console.log("Total upload photos=" + TOTALCOUNTER);
	for (i = 0; i < images.length; i++) {
		image = images[i];
		var xhr = new XMLHttpRequest();
		xhr.upload.addEventListener("progress", get_upload_progress(image),
				false);
		xhr.addEventListener("load", get_upload_complete(image), false);
		xhr.open("POST", SITE_ROOT + "galerie/upload/");

		var fd = new FormData();
		fd.append("album", album);
		fd.append("ordre", $("#inputordre_" + image.id).val());
		fd.append("filename", image.file.name);
		fd.append("image", image.src);
		xhr.send(fd);
	}
	if (COUNTER == TOTALCOUNTER) {
		window.location.reload();
	}
}

function finishthumbnail() {
	hideLoading();
	$("#thumbnaillistul").sortable({
		distance : 10,
		revert : true,
		stop : function(event, ui) {
			var offset = parseInt($("#totalphotosnumber").val());
			$(this).find("li").each(function() {
				index = offset + parseInt($(this).index() + 1);
				$(this).find("input:hidden").val(index);
			});
		}
	});
}

$(document).ready(function() {
	var dropzone = document.getElementById("dropzone");
	dropzone.addEventListener("dragexit", function(event) {
		$("#dropzone").removeClass("dropzonegreen");
		event.preventDefault();
	}, true);
	dropzone.addEventListener("dragleave", function(event) {
		$("#dropzone").removeClass("dropzonegreen");
		event.preventDefault();
	}, true);
	dropzone.addEventListener("dragover", function(event) {
		$("#dropzone").addClass("dropzonegreen");
		event.preventDefault();
	}, true);
	dropzone.addEventListener("drop", function(event) {
		event.preventDefault();
		$("#dropzone").removeClass("dropzonegreen");
		showModalLoading();
		// Ready to do something with the dropped object
		var allTheFiles = event.dataTransfer.files;
		var ul = document.querySelector("#bag>ul");
		COUNTER = 0;
		TOTALCOUNTER = allTheFiles.length;
		if (TOTALCOUNTER > 20) {
			hideLoading();
			alert("20 photos maximum en meme temps, sinon tu vas tout casser :)");
		} else {
			var offset = parseInt($("#totalphotosnumber").val());
			for ( var i = 0; i < allTheFiles.length; i++) {
				var file = allTheFiles[i];
				if (file.type.match(/image.*/) && file.size <= 10000000) {
					var theID = "the_id_"+i;
					var li = document.createElement("li");
					ul.appendChild(li);

					var canvas = document.createElement("canvas");
					canvas.width = 90;
					canvas.height = 90;
					li.appendChild(canvas);

					var inputordre = document.createElement("input");
					inputordre.type = "hidden";
					inputordre.id = "inputordre_" + theID;
					inputordre.name = "ordre";
					inputordre.value = offset + i + 1;
					li.appendChild(inputordre);

					var progress = document.createElement("div");
					progress.id = "progress_" + theID;
					progress.className = "progressbar";
					progress.innerHTML = file.name;
					li.appendChild(progress);

					var img = document.createElement("img");
					img.classList.add("obj");
					img.file = file;
					img.id = theID;
					img.className = "hiddenstuff";
					img.onload = (function(aImg, aCanvas, aLi) {
						return function(e) {
							aLi.appendChild(aImg);
							var ctx = aCanvas.getContext("2d");
							ctx.drawImage(aImg, 0, 0, 90, 90);
							COUNTER++;
							if (COUNTER == TOTALCOUNTER) {
								finishthumbnail();
							}
						};
					})(img, canvas, li);
					var reader = new FileReader();
					reader.onload = (function(aImg) {
						return function(e) {
							aImg.src = e.target.result
						};
					})(img);
					reader.readAsDataURL(file);
				} else {
					COUNTER++;
					if (COUNTER == TOTALCOUNTER) {
						finishthumbnail();
					}
				} // end if
			} // end for
			if (COUNTER == TOTALCOUNTER) {
				finishthumbnail();
			}
		}
	}, true);
});
