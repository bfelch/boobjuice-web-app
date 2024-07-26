import mariadb

from boobjuice.persistence.utils import get_connection, get_query, validate_data
from boobjuice.persistence.utils import DataAccessError, IllegalArgumentError
from datetime import datetime

class PumpedMilk:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_MASS = 'mass'
	PARAM_DURATION = 'duration'

	ISO_STD = '%Y-%m-%d %H:%M'
	ISO_8601 = '%Y-%m-%dT%H:%M'

	def __init__(self):
		conn = get_connection()

		try:
			query = get_query('create_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query)
		except mariadb.Error as e:
			raise DataAccessError(f'Error initializing table: {e}')
		finally:
			conn.close()

	def get(self):
		conn = get_connection()
		results = []

		try:
			query = get_query('select_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query)
			for (timestamp, mass, duration) in cur:
				results.append({'timestamp':timestamp.strftime(self.ISO_STD), 'mass':mass, 'duration':duration})
		except mariadb.Error as e:
			raise DataAccessError(f'Error selecting from database: {e}')
		finally:
			conn.close()

		return results

	def insert(self, data):
		validate_data('pumped_milk.insert', data, [self.PARAM_MASS, self.PARAM_DURATION])

		timestamp = self.get_timestamp(data, optional=True)
		mass = data.get(self.PARAM_MASS)
		duration = data.get(self.PARAM_DURATION)

		if timestamp is None:
			timestamp = datetime.now().strftime(self.ISO_8601)
		
		conn = get_connection()

		try:
			query = get_query('insert_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query, (timestamp, mass, duration))
		except mariadb.Error as e:
			raise DataAccessError(f'Error inserting to database: {e}')
		finally:
			conn.close()

	def update(self, data):
		validate_data('pumped_milk.update', data, [self.PARAM_TIMESTAMP, self.PARAM_MASS, self.PARAM_DURATION])

		timestamp = self.get_timestamp(data)
		mass = data.get(self.PARAM_MASS)
		duration = data.get(self.PARAM_DURATION)
		
		conn = get_connection()

		try:
			query = get_query('update_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query, (mass, duration, timestamp))
		except mariadb.Error as e:
			raise DataAccessError(f'Error updating database: {e}')
		finally:
			conn.close()

	def delete(self, data):
		validate_data('pumped_milk.delete', data, [self.PARAM_TIMESTAMP])
		
		timestamp = self.get_timestamp(data)
		
		conn = get_connection()

		try:
			query = get_query('delete_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query, (timestamp,))
		except mariadb.Error as e:
			raise DataAccessError(f'Error deleting from database: {e}')
		finally:
			conn.close()
	
	def get_timestamp(self, data, optional=False):
		if optional and self.PARAM_TIMESTAMP not in data:
			return None
		
		if optional and data.get(self.PARAM_TIMESTAMP) is None:
			return None
		
		try:
			timestamp = data.get(self.PARAM_TIMESTAMP)
			if timestamp is None:
				raise Exception
		except:
			raise IllegalArgumentError('timestamp is required')
		
		try:
			return datetime.strptime(timestamp, self.ISO_8601)
		except ValueError:
			print(timestamp)
			raise IllegalArgumentError('invalid timestamp format')