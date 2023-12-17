#!/usr/bin/node
// Properties of the index/welcome page
$(function() {


	$('#start').click(function() {
		window.location.href = 'http://localhost:5000/take_quiz';
	});
});
