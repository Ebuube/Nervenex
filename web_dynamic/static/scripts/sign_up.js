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


	// Error message
	function errorMsg(msg, title="Oops...", icon="error") {
		Swal.fire({
			icon: `${icon}`,
			title: `${title}`,
			text: `${msg}`
		});
		setTimeout(() => {}, 1500);
	};

	// Sign Up proper
	function createUser(payload) {
		if (!payload) {
			alert('Invalid form');
			return;
		};

		$.ajax({
			url: 'http://web-01.brainspark.tech/nervenex/api/v1/signup',
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

			// Message
			Swal.fire({
				title: "Welcome",
				text: "Login successful",
				icon: "success",
				timer: 2000,
				timerProgressBar: true,
				showConfirmButton: false,
				allowOutsideClick: false
			}).then((result) => {
				history.back();
			});

		})
		.fail(function (xhr, status, errorThrown) {
			console.log('Sign up failure');
			// alert(xhr.responseJSON.description);
			errorMsg(xhr.responseJSON.description, title="Sign up failure");
			$('p#username').text('Unidentified User');
			$('div#api_status').text('U');
		});
	};


	$('#sign_up').click(function signUp() {
		console.log('Processing sign up');
		var firstname = document.getElementById('firstname').value;
		if (firstname.length == 0) {
			// alert('Please, put your first name in the box 😁');
			const msg = 'Please, put your first name in the box 😁';
			errorMsg(msg);
			return;
		}

		var lastname = document.getElementById('lastname').value;
		if (lastname.length == 0) {
			// alert('Could you put your last name in the box 😁');
			const msg = 'Could you put your last name in the box 😁';
			errorMsg(msg);
			return;
		}

		var email = document.getElementById('email').value;
		if (email.length == 0) {
			// alert('You forgot to put your email in the box 😁');
			const msg = 'You forgot to put your email in the box 😁';
			errorMsg(msg);
			return;
		}

		var password = document.getElementById('password').value;
		if (password.length == 0) {
			// alert('Kindly, put your password 😊');
			const msg = 'Kindly, put your password 😊';
			errorMsg(msg);
			return;
		}

		var verify_password = document.getElementById('verify_password').value;
		if (verify_password.length == 0) {
			const msg = "Kindly verify your password 😊";
			errorMsg(msg);
			return;
		}

		if (verify_password !== password) {
			// alert('Kindly verify your password 😊');
			const msg = 'Kindly verify your password 😊';
			errorMsg(msg, title="Mismatch");
			return;
		}

		if (!$('#terms_of_service:checked').val()) {
			// alert('Hello, agree to our terms of service. 🥳');
			const msg = 'Hello, agree to our terms of service. 🥳';
			errorMsg(msg, title="Almost there", icon="info");
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
