#!/usr/bin/node
// Set some general properties
$(function() {

	// Show API status
	$.ajax({
		url: 'http://localhost:5001/api/v1/status',
		type: 'GET',
		dataType: 'json'
	})
	.done(function (json) {
		api = $('#api_status')
		console.log('API is available');
		if (!api.hasClass('api_active')) {
			api.addClass('api_active');
		}
	})
	.fail(function (xhr, status, errorThrown) {
		console.log('Could not access API');
		// Mesage
		Swal.fire({
			icon: "info",
			title: "Sorry 😔",
			text: "API server is inactive at the moment."
		});
		setTimeout(() => {}, 1500);

	});

	// Nervenex icon > Home
	nervenex_icon = $('.header_logo div.button');
	nervenex_icon.click(function () {
		window.location.href = 'http://localhost:5000/home';
	});


	// Menu -> navigation
	$('#menu_home').click(function() {
		window.location.href = 'http://localhost:5000/home';
	});

	$('#menu_take_quiz').click(function() {
		window.location.href = 'http://localhost:5000/take_quiz';
	});

	$('#menu_create_quiz').click(function() {
		window.location.href = 'http://localhost:5000/create_quiz';
	});

	$('#menu_view_posts').click(function() {
		window.location.href = 'http://localhost:5000/view_posts';
	});

	$('#menu_get_resources').click(function() {
		window.location.href = 'http://localhost:5000/get_resources';
	});

	$('#menu_login').click(function() {
		window.location.href = 'http://localhost:5000/login';
	});

	$('#menu_logout').click(function() {
		/*
		if (confirm('Are you sure you want to leave? 😫')) {
			localStorage.removeItem('user');
			$('p#username').text('Unidentified User');
			$('div#api_status').text('U');
		}
		*/
		Swal.fire({
			title: "Oh no! 😩",
			text: "Are you sure you want to leave?",
			icon: "question",
			showCancelButton: true,
			confirmButtonText: "Yes, I do"
		}).then((result) => {
			if (result.isConfirmed) {
				localStorage.removeItem('user');
				$('p#username').text('Unidentified User');
				$('div#api_status').text('U');
				console.log("Logged out successfully");
				Swal.fire({
					icon: "success",
					title: "Okay",
					text: "Successfully logged out!",
					timer: 2000,
					showConfirmButton: false
				});
			}
		});
	});

	// Footer -> navigation
	$('#footer_about').click(function() {
		window.location.href = 'https://nervenex.mailchimpsites.com/';
	});

	$('#footer_contact').click(function() {
		window.location.href = 'https://nervenex.mailchimpsites.com/';
	});

	$('#footer_terms').click(function() {
		window.location.href = 'https://nervenex.mailchimpsites.com/';
	});

	$('#footer_facebook').click(function() {
		window.location.href = 'https://www.facebook.com/groups/354878470471404/';
	});

	$('#footer_github_ebube').click(function() {
		window.location.href = 'https://github.com/Ebuube/';
	});

	$('#footer_github_edwin').click(function() {
		window.location.href = 'https://github.com/arkoaikins/';
	});
});
