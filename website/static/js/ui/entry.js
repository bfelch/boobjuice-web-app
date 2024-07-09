let entry = {};
entry.modal = undefined;

entry.show = function(title, item) {
	if (this.modal === undefined) {
		this.modal = new bootstrap.Modal('#entryModal', {
			focus: true
		});
	}

	let modal = document.getElementById('entryModal');
	let titleTag = modal.getElementsByClassName('modal-title')[0];
	titleTag.textContent = title;

	let timeTag = document.getElementsByName('entryTimestamp')[0];
	let massTag = document.getElementsByName('entryMass')[0];
	if (item === undefined) {
		timeTag.value = undefined;
		massTag.value = 0;
	} else {
		// YYYY-mm-ddTHH:MM (ie '2024-07-08T20:17')
		timeTag.value = item.timestamp;
		massTag.value = item.mass;
	}

	this.modal.show();
}