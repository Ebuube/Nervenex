#!/usr/bin/node
// Properties of the Sign up page
$(function () {
	// Global variables
	var user = null;

	// Clone object
	function cloneObj (obj) {
		const clonedObject = JSON.parse(JSON.stringify(obj));
		return clonedObject;
	};


	// Sign Up proper
	function createUser(payload) {
		if (!payload) {
			alert('Invalid form');
			return;
		};

		$.ajax({
			url: 'http://localhost:5001/api/v1/signup',
			type: 'POST',
			dataType: 'json',
			contentType: 'application/json',
			data: `${JSON.stringify(payload)}`
		})
		.done(function (json) {
			user = cloneObj(json);
			user.password = payload.password;

			// Set data
			localStorage.setItem('user', JSON.stringify(user));
			window.location.href = 'http://localhost:5000/home';
		})
		.fail(function (xhr, status, errorThrown) {
			console.log('Login failure');
			alert(xhr.responseJSON.description);
			$('p#username').text('Unidentified User');
			$('div#api_status').text('U');
		});
	};


	$('#sign_up').click(function signUp() {
		console.log('Processing sign up');
		var firstname = document.getElementById('firstname').value;
		if (firstname.length == 0) {
			alert('Please, put your first name in the box 😁');
			return;
		}

		var lastname = document.getElementById('lastname').value;
		if (lastname.length == 0) {
			alert('Could you put your last name in the box 😁');
			return;
		}

		var email = document.getElementById('email').value;
		if (email.length == 0) {
			alert('You forgot to put your email in the box 😁');
			return;
		}

		var password = document.getElementById('password').value;
		if (password.length == 0) {
			alert('Kindly, put your password 😊');
			return;
		}

		var verify_password = document.getElementById('verify_password').value;
		if (verify_password !== password) {
			alert('Kindly verify your password 😊');
			return;
		}

		if (!$('#terms_of_service:checked').val()) {
			alert('Hello, agree to our terms of service. 🥳');
			return;
		}

		const details = {
			'email': email,
			'first_name': firstname,
			'last_name': lastname,
			'password': password
		}

		createUser(details);
	});
});
