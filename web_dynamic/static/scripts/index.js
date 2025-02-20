#!/usr/bin/node
// Properties of the index/welcome page
$(function() {


	$('#start').click(function() {
		window.location.assign(`${WEB_BASE_URL}/choose_quiz`);
	});
});
