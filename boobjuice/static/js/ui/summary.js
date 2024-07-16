let summary = {};
summary.TYPE = {
	VOLUME: 0,
	DURATION: 1
};

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

summary.initPlotTypes = function() {
	let plotTypeInput = this._getPlotTypeInput();
	plotTypeInput.innerHTML = '';

	for (let key in this.TYPE) {
		let option = document.createElement('option');
		option.value = this.TYPE[key];
		option.innerHTML = this._getPlotYTitle(this.TYPE[key]);
		
		plotTypeInput.appendChild(option);
	}
}

summary.updatePlotType = function() {
	this.plotType = Number(this._getPlotTypeInput().value);
	this.updatePlot();
}

summary.resetFilters = function() {
	this.plotType = this.TYPE.VOLUME;
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

summary.updatePlotDetails = function(numberPumps, totalValue) {
	let plotDetails = this._getPlotDetails();

	let plotType = this._getPlotYTitle();
	plotDetails[0].value = numberPumps;
	plotDetails[1].innerHTML = 'Total ' + plotType;
	plotDetails[2].value = this._formatNumber(totalValue);
	plotDetails[3].innerHTML = 'Average ' + plotType;
	plotDetails[4].value = this._formatNumber(totalValue / numberPumps);
}

summary.plotEntries = function() {
	let values = this._getValues();
	let data = {
		x: values.data.x,
		y: values.data.y,
		name: 'pumps',
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
			title: this._getPlotYTitle(),
			rangemode: 'tozero'
		}
	};

	this.updatePlotDetails(values.details.numberPumps, values.details.totalValue);

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
		},
		details:{
			totalValue:0,
			numberPumps:0
		}
	};

	let tempEntries = this.entries.filter((entry) => {
		let date = this._getFilterDate(entry['date']);
		return date >= this.range.filterMin
			&& date <= this.range.filterMax;
	});
	let buckets = {};

	let valueKey = this._getKeyValue();

	values.data.x = tempEntries.map((entry) => {
		let date = entry['date'].toDateString();
		if (!buckets[date]) {
			buckets[date] = [];
		}
		buckets[date].push(entry[valueKey]);

		return date;
	});
	values.data.y = tempEntries.map((entry) => this._formatNumber(entry[valueKey]));

	for (var dateKey in buckets) {
		let pumpValues = buckets[dateKey];
		values.calculated.keys.push(dateKey);

		let subtotalPumpValue = pumpValues
			.map(pumpValue => Number(pumpValue))
			.reduce((partialSum, pumpValue) => partialSum + pumpValue, 0);

		values.calculated.totals.push(this._formatNumber(subtotalPumpValue));
		values.calculated.averages.push(this._formatNumber(subtotalPumpValue / pumpValues.length));

		values.details.totalValue += subtotalPumpValue;
		values.details.numberPumps += pumpValues.length;
	};

	return values;
}

summary._getPlotYTitle = function(key=this.plotType) {
	switch (key) {
		case this.TYPE.VOLUME:
			return 'Volume (ml)';
		case this.TYPE.DURATION:
			return 'Duration (min)';
	}

	return 'Title Placeholder';
}

summary._getKeyValue = function(key=this.plotType) {
	switch (key) {
		case this.TYPE.VOLUME:
			return 'volume';
		case this.TYPE.DURATION:
			return 'duration';
	}

	return 'invalid';
}

summary._getPlotTypeInput = function() {
	return document.getElementById('plotTypeInput');
}

summary._getPickers = function() {
	return [document.getElementById('plotMinPicker'), document.getElementById('plotMaxPicker')];
}

summary._getFilterDate = function(date) {
	return dateUtils.formatTimestamp(date, dateUtils.ISO_8601, false);
}

summary._getPlotDetails = function() {
	return [
		document.getElementById('plotNumberPumpsDetails'),
		document.getElementById('plotTotalValueLabel'),
		document.getElementById('plotTotalValueDetails'),
		document.getElementById('plotAverageValueLabel'),
		document.getElementById('plotAverageValueDetails')
	];
}

summary._formatNumber = function(number) {
	return Number(number.toFixed(2));
}