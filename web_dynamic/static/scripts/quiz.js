#!/usr/bin/node
// Properties of the Quiz page
$(function () {
	Swal.fire({
		title: "Hurray! 🤩",
		icon: "info",
		text: "Scroll down the left panel and start quiz",
		timer: 3000,
		timerProgressBar: true,
		showConfirmButton: false,
		allowOutsideClick: false
	});
	setTimeout(() => {}, 3000);

	function setCurrent() {
		// alert(`${obj.attr('id')} is in view`);
		var oldLink = document.getElementsByClassName('current')[0];
		if (oldLink) {
			oldLink.classList.remove('current');
		}
		this.classList.add('current');
		const question = document.getElementById(this.getAttribute('href'));
		if (question) {
			const properties = {
				behaviour: "smooth",
				inline: "nearest",
			};
			question.scrollIntoView(properties);
			window.scrollBy(0, -100);
		}
	}
	// Current item
	const els = document.getElementsByClassName('quiz_num');
	for (var i = 0; i < els.length; i++) {
		els[i].onclick = setCurrent;
	}


	// Set icon when question is in view
	function isInViewPort(element) {
		// Get the bounding client rectangle position in the viewport
		var bouding = element.getBoundingClientRect();

		// Here the code checks if it's fully visible
		// Edit this part if you just want a partial visibility
		if (
			bounding.top >= 0 &&
			bounding.left >= 0 &&
			bounding.right <= (window.innerWidth || document.documentElement.clientWidth) &&
			bounding.bottom <= (window.innerHeight || document.documentElement.clientHeight)
		) {
			console.log(`${this.attribute('id')} is in viewport`);
			return true;
		} else {
			return false;
		}
	}

	const quest = document.getElementsByClassName('question_item');
	for (var i = 0; i< quest.length; i++) {
		window.addEventListener('scroll', function (event) {
			if (isInViewPort(quest[i])) {
				console.log(quest.getAttribute('id'));
			}
		}, false);
	}
});
