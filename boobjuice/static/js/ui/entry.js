let entry = {};
entry.modal = undefined;
entry.currentItem = undefined;
entry.submitCallback = undefined;

entry.MODE = {
	INSERT: 0,
	UPDATE: 1,
	DELETE: 2
};

entry.show = function(mode, item) {
	if (this.modal === undefined) {
		this.modal = new bootstrap.Modal('#entryModal', {
			focus: true
		});
	}

	let modal = document.getElementById('entryModal');
	let titleTag = modal.getElementsByClassName('modal-title')[0];
	let title = 'Title Placeholder';
	switch (mode) {
		case this.MODE.INSERT:
			title = 'Insert';
			break;
		case this.MODE.UPDATE:
			title = 'Update';
			break;
		case this.MODE.DELETE:
			title = 'Want to delete?';
			break;
	}
	titleTag.textContent = title;

	this._initModal(mode);

	let timeTag = this.getTimeInput()
	let massTag = this.getMassInput();
	if (item === undefined) {
		timeTag.value = undefined;
		massTag.value = 0;

		this.submitCallback = this.insert;
	} else {
		// YYYY-mm-ddTHH:MM:SS (ie '2024-07-08T20:17:49')
		timeTag.value = dateUtils.formatTimestamp(item.timestamp, dateUtils.ISO_8601);
		massTag.value = item.mass;

		this.currentItem = item;
		if (mode == this.MODE.DELETE) {
			this.submitCallback = this.delete;
		} else {
			this.submitCallback = this.update;
		}
	}

	this.modal.show();
}

entry.hide = function() {
	this.currentItem = undefined;
	this.submitCallback = undefined;
	this.modal.hide();
}

entry._initModal = function(mode) {
	let timestampNote = document.getElementById('entryTimestampNote');
	if (mode == this.MODE.INSERT) {
		timestampNote.innerHTML = 'leave blank for current timestamp';
	} else {
		timestampNote.innerHTML = '';
	}
	
	this.getTimeInput().readOnly = mode >= this.MODE.UPDATE;
	this.getTimeInput().disabled = mode >= this.MODE.UPDATE;
	this.getMassInput().readOnly = mode >= this.MODE.DELETE;
	this.getMassInput().disabled = mode >= this.MODE.DELETE;
	this.getDurationInput().readOnly = mode >= this.MODE.DELETE;
	this.getDurationInput().disabled = mode >= this.MODE.DELETE;

	let submitButton = this.getSubmitButton();
	if (mode >= this.MODE.DELETE) {
		submitButton.classList.remove('btn-primary');
		submitButton.classList.add('btn-danger');
		submitButton.innerHTML = 'DELETE';
	} else {
		submitButton.classList.add('btn-primary');
		submitButton.classList.remove('btn-danger');
		submitButton.innerHTML = 'Save Changes';
	}
}

entry._initCurrentItem = function() {
	if (this.currentItem === undefined) {
		this.currentItem = {};
	}
}

entry._updateCurrentItem = function() {
	this._initCurrentItem();

	let timeInput = this.getTimeInput();
	this.currentItem['timestamp'] = dateUtils.formatTimestamp(timeInput.value, dateUtils.ISO_8601);

	let massInput = this.getMassInput();
	this.currentItem['mass'] = massInput.value;

	let durationInput = this.getDurationInput();
	this.currentItem['duration'] = durationInput.value;
}

entry.getTimeInput = function() {
	return document.getElementsByName('entryTimestamp')[0];
}

entry.getMassInput = function() {
	return document.getElementsByName('entryMass')[0];
}

entry.getDurationInput = function() {
	return document.getElementsByName('entryDuration')[0];
}

entry.getSubmitButton = function() {
	return document.getElementsByName('entrySubmit')[0];
}

entry.submit = function() {
	this._updateCurrentItem();

	if (!this.validate()) {
		return;
	}

	this.submitCallback();
	this.hide();
}

entry.validate = function() {
	if (!this.currentItem) {
		return this.handleError('entry item is undefined');
	}

	if (!this.currentItem.mass) {
		return this.handleError('entry mass is undefined');
	}

	if (!this.currentItem.duration) {
		return this.handleError('entry duration is undefined');
	}

	return true;
}

entry.handleError = function(message, category='danger') {
	let container = document.getElementById('entryAlertContainer');
	container.innerHTML = '';

	let alert = document.createElement('div');
	let alertMessage = document.createTextNode(message);
	let alertButton = document.createElement('button');

	alert.appendChild(alertMessage);
	alert.appendChild(alertButton);

	alert.classList.add('alert', `alert-${category}`, 'alert-dismissible', 'fade', 'show');
	alert.role = 'alert';
	
	alertButton.type = 'button';
	alertButton.classList.add('btn-close');
	alertButton.setAttribute('data-bs-dismiss', 'alert');
	alertButton.ariaLabel = 'Close';

	container.appendChild(alert);
}

entry.insert = function() {
	console.log('inserting...', this.currentItem);
	boobjuiceClient.insert(this.currentItem);
}

entry.update = function() {
	console.log('updating...', this.currentItem);
	boobjuiceClient.update(this.currentItem);
}

entry.delete = function(item) {
	console.log('deleting...', item);
	boobjuiceClient.remove(this.currentItem);
}