from datetime import datetime, timedelta

import os
import logging
import mariadb
import random

def get_connection():
	database = os.environ['MARIA_DATABASE']
	username = os.environ['MARIA_USERNAME']
	password = os.environ['MARIA_PASSWORD']
	port = int(os.environ['MARIA_PORT'])

	logging.info(f'maria variables: {database}, {username}, {password}, {port}')

	try:
		conn = mariadb.connect(
			user=username,
			password=password,
			host='127.0.0.1',
			port=port,
			database=database
		)
	except mariadb.Error as e:
		logging.error(f'Error connecting to MariaDB platform: {e}')
		raise DataAccessError(e)

	return conn.cursor()

class Boobjuice:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_MASS = 'mass'

	TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M'

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
			timestamp = datetime.now().strftime(self.TIMESTAMP_FORMAT)
		
		cursor = get_connection()

		print('inserting', data)
		pass

	def update(self, data):
		self.validate_data('update', data, [self.PARAM_TIMESTAMP, self.PARAM_MASS])

		timestamp = self.get_timestamp(data)
		mass = data.get(self.PARAM_MASS)
		
		cursor = get_connection()

		print('updating...', data)
		pass

	def delete(self, data):
		self.validate_data('delete', data, [self.PARAM_TIMESTAMP])
		
		timestamp = self.get_timestamp(data)
		
		cursor = get_connection()

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
			return datetime.strptime(timestamp, self.TIMESTAMP_FORMAT)
		except ValueError:
			print(timestamp)
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

		return {'timestamp':timestamp.strftime('%Y-%m-%d %H:%M'), 'mass':mass}

class DataAccessError(Exception):
	def __init__(self, message='failed to connect to database'):
		self.message = message

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message