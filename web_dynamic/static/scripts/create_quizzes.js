// Properties of Quiz creation
$(function () {

	// Execute on page load
	Swal.fire({
		title: "Welcome! 🤩",
		icon: "info",
		text: "Scroll down the left panel to upload quiz",
		timer: 3000,
		timerProgressBar: true,
		showConfirmButton: false,
		allowOutsideClick: false
	}).then((result) => {
		if (result.dismiss === Swal.DismissReason.timer) {
			stopTimer = false;	// start countdown timer
		}
	});



	// Choose a category
	function setChosen() {
		let oldChoice = document.querySelector('.cat_chosen');
		if (oldChoice) {
			oldChoice.classList.remove('cat_chosen');
		}
		this.classList.add('cat_chosen');
	}
	let categories = document.querySelectorAll('.categories li');
	for (let i = 0; i < categories.length; i++) {
		categories[i].onclick = setChosen;
	}


	// Delete a question
	function deleteQuestion() {
		Swal.fire({
			icon: "warning",
			title: "Delete ? 🥵",
			text: "Are you sure you want to delete this question?",
			showCancelButton: true
		}).then((result) => {
			if (result.isConfirmed) {
				this.parentNode.parentNode.remove();
			}
		});
	}

	function bindDeleteQuestion() {
		delButtons = document.querySelectorAll('.question_item span.delete_question');
		if (!delButtons) {
			return;
		}
		for (let i = 0; i < delButtons.length; i++) {
			delButtons[i].onclick = deleteQuestion;
		}
	}
	

	// Default operations on start up
	bindDeleteQuestion();
	var questionId = 1;
	$('.question_item').attr('id', questionId);


	// Add a new question
	const addQuestionBtn = document.getElementById('add_question');
	addQuestionBtn.onclick = function addQuestion() {
		let questions = $('.questions ul');
		questionId = questionId + 1;
		let element = `<li class="question_item" id="${questionId}">
			                        <article>
			    			    <span class="delete_question">Delete</span>

			                            <textarea class="question_content" maxlength="512" placeholder="Describe the question ..."></textarea>
			                            <p>* Select the correct option.</p>
			                            <ol>
			                                <!--
		                                <li class="answer"><input class="checkbox" type="radio" name="question.${questionId}"/> <input maxlength="128" type="text" placeholder="Option C"/></li>
			                                -->
			                                <li><input class="checkbox" type="radio" name="question.${questionId}"/> <input maxlength="128" type="text" placeholder="Option A"/></li>
			                                <li><input class="checkbox" type="radio" name="question.${questionId}"/> <input maxlength="128" type="text" placeholder="Option B"/></li>
			                                <li><input class="checkbox" type="radio" name="question.${questionId}"/> <input maxlength="128" type="text" placeholder="Option C"/></li>
			                                <li><input class="checkbox" type="radio" name="question.${questionId}"/> <input maxlength="128" type="text" placeholder="Option D"/></li>
			                            </ol>
			                            <p>* Give explanation for answer (optional)</p>
			                            <textarea class="explanation" placeholder="Explain why it is so ..."></textarea>
			                        </article>
			                    </li>`;


		questions.append(element);
		bindDeleteQuestion();
		// Add its question number
		// $('.quiz_numbers ul').append(`<li>${questionCount}</li>`);
	};


	// Error message
	function errorMsg(msg, title="Oops...", icon="error") {
		Swal.fire({
			icon: `${icon}`,
			title: `${title}`,
			text: `${msg}`,
		}).then((result) => {
			return;
		});
	};


	function createQuiz(category_id="", duration=0) {
		// Create Quiz
		let uploadStatus = true;
		let Quiz = new Object();
		let payload = new Object();
		payload.user_id = user.id;
		payload.category_id = category_id;
		payload.title = document.querySelector('.quiz_info .quiz_title').value;
		payload.description = document.querySelector('.quiz_info .description').value;
		payload.duration = duration;
		payload.is_active = true;
		$.ajax({
			url: 'http://web-01.brainspark.tech/nervenex/api/v1/quizzes',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: `${JSON.stringify(payload)}`
		})
		.done(function (quiz) {
			Quiz = JSON.parse(JSON.stringify(quiz));
			console.log(Quiz);	// test
			if (uploadQuestions(Quiz)) {
				// Done Uploading quiz
				Swal.fire({
					icon: 'success',
					title: 'Hurray!! 🥳',
					text: 'Quiz successfully created',
					allowOutsideClick: false,
					timer: 3000,
					timerProgressBar: true
				}).then((result) => {
					history.back();	// go back to the previous page
				});
			}
		})
		.fail(function (xhr, status, errorThrown) {
			uploadStatus = false;
			console.log(xhr.responseJSON.description);
			errorMsg(xhr.responseJSON.description, title="Oh! No! 😣");
		});
		if (!uploadStatus) {
			return;
		}

		return true;
	}




	/*
	 * Properly upload a quiz
	 */
	function postQuiz(user=null, duration=null) {
		// Keep user busy
		Swal.fire({
			icon: "info",
			title: "Uploading quiz",
			text: "Just hang in there, we are uploading your quiz 😇",
			timer: 120000,
			// allowOutsideClick: false,
			didOpen: () => {
				Swal.showLoading();
			},
			willClose: () => {
			}
		});

		// Ensure category is valid
		let new_cat = document.querySelector('.new_category');
		var new_category = new Object();
		let uploadStatus = true;
		if (new_cat.value.length > 0) {
			let payload = new Object();
			payload.name = new_cat.value;

			// Creat new category
			$.ajax({
				url: 'http://web-01.brainspark.tech/nervenex/api/v1/categories',
				type: 'POST',
				dataType: 'json',
				contentType: 'application/json',
				data: `${JSON.stringify(payload)}`
			})
			.done(function (category) {
				new_category = JSON.parse(JSON.stringify(category));
				console.log(new_category);	// test
				if (!createQuiz(category_id=category.id, duration=duration)) {
					uploadStatus = false;
					errorMsg('Sorry, we could not create Quiz your quiz.');
				}
			})
			.fail(function (xhr, status, errorThrown) {
				uploadStatus = false;
				console.log(xhr.responseJSON.description);
				errorMsg(xhr.responseJSON.description, title="Oh! No! 😣");
			});
		} else {
			new_category = new Object();
			const id = document.querySelector('.quiz_info select.categories').value;
			console.log(`category id: ${id}`);	// test
			new_category.id = id;

			if (!createQuiz(category_id=new_category.id, duration=duration)) {
				uploadStatus = false;
				errorMsg('Sorry, we could not create Quiz your quiz.');
			}
		}
		if (!uploadStatus) {
			return;
		}

	}

	////////////////////

	////////////////////
	


	// Upload questions to quiz - one at a time
	function uploadQuestions(quiz=null) {
		if (!quiz) {
			return;
		}

		let uploadStatus = true;
		let allQuestions = document.querySelectorAll('.question_item');
		for (let i = 0; i < allQuestions.length; i++) {
			payload = new Object();

			console.log(`Quiz id: ${quiz.id}`);	// test

			payload.quiz_id = quiz.id;
			payload.content = allQuestions[i].querySelector('.question_content').value;
			payload.option_a = allQuestions[i].querySelectorAll('input[type="text"]')[0].value;
			payload.option_b = allQuestions[i].querySelectorAll('input[type="text"]')[1].value;
			payload.option_c = allQuestions[i].querySelectorAll('input[type="text"]')[2].value;
			payload.option_d = allQuestions[i].querySelectorAll('input[type="text"]')[3].value;
			// Pick correct answer
			let options = allQuestions[i].querySelectorAll('input[type="radio"]');
			console.log(options);	// test
			payload.correct_answer = -1;
			for (let a = 0; a < options.length; a++) {
				if (options[a].checked) {
					payload.correct_answer = a + 1;
					console.log(`In Answer: ${payload.correct_answer}`);	// test
				}
			}
			console.log(`Out Answer: ${payload.correct_answer}`);	// test
			payload.explanation = allQuestions[i].querySelector('.explanation').value;
			$.ajax({
				url: 'http://web-01.brainspark.tech/nervenex/api/v1/questions',
				type: 'POST',
				dataType: 'json',
				contentType: 'application/json',
				data: `${JSON.stringify(payload)}`
			})
			.done(function (question) {
				console.log(`Question upload:\n${question}`);
			})
			.fail(function (xhr, status, errorThrown) {
				uploadStatus = false;
				console.log(xhr.responseJSON.description);
				errorMsg(xhr.responseJSON.description, title="Oh! No! 😣");
			});
			if (!uploadStatus) {
				return false;
			}

		}

		return true;
	}

	////////////////////

	/*
	 * Verify the format of a quiz
	 */
	function uploadQuiz() {
		// console.log('Quiz uploaded');	// test
		// Verify quiz details

		if ($('.quiz_info .quiz_title').val().length == 0) {
			Swal.fire({
				icon: "warning",
				title: "No title",
				text: "Please add a title for the quiz"
			});
			return;
		}

		// Veiry quiz description
		if ($('.quiz_info .description').val().length == 0) {
			Swal.fire({
				icon: "warning",
				title: "No description",
				text: "Please add a description for the quiz"
			});
			return;
		}

		// Time alloted
		const alloted_time = document.querySelector('.quiz_info input.alloted_time');
		const empty = "";
		console.log(`${alloted_time.value}`);	// test
		if (alloted_time.value == empty) {
			Swal.fire({
				icon: "warning",
				title: "No time ⏳",
				text: "Please allot a time for the quiz E.g 00:04 that is 4 minutes"
			});
			return;
		}
		const timeArray = alloted_time.value.split(':');
		const hours = parseInt(timeArray[0]);
		const minutes = parseInt(timeArray[1]);
		if (isNaN(hours) || isNaN(minutes) || (hours == 0 && minutes == 0)) {
			console.log('Error converting time');
			Swal.fire({
				icon: "error",
				title: "Invalid time",
				text: "Please set a valid time"
			});
			return;
		}
		var duration = (hours * 60) + minutes;
		console.log(duration);

		// Verify category selected
		const cat_id = document.querySelector('select.categories').value;
		const new_cat = document.querySelector('.new_category');
		if (cat_id == "" && new_cat.value.length == 0) {
			Swal.fire({
				icon: "warning",
				title: "No category",
				text: "Select a category or create a new one"
			});
			return;
		}

		// Verify user exists
		var user = localStorage.getItem('user');
		if (!user) {
			Swal.fire({
				icon: "error",
				title: "You are logged out",
				text: "Open a new tab and log in then return to upload quiz"
			});
			return;
		}
		user = JSON.parse(user);


		// Verify all question are in good format
		let questions = document.querySelectorAll('.question_item');
		if (!questions || questions.length == 0) {
			Swal.fire({
				icon: 'warning',
				title: 'No question here',
				text: 'Please add a question to your quiz'
			});
			return;
		}
		for (let i = 0; i < questions.length; i++) {
			// verify format
			if (questions[i].querySelector('.question_content').value.length == 0) {
				Swal.fire({
					icon: "warning",
					title: "Missing question description",
					text: `Give a description to question number ${i + 1}`
				});
				return;
			}
			let options = questions[i].querySelectorAll('li');
			let correct_answer = undefined;
			for (let a = 0; a < options.length; a++) {
				// Check empty option
				if (options[a].querySelector('input[type="text"]').value.length == 0) {
					Swal.fire({
						icon: "warning",
						title: "Missing option",
						text: `Add a content to option ${a + 1} of question ${i + 1}`
					});
					return;
				}
				if (options[a].querySelector('input[type="radio"]').checked) {
					correct_answer = true;
				}
			}
			if (!correct_answer) {
				Swal.fire({
					icon: "warning",
					title: "No correct option",
					text: `Pick a correction option for question ${i + 1}`
				});
				return;
			}
		}

		postQuiz(user=user, duration=duration);
		return;

	};

	const upload = document.querySelector('#upload');
	upload.onclick = uploadQuiz;
});
