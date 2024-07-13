let summary = {};
summary.entries = [];
summary.range = {
	max: undefined,
	min: undefined,
	filterMax: undefined,
	filterMin: undefined
};

summary.setEntries = function(entries) {
	this.entries = entries;
	this.entries.forEach((entry) => {
		let date = new Date(entry['timestamp']);
		date = new Date(date.toDateString());

		entry['date'] = date;
		entry['volume'] = entry['mass'] / 1.03;

		if (date > this.range.max || !this.range.max) {
			this.range.max = date;
		}
		if (date < this.range.min || !this.range.min) {
			this.range.min = date;
		}
	});

	this.resetFilters();
}

summary.resetFilters = function() {
	this._initFilterRange();
	this.updatePlot();
}

summary._initFilterRange = function() {
	this.range.filterMax = this.range.max;
	this.range.filterMin = this.range.min;

	let pickers = this._getPickers();
	pickers[0].value = this._getFilterDate(this.range.min);
	pickers[1].value = this._getFilterDate(this.range.max);
}

summary.plotEntries = function() {
	let values = this._getValues();
	let data = {
		x: values.data.x,
		y: values.data.y,
		name: 'extractions',
		mode: 'markers',
		type: 'scatter',
		marker: {
			color: 'rgb(255,127,14)'
		}
	};

	let average = {
		x: values.calculated.keys,
		y: values.calculated.averages,
		name: 'average',
		type: 'bar',
		marker: {
			color: 'rgba(31,119,180,0.2)',
			line: {
				color: 'rgb(31,119,180)',
				width: 1.5
			}
		}
	};

	let total = {
		x: values.calculated.keys,
		y: values.calculated.totals,
		name: 'total',
		type: 'bar',
		marker: {
			color: 'rgba(44,160,44,0.2)',
			line: {
				color: 'rgb(44,160,44)',
				width: 1.5
			}
		}
	};

	let layout = {
		xaxis: {title: 'Date'},
		yaxis: {
			title: 'Volume (ml)',
			rangemode: 'tozero'
		}
	};

	let plot = document.getElementById('scatterPlot');
	Plotly.newPlot(plot, [average, total, data], layout);
}

summary.updatePlot = function() {
	let pickers = this._getPickers();

	this.range.filterMin = pickers[0].value;
	this.range.filterMax = pickers[1].value;

	this.plotEntries();
}

summary._getValues = function() {
	let values = {
		data:{x:[],y:[]},
		calculated:{
			keys:[],
			averages:[],
			totals:[]
		}
	};

	let tempEntries = this.entries.filter((entry) => {
		let date = this._getFilterDate(entry['date']);
		return date >= this.range.filterMin
			&& date <= this.range.filterMax;
	});
	let buckets = {};

	values.data.x = tempEntries.map((entry) => {
		let date = entry['date'].toDateString();
		if (!buckets[date]) {
			buckets[date] = [];
		}
		buckets[date].push(entry['volume']);

		return date;
	});
	values.data.y = tempEntries.map((entry) => entry['volume']);

	for (var key in buckets) {
		let masses = buckets[key];
		values.calculated.keys.push(key);

		let totalMass = masses
			.map(mass => Number(mass))
			.reduce((partialSum, mass) => partialSum + mass, 0);

		values.calculated.totals.push(totalMass);
		values.calculated.averages.push(totalMass / masses.length);
	};

	return values;
}

summary._getPickers = function() {
	return [document.getElementById('plotMinPicker'), document.getElementById('plotMaxPicker')];
}

summary._getFilterDate = function(date) {
	return dateUtils.formatTimestamp(date, dateUtils.ISO_8601, false);
}