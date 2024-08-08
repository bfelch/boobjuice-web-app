let boobjuiceClient = {};
boobjuiceClient.URL = '/record/pumped-milk';

boobjuiceClient.insert = function(data) {
	this._validateData(data);

	return clientBase.callService(this.URL, 'PUT', data);
}

boobjuiceClient.update = async function(data) {
	this._validateData(data);

	return clientBase.callService(this.URL, 'POST', data);
}

boobjuiceClient.remove = async function(data) {
	this._validateData(data);

	return clientBase.callService(this.URL, 'DELETE', data);
}

boobjuiceClient._validateData = function(data) {
	if (data === undefined) {
		data = {};
	}

	data['source'] = 'W';
}