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
	PARAM_DURATION = 'duration'

	ISO_STD = '%Y-%m-%d %H:%M'
	ISO_8601 = '%Y-%m-%dT%H:%M'

	TBL_NAME = 'PUMPED_MILK'
	COL_ID = 'U_PUMPED'
	COL_MASS = 'Q_PUMPED_GRAMS'
	COL_DURATION = 'Q_PUMPED_MINUTES'

	def __init__(self):
		conn = get_connection()

		try:
			cur = conn.cursor()
			cur.execute(f'CREATE TABLE IF NOT EXISTS {self.TBL_NAME} (\n'
			   f'  `{self.COL_ID}` TIMESTAMP NOT NULL,\n'
			   f'  `{self.COL_MASS}` SMALLINT(5) UNSIGNED DEFAULT NULL,\n'
			   f'  `{self.COL_DURATION}` SMALLINT(5) UNSIGNED DEFAULT NULL,\n'
			   f'  `S_UPDATE` TIMESTAMP NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),\n'
			   f'  PRIMARY KEY (`{self.COL_ID}`),\n'
			   f'  UNIQUE KEY `{self.COL_ID}_U1` (`{self.COL_ID}`)\n'
			   f') ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;')
		except mariadb.Error as e:
			raise DataAccessError(f'Error initializing table: {e}')
		finally:
			conn.close()

	def get(self):
		conn = get_connection()
		results = []

		try:
			cur = conn.cursor()
			cur.execute(f'SELECT {self.COL_ID}, {self.COL_MASS}, {self.COL_DURATION} FROM {self.TBL_NAME} ORDER BY {self.COL_ID} ASC;')
			for (timestamp, mass, duration) in cur:
				results.append({'timestamp':timestamp.strftime(self.ISO_STD), 'mass':mass, 'duration':duration})
		except mariadb.Error as e:
			raise DataAccessError(f'Error selecting from database: {e}')
		finally:
			conn.close()

		return results

	def insert(self, data):
		self.validate_data('insert', data, [self.PARAM_MASS, self.PARAM_DURATION])

		timestamp = self.get_timestamp(data, optional=True)
		mass = data.get(self.PARAM_MASS)
		duration = data.get(self.PARAM_DURATION)

		if timestamp is None:
			timestamp = datetime.now().strftime(self.ISO_8601)
		
		conn = get_connection()

		try:
			cur = conn.cursor()
			cur.execute(f'INSERT INTO {self.TBL_NAME}({self.COL_ID}, {self.COL_MASS}, {self.COL_DURATION}) VALUES(?, ?);', (timestamp, mass, duration))
		except mariadb.Error as e:
			raise DataAccessError(f'Error inserting to database: {e}')
		finally:
			conn.close()

	def update(self, data):
		self.validate_data('update', data, [self.PARAM_TIMESTAMP, self.PARAM_MASS, self.PARAM_DURATION])

		timestamp = self.get_timestamp(data)
		mass = data.get(self.PARAM_MASS)
		duration = data.get(self.PARAM_DURATION)
		
		conn = get_connection()

		try:
			cur = conn.cursor()
			cur.execute(f'UPDATE {self.TBL_NAME} SET {self.COL_MASS} = ?, {self.COL_DURATION} WHERE {self.COL_ID} = ?;', (mass, duration, timestamp))
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
			cur.execute(f'DELETE FROM {self.TBL_NAME} WHERE {self.COL_ID} = ?;', (timestamp,))
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

class DataAccessError(Exception):
	def __init__(self, message='failed to connect to database'):
		self.message = message

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message