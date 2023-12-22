#!/usr/bin/node
// Properties of the Quiz page
$(function () {

	// Get quiz
	var Quiz = JSON.parse(localStorage.getItem('Quiz'));

	// console.log(Quiz);	// test
	if (Quiz == null) {
		console.log('Null quiz');	// test
		Swal.fire({
			title: "No quiz loaded 🥺",
			icon: "error",
			text: "Sorry, go to Menu >> Take a quiz."
		}).then((result) => {
			if (result.isConfirmed) {
				window.location.href = "http://web-01.brainspark.tech/nervenex/choose_quiz";
			}
		});
	}

	// Current item
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
	const els = document.getElementsByClassName('quiz_num');
	for (var i = 0; i < els.length; i++) {
		els[i].onclick = setCurrent;
	}
});
