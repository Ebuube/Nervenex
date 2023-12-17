#!/usr/bin/node
// Properties of the Choose Quiz page
$(function () {
	$("li.quiz_item").click(function takeQuiz() {
		// console.log($(this).attr('data-id'));
		console.log('Fetching quiz');
		const quiz_id = $(this).attr('data-id');

		$.ajax({
			url: `http://localhost:5001/api/v1/quizzes/${quiz_id}/questions`,
			type: 'GET',
			dataType: 'json',
		})
		.done(function (json) {
			console.log('Quiz gotten');
			// Set data
			localStorage.setItem('questions', JSON.stringify(json));
			// Message
			Swal.fire({
				title: "Hang in there 👨🏽‍🏫",
				text: "Setting up quiz for you...",
				icon: "info",
				timer: 2000,
				timerProgressBar: true,
				showConfirmButton: false
			});
			setTimeout(() => {
				window.location.href = 'http://localhost:5000/quiz';
			}, 2000);
		})
		.fail(function (xhr, status, errorThrown) {
			console.log('Failure in getting quiz');
			const msg = xhr.responseJSON.description;
			// Message
			Swal.fire({
				icon: "error",
				title: "Oh oh!",
				text: `${msg}`
			});
		});
	});
});
