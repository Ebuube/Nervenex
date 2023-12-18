#!/usr/bin/node
// Properties of the Choose Quiz page
$(function () {
	$("li.quiz_item").click(function takeQuiz() {
		// console.log($(this).attr('data-id'));
		console.log('Fetching quiz');
		const quiz_id = $(this).attr('data-id');

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
			window.location.href = `http://localhost:5000/quiz/${quiz_id}`;
		}, 2000);
	});
});
