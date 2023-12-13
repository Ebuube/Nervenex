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
		console.log('API is available');
		api = $('header .user_detail .api_status')
		if (json.status == 'OK'){
			if (!api.hasClass('api_active')) {
				api.addClass('api_active');
			}
		}
	})
	.fail(function (xhr, status, errorThrown) {
		console.log('Could not access API');
	});
});
