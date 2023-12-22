#!/usr/bin/node
// Properties of the Quiz page
$(function () {

	// Get quiz
	var Quiz = JSON.parse(localStorage.getItem('Quiz'));

	// Count down timer
	var stopTimer = true;
	var timeExhausted = false;
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
				// seconds = -1;
				// countDownTime = -1;
				timeExhausted = true;
				Swal.fire({
					icon: "info",
					title: "Time up ⏳",
					text: "You have exhausted your time. Submission in progress...",
					timer: 3000,
					allowOutsideClick: false,
					showConfirmButton: false,
					timerProgressBar: true
				});
				// submitAnswers();
				console.log('Sumbitted answer');	// test
				submitAnswers();
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
				window.location.href = "http://web-01.brainspark.tech.tech/nervenex/choose_quiz";
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

	// Current item -> Quiz number
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


	// Answer submisison
	const submit = document.getElementById('submit');
	submit.onclick = function askToSubmit() {
		// Verify all questions are attempted
		let attempted = document.querySelectorAll('.quiz_num');
		for (let i = 0; i < attempted.length; i++) {
			console.log(`obj -> ${attempted[i].getAttribute('id')}`);	// test
			if (!attempted[i].classList.contains('attempted')) {
				// Unattempted question recognized
				console.log('\tNot attempted');	// test
				Swal.fire({
					icon: "warning",
					title: 'Wait a sec ... 🚦',
					text: "You have not attempted all questions. Do you still want to submit?",
					showCancelButton: true,
					confirmButtonText: 'Yes, submit'
				}).then((result) => {
					if (result.isConfirmed) {
						// submitAnswers();
						stopTimer = true;
						console.log('Sumbitted answer');	// test
						submitAnswers();
					}
				});
				return;
			} else {
				// If all questions have been attempted

				Swal.fire({
					icon: "question",
					title: "Submission",
					text: "Are you sure you want to submit?",
					showCancelButton: true
				}).then((result) => {
					if (result.isConfirmed) {
						// submitAnswers();
						stopTimer = true;
						console.log('Sumbitted answer');	// test
						submitAnswers();
					}
				});
			}
		};
	};


	// Properly compile and submit the answers
	function submitAnswers() {

		// Keep user busy
		Swal.fire({
			icon: "info",
			title: "Processing result",
			text: "Just hang in there, we are marking your scripts 😇",
			timer: 120000,
			allowOutsideClick: false,
			didOpen: () => {
				Swal.showLoading();
			},
			willClose: () => {
			}
		});

		let payload = new Object();
		payload['duration'] = Quiz.duration - countDownTime;
		payload['ans_per_question'] = new Object();
		let questions = document.querySelectorAll('.question_item');
		for (let i = 0; i < questions.length; i++) {
			/*
			 * Go through each <li> child of this object
			 * Pick the one with the class 'answer'
			 * If it is the first one, set answer as 1,
			 * if it is the second, set answer as 2
			 */
			const options = questions[i].getElementsByTagName('li');

			let ans = -1;
			for (let x = 0; x < options.length; x++, ans = -1) {
				if (options[x].classList.contains('answer')) {
					ans = x + 1;
					break;
				}
			}
			/*
			 * add the object -- to payload['ans_per_question']
			 * "id": answer value(1-4)
			 * Where id is li.getAttribute('id') remove the 'Question.' part
			 * which starts the string
			 */

			let obj = new Object();
			let id = questions[i].id.replace('Question.', '');
			payload.ans_per_question[id] = ans;
		}

		// console.log(JSON.stringify(payload));	// test
		user = localStorage.getItem('user');
		if (!user) {
			Swal.fire({
				icon: "warning",
				title: "Logged out! 🧐",
				text: "Log in to see your results "
			});
			// Redirect to log in page and redirect back to here
			// To be implemented
			return;
		}
		user = JSON.parse(user);
		if (!Quiz) {
			Swal.fire({
				icon: "error",
				title: "Quiz error",
				text: "No quiz identified to submit"
			});
			return;
		}

		$.ajax({
			url: `http://web-01.brainspark.tech.tech/nervenex/api/v1/submit/${user.id}/quiz/${Quiz.id}`,
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: `${JSON.stringify(payload)}`
		})
		.done(function (attempt) {
			console.log(attempt);	// test
			window.location.href = `http://web-01.brainspark.tech.tech/nervenex/correction/${attempt.id}`;
		})
		.fail(function (xhr, status, errorThrown) {
			errorMsg(xhr.responseJSON.description, title="Submission failure");
			console.log(xhr.responseJSON.description);	// test
		});
	}
});
