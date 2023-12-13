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
});
