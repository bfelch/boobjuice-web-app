import time

class Boobjuice:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_VOLUME = 'volume'
	PARAM_SOURCE = 'source'

	def __init__(self):
		pass

	def get(self):
		return ['entry1', 'entryA']

	def insert(self, data):
		self.validate_data('insert', data, [self.PARAM_VOLUME, self.PARAM_VOLUME])

		timestamp = data.get(self.PARAM_TIMESTAMP)
		volume = data.get(self.PARAM_VOLUME)
		source = data.get(self.PARAM_SOURCE)

		if timestamp is None:
			timestamp = time.time()
		
		pass

	def update(self, data):
		self.validate_data('update', data, [self.PARAM_TIMESTAMP, self.PARAM_VOLUME, self.PARAM_SOURCE])

		timestamp = data.get(self.PARAM_TIMESTAMP)
		volume = data.get(self.PARAM_VOLUME)
		source = data.get(self.PARAM_SOURCE)
		
		pass

	def delete(self, data):
		self.validate_data('delete', data, [self.PARAM_TIMESTAMP])
		
		timestamp = data.get(self.PARAM_TIMESTAMP)
		
		pass

	def validate_data(self, method, data, params=[]):
		if data is None:
			raise IllegalArgumentError('object is invalid for ' + method)
		
		for param in params:
			if data.get(param) is None:
				raise IllegalArgumentError(param + ' is invalid for ' + method)

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message