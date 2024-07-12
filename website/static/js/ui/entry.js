let entry = {};
entry.modal = undefined;
entry.currentItem = undefined;
entry.submitCallback = undefined;

entry.show = function(title, item, deleting=false) {
	if (this.modal === undefined) {
		this.modal = new bootstrap.Modal('#entryModal', {
			focus: true
		});
	}

	let modal = document.getElementById('entryModal');
	let titleTag = modal.getElementsByClassName('modal-title')[0];
	titleTag.textContent = title;

	this._initModal(deleting);

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
		if (deleting) {
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

entry._initModal = function(deleting) {
	this.getTimeInput().readOnly = deleting;
	this.getTimeInput().disabled = deleting;
	this.getMassInput().readOnly = deleting;
	this.getMassInput().disabled = deleting;

	let submitButton = this.getSubmitButton();
	if (deleting) {
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

entry.updateItemTimestamp = function() {
	this._initCurrentItem();

	let timeInput = this.getTimeInput();
	this.currentItem['timestamp'] = dateUtils.formatTimestamp(timeInput.value, dateUtils.ISO_STD, true, '/');
	console.log('changed timestamp...', this.currentItem);
}

entry.updateItemMass = function() {
	this._initCurrentItem();

	let massInput = this.getMassInput();
	this.currentItem['mass'] = massInput.value;
	console.log('changed mass...', this.currentItem);
}

entry.getTimeInput = function() {
	return document.getElementsByName('entryTimestamp')[0];
}

entry.getMassInput = function() {
	return document.getElementsByName('entryMass')[0];
}

entry.getSubmitButton = function() {
	return document.getElementsByName('entrySubmit')[0];
}

entry.submit = function() {
	this.submitCallback();
	this.hide();
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