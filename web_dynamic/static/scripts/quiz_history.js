#!/usr/bin/node
// Properties of the Choose Quiz page
$(function () {

	// View history
	var clickedAttempt = false;
	function viewHistory() {
		clickedAttempt = true;
		window.location.href = `http://web-01.brainspark.tech/nervenex/correction/${this.id}`;
	}

	// bind function to attempts
	let attempts = document.querySelectorAll('.user_attempts p');
	for (let i = 0; i < attempts.length; i++) {
		attempts[i].onclick = viewHistory;
	}


	// Retake a quiz
	$("li.quiz_item").click(function takeQuiz() {
		// console.log($(this).attr('data-id'));
		if (clickedAttempt == true) {
			// Don't open quiz if the user only wants to see the correction
			return;
		}
		console.log('Fetching quiz');
		const quiz_id = $(this).attr('data-id');

		$.ajax({
			url: `http://web-01.brainspark.tech/nervenex/api/v1/quizzes/${quiz_id}`,
			type: 'GET',
			dataType: 'json',
		})
		.done(function (Quiz) {
			localStorage.setItem('Quiz', JSON.stringify(Quiz));
			// Message
			Swal.fire({
				title: "Hang in there 👨🏽‍🏫",
				text: "Setting up quiz for you...",
				icon: "info",
				timer: 2000,
				timerProgressBar: true,
				showConfirmButton: false,
				allowOutsideClick: false
			});
			setTimeout(() => {
				window.location.href = `http://web-01.brainspark.tech/nervenex/quiz/${quiz_id}`;
			}, 2000);
		})
		.fail(function (xhr, status, errorThrown) {
			console.log('Quiz not found');
			const msg = xhr.responseJSON.description;
			// Message
			Swal.fire({
				icon: "error",
				title: "Quiz unavailable 😣",
				text: "Sorry, we could not get this quiz, you can try another quiz. 😉"
			});
		});
	});
});
