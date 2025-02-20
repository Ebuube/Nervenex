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
		if (email.length == 0) {
			// alert('You forgot to put your email in the box 😁');
			const msg = 'You forgot to put your email in the box 😁';
			// Message
			Swal.fire({
				icon: "error",
				title: "Oops...",
				text: `${msg}`
			});
			setTimeout(() => {}, 1500);
			return;
		}

		var password = document.getElementById('login_password').value;
		if (password.length == 0) {
			// alert('Kindly, put your password 😊');
			const msg = 'Kindly, put your password 😊';
			// Message
			Swal.fire({
				icon: "error",
				title: "Ugh...",
				text: `${msg}`
			});
			setTimeout(() => {}, 1500);
			return;
		}

		// Keep user busy
		Swal.fire({
			icon: "info",
			title: "Logging in 🔄",
			text: "Get ready for your learning journey...",
			timer: 360000,
			allowOutsideClick: false,
			didOpen: () => {
				Swal.showLoading();
			},
			willClose: () => {
			}
		});

		const details = {'email': email, 'password': password};
		$.ajax({
			url: `${API_BASE_URL}/login`,
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
			        // Link to take quizzes
		                window.location.assign(`WEB_BASE_URL/choose_quiz`);
			});
		})
		.fail(function (xhr, status, errorThrown) {
			console.log('Login failure');
			// alert(xhr.responseJSON.description);
			const msg = xhr.responseJSON.description;
			$('p#username').text('Unidentified User');
			$('div#api_status').text('U');

			// Message
			Swal.fire({
				icon: "error",
				title: "Oops...",
				text: `${msg}`
			});
			setTimeout(() => {}, 1500);
		});
	});

	$('#sign_up').click(function signUp() {
		window.location.assign(`${WEB_BASE_URL}/signup`);
	});
});
