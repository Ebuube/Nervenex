#!/usr/bin/node
// Properties of the index/welcome page
$(function() {
	user = JSON.parse(localStorage.getItem('user'));
	// console.log(user);	// test

	function setUserDetails(user) {
		// console.log(user);
		user.first_name.toLowerCase();
		user.last_name.toLowerCase();
		user.first_name[0] = user.first_name[0].toUpperCase();
		user.last_name[0] = user.last_name[0].toUpperCase();
		$('p#username').text(user.first_name + ' ' + user.last_name);
		$('div#api_status').text(user.first_name[0]);
	};
	if (user) {
		setUserDetails(user);
	}


	$('#start').click(function() {
		window.location.href = 'http://localhost:5000/take_quiz';
	});
});
