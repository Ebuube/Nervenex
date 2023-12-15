#!/usr/bin/node
// Set some general properties
$(function() {

	// Show API status
	$.ajax({
		url: 'http://localhost:5001/api/v1/status',
		type: 'GET',
		dataType: 'json'
	})
	.done (function (json) {
		api = $('#api_status')
		if (json.status == 'OK'){
			console.log('API is available');
			if (!api.hasClass('api_active')) {
				api.addClass('api_active');
			}
		}
		else {
			console.log('API is unavailable at the moment');
		}
	})
	.fail(function (xhr, status, errorThrown) {
		console.log('Could not access API');
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
});
