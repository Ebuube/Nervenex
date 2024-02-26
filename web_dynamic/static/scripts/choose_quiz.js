#!/usr/bin/node
// Properties of the Choose Quiz page
$(function () {
	$("li.quiz_item").click(function takeQuiz() {
		// console.log($(this).attr('data-id'));
		console.log('Fetching quiz');
		const quiz_id = $(this).attr('data-id');

		// Keep user busy
		Swal.fire({
			icon: "info",
			title: "Hang in there 👨🏽‍🏫",
			text: "Setting up quiz for you...",
			timer: 360000,
			allowOutsideClick: false,
			didOpen: () => {
				Swal.showLoading();
			},
			willClose: () => {
			}
		});

		$.ajax({
			url: `http://localhost:5001/api/v1/quizzes/${quiz_id}`,
			type: 'GET',
			dataType: 'json',
		})
		.done(function (Quiz) {
			localStorage.setItem('Quiz', JSON.stringify(Quiz));
			window.location.href = `http://nervenex/quiz/${quiz_id}`;
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
