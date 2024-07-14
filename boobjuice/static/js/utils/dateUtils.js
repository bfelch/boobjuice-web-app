let dateUtils = {};
dateUtils.ISO_8601 = 'YYYY-mm-ddTHH:MM';

dateUtils.formatTimestamp = function(timestamp, format, includeTime=true, dateDelimiter='-', timeDelimiter=':') {
	if (!timestamp) {
		return undefined;
	}
	
	if (timestamp instanceof String) {
		timestamp = Date.parse(timestamp);
	}

	let datetime = new Date(timestamp);

	let year = datetime.getFullYear();
	let month = datetime.getMonth()+1;
	let day = datetime.getDate();
	let hours = datetime.getHours();
	let minutes = datetime.getMinutes();

	let dateString = this.formatDate(year, month, day, format, dateDelimiter);
	let timeString = this.formatTime(hours, minutes, format, timeDelimiter);

	let formattedTimestamp = dateString;
	if (includeTime) {
		switch (format) {
			case this.ISO_STD:
				formattedTimestamp += ` ${timeString}`;
				break;
			case this.ISO_8601:
				formattedTimestamp += `T${timeString}`;
				break;
		}
	}

	// console.log(formattedTimestamp);
	return formattedTimestamp;
}

dateUtils.formatDate = function(year, month, day, format=this.ISO_8601, dateDelimiter='-') {
	switch (format) {
		case this.ISO_STD:
		case this.ISO_8601:
			month = this.padElement(month, 2);
			day = this.padElement(day, 2);
			break;
	}

	switch (format) {
		case this.ISO_STD:
		case this.ISO_8601:
			return `${year}${dateDelimiter}${month}${dateDelimiter}${day}`;
	}

	console.error(`Invalid date format: ${format}`);
}

dateUtils.formatTime = function(hours, minutes, format=this.ISO_8601, timeDelimiter=':') {
	switch (format) {
		case this.ISO_8601:
			hours = this.padElement(hours, 2);
			minutes = this.padElement(minutes, 2);
			break;
	}

	switch (format) {
		case this.ISO_STD:
		case this.ISO_8601:
			return `${hours}${timeDelimiter}${minutes}`;
	}

	console.error(`Invalid time format: ${format}`);
}

dateUtils.padElement = function(value, length) {
	return String(value).padStart(length, '0');
}