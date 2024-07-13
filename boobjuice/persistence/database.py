from datetime import datetime, timedelta

import random

class Boobjuice:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_MASS = 'mass'

	def __init__(self):
		pass

	def get(self):
		return self._build_random_entries()
		# return [{'timestamp':'2024/07/08 09:44:36', 'mass':'123'},
		#   {'timestamp':'2024/07/08 20:17:11', 'mass':'108'},
		#   {'timestamp':'2024/07/09 04:11:32', 'mass':'144'},
		#   {'timestamp':'2024/07/09 10:27:22', 'mass':'121'},
		#   {'timestamp':'2024/07/09 23:27:22', 'mass':'136'},
		#   {'timestamp':'2024/07/10 08:58:09', 'mass':'131'},
		#   {'timestamp':'2024/07/10 13:33:47', 'mass':'117'}]

	def insert(self, data):
		self.validate_data('insert', data, [self.PARAM_MASS])

		timestamp = self.get_timestamp(data, optional=True)
		mass = data.get(self.PARAM_MASS)

		if timestamp is None:
			timestamp = datetime.now()
		
		print('inserting', data)
		pass

	def update(self, data):
		self.validate_data('update', data, [self.PARAM_TIMESTAMP, self.PARAM_MASS])

		timestamp = self.get_timestamp(data)
		mass = data.get(self.PARAM_MASS)
		
		print('updating...', data)
		pass

	def delete(self, data):
		self.validate_data('delete', data, [self.PARAM_TIMESTAMP])
		
		timestamp = self.get_timestamp(data)
		
		print('deleting...', data)
		pass

	def validate_data(self, method, data, params=[]):
		if data is None:
			raise IllegalArgumentError('object is invalid for ' + method)
		
		for param in params:
			if data.get(param) is None:
				raise IllegalArgumentError(param + ' is invalid for ' + method)
	
	def get_timestamp(self, data, optional=False):
		if optional and self.PARAM_TIMESTAMP not in data:
			return None
		
		try:
			timestamp = data.get(self.PARAM_TIMESTAMP)
		except:
			raise IllegalArgumentError('timestamp is required')
		
		try:
			return datetime.strptime(timestamp, '%Y/%m/%d %H:%M:%S')
		except ValueError:
			raise IllegalArgumentError('invalid timestamp format')
	
	def _build_random_entries(self):
		random.seed('1234')

		start_date = datetime.today()
		entries = []
		for i in range(40):
			entries.append(self._build_random_entry(start_date))
		
		return sorted(entries, key=lambda _e: _e.get('timestamp'))

	def _build_random_entry(self, start_date):
		timestamp = start_date - timedelta(minutes=random.randrange(21600))
		mass = 50 + random.randrange(300)

		return {'timestamp':timestamp.strftime('%Y-%m-%d %H:%M:%S'), 'mass':mass}

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message