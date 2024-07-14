from datetime import datetime, timedelta

import os
import mariadb
import random

def get_connection():
	database = os.environ['MARIA_DATABASE']
	username = os.environ['MARIA_USERNAME']
	password = os.environ['MARIA_PASSWORD']
	host = os.environ['MARIA_HOST']
	port = int(os.environ['MARIA_PORT'])

	try:
		conn = mariadb.connect(
			user=username,
			password=password,
			host=host,
			port=port,
			database=database,
			autocommit=True
		)
	except mariadb.Error as e:
		raise DataAccessError(f'Error connecting to MariaDB platform: {e}')

	return conn

class Boobjuice:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_MASS = 'mass'

	ISO_STD = '%Y-%m-%d %H:%M'
	ISO_8601 = '%Y-%m-%dT%H:%M'

	def __init__(self):
		pass

	def get(self):

		conn = get_connection()
		results = []

		try:
			cur = conn.cursor()
			cur.execute('SELECT U_EXTRACTED, Q_GRAMS FROM BOOBJUICE ORDER BY U_EXTRACTED ASC;')
			for (timestamp, mass) in cur:
				results.append({'timestamp':timestamp.strftime(self.ISO_STD), 'mass':mass})
		except mariadb.Error as e:
			raise DataAccessError(f'Error selecting from database: {e}')
		finally:
			conn.close()

		return results

		# return self._build_random_entries()

	def insert(self, data):
		self.validate_data('insert', data, [self.PARAM_MASS])

		timestamp = self.get_timestamp(data, optional=True)
		mass = data.get(self.PARAM_MASS)

		if timestamp is None:
			timestamp = datetime.now().strftime(self.ISO_8601)
		
		conn = get_connection()

		try:
			cur = conn.cursor()
			cur.execute('INSERT INTO BOOBJUICE(U_EXTRACTED, Q_GRAMS) VALUES(?, ?);', (timestamp, mass))
		except mariadb.Error as e:
			raise DataAccessError(f'Error inserting to database: {e}')
		finally:
			conn.close()

	def update(self, data):
		self.validate_data('update', data, [self.PARAM_TIMESTAMP, self.PARAM_MASS])

		timestamp = self.get_timestamp(data)
		mass = data.get(self.PARAM_MASS)
		
		conn = get_connection()

		try:
			cur = conn.cursor()
			cur.execute('UPDATE BOOBJUICE SET Q_GRAMS = ? WHERE U_EXTRACTED = ?;', (mass, timestamp))
		except mariadb.Error as e:
			raise DataAccessError(f'Error updating database: {e}')
		finally:
			conn.close()

	def delete(self, data):
		self.validate_data('delete', data, [self.PARAM_TIMESTAMP])
		
		timestamp = self.get_timestamp(data)
		
		conn = get_connection()

		try:
			cur = conn.cursor()
			cur.execute('DELETE FROM BOOBJUICE WHERE U_EXTRACTED = ?;', (timestamp,))
		except mariadb.Error as e:
			raise DataAccessError(f'Error deleting from database: {e}')
		finally:
			conn.close()

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
			return datetime.strptime(timestamp, self.ISO_8601)
		except ValueError:
			print(timestamp)
			raise IllegalArgumentError('invalid timestamp format')
	
	# def _build_random_entries(self):
	# 	random.seed('1234')

	# 	start_date = datetime.today()
	# 	entries = []
	# 	for i in range(40):
	# 		entries.append(self._build_random_entry(start_date))
		
	# 	return sorted(entries, key=lambda _e: _e.get('timestamp'))

	# def _build_random_entry(self, start_date):
	# 	timestamp = start_date - timedelta(minutes=random.randrange(21600))
	# 	mass = 50 + random.randrange(300)

	# 	return {'timestamp':timestamp.strftime('%Y-%m-%d %H:%M'), 'mass':mass}

class DataAccessError(Exception):
	def __init__(self, message='failed to connect to database'):
		self.message = message

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message