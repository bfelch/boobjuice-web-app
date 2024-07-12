let clientBase = {};

clientBase.callService = function(url, method, data) {
	data = JSON.stringify(data);
	
	return fetch(url, {
		method: method,
		headers: {'Content-Type': 'application/json'},
		body: data
	})
	.then(response => {
		if (response.status === 200) {
			console.log('Service success!');
		} else {
			console.error('Service error!')
		}
		window.location.reload();
	})
	.catch((error) => {
		console.error('Service error!', error);
	});
}