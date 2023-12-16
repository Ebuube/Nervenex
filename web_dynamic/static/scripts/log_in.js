#!/usr/bin/node
// Properties of the login page
$(function () {
	// Global variables
	var user = null;

	// Clone object
	function cloneObj (obj) {
		const clonedObject = JSON.parse(JSON.stringify(obj));
		return clonedObject;
	};

	$('#log_in').click(function logIn() {
		console.log('Processing login');
		var email = document.getElementById('login_email').value;
		var password = document.getElementById('login_password').value;
		const details = {'email': email, 'password': password};
		$.ajax({
			url: 'http://localhost:5001/api/v1/login',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: `${JSON.stringify(details)}`
		})
		.done(function (json) {
			// console.log(json);
			user = cloneObj(json);
			user.password = password;

			// Set data
			localStorage.setItem("user", JSON.stringify(user));
			window.location.href = 'http://localhost:5000/home';
		})
		.fail(function (xhr, status, errorThrown) {
			console.log('Login failure');
			alert(xhr.responseJSON.description);
			$('p#username').text('Unidentified User');
			$('div#api_status').text('U');
		});
	});

	$('#sign_up').click(function signUp() {
		window.location.href = 'http://localhost:5000/signup';
	});
});
