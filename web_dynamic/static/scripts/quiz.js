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


	// Select answer
	function setAnswer() {
		// set this option as answer
		let children = this.parentNode.children;

		for (let i = 0; i < children.length; i++) {
			children[i].classList.remove('answer');
		}
		this.classList.add('answer');
		const question = this.parentNode.parentNode.parentNode;
		let quiz_num = document.getElementById(`quiz_num.${question.id}`);
		quiz_num.classList.add('attempted');
	}
	const ans = document.querySelectorAll('.question_item ol li');
	for (var i = 0; i < ans.length; i++) {
		ans[i].onclick = setAnswer;
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
