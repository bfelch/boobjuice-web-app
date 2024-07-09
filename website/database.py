from datetime import datetime

class Boobjuice:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_MASS = 'mass'

	def __init__(self):
		pass

	def get(self):
		return [{'timestamp':self.get_js_timestamp('2024/07/08 09:44:36'), 'mass':'123'},
		  {'timestamp':self.get_js_timestamp('2024/07/08 20:17:11'), 'mass':'108'}]

	def insert(self, data):
		self.validate_data('insert', data, [self.PARAM_MASS])

		timestamp = data.get(self.PARAM_TIMESTAMP)
		mass = data.get(self.PARAM_MASS)

		if timestamp is None:
			timestamp = datetime.now()
		else:
			timestamp = datetime.fromtimestamp(timestamp / 1000)
		
		pass

	def update(self, data):
		self.validate_data('update', data, [self.PARAM_TIMESTAMP, self.PARAM_MASS])

		timestamp = datetime.fromtimestamp(data.get(self.PARAM_TIMESTAMP))
		mass = data.get(self.PARAM_MASS)
		
		pass

	def delete(self, data):
		self.validate_data('delete', data, [self.PARAM_TIMESTAMP])
		
		timestamp = datetime.fromtimestamp(data.get(self.PARAM_TIMESTAMP))
		
		pass

	def get_js_timestamp(self, dbTimestamp):
		# get datetime object from db timestamp
		timestamp = datetime.strptime(dbTimestamp, '%Y/%m/%d %H:%M:%S')
		# format datetime object to js format for datetime-local input
		return timestamp.strftime('%Y-%m-%dT%H:%M:%S')

	def validate_data(self, method, data, params=[]):
		if data is None:
			raise IllegalArgumentError('object is invalid for ' + method)
		
		for param in params:
			if data.get(param) is None:
				raise IllegalArgumentError(param + ' is invalid for ' + method)

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message