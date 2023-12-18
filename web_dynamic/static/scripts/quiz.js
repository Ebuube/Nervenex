#!/usr/bin/node
// Properties of the Quiz page
$(function () {

	// Get quiz
	var Quiz = JSON.parse(localStorage.getItem('Quiz'));

	// Count down timer
	var stopTimer = true;
	var countDownTime = Quiz.duration;
	var seconds = 0;
	// console.log(countDownTime);	// test
	window.setInterval(function perSec() {
		if (!stopTimer) {
			if (seconds > 0) {
				seconds = seconds - 1;
				$('div.timer .figures .seconds').html(seconds);
			} else if (countDownTime > 0) {
				seconds = 59;
				countDownTime = countDownTime - 1;
				$('div.timer .figures .hour').html(countDownTime);
				$('div.timer .figures .seconds').html(seconds);
			} else {
				stopTimer = true;
				seconds = -1;
				countDownTime = -1;
				Swal.fire({
					icon: "info",
					title: "Time up ⏳",
					text: "You have exhausted your time",
					confirmButtonText: "Submit",
					allowOutsideClick: false
				});
			}

		}
	}, 1000);

	// console.log(Quiz);	// test
	if (Quiz == null) {
		console.log('Null quiz');	// test
		Swal.fire({
			title: "No quiz loaded 🥺",
			icon: "error",
			text: "Sorry, go to Menu >> Take a quiz."
		}).then((result) => {
			if (result.isConfirmed) {
				window.location.href = "http://localhost:5000/choose_quiz";
			}
		});
	} else {
		Swal.fire({
			title: "Hurray! 🤩",
			icon: "info",
			text: "Scroll down the left panel to submit quiz",
			timer: 3000,
			timerProgressBar: true,
			showConfirmButton: false,
			allowOutsideClick: false
		}).then((result) => {
			if (result.dismiss === Swal.DismissReason.timer) {
				stopTimer = false;	// start countdown timer
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
		quiz_num.onclick();
	}
	const ans = document.querySelectorAll('.question_item ol li');
	for (var i = 0; i < ans.length; i++) {
		ans[i].onclick = setAnswer;
	}
});
