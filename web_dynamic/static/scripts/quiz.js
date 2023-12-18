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


	/*
	// Set icon when question is in view
	const questions = document.getElementsByClassName('question_item');
	const observer = new IntersectionObserver((entries) => {
		entries.forEach((entry) => {
			// console.log(entry.target);
			var oldLink = document.getElementsByClassName('current')[0];
			if (oldLink) {
				oldLink.classList.remove('current');
			}
			console.log(`type: ${this}`);	// test
			var newLink = document.getElementById(`quiz_num.${this.id}`);
			console.log(newLink);
			if (newLink) {
				newLink.classLlist.add('current');
			}
		})
	});
	for (var i = 0; i < questions.length; i++) {
		observer.observe(questions[i]);
	}
	*/
});
