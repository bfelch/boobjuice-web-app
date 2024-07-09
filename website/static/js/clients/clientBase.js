let clientBase = {};

clientBase.callService = function(url, method, data) {
	console.log(data);
	data = JSON.stringify(data);
	console.log(data);
	
	return fetch(url, {
		method: method,
		headers: {'Content-Type': 'application/json'},
		body: data
	})
	.then(response => {
		console.log('Success!');
		window.location.reload();
	})
	.catch((error) => {
		console.error('Error', error);
	});
}