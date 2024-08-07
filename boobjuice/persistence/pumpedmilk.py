import mariadb

from datetime import datetime

from boobjuice.persistence.utils import get_connection, get_query, validate_data
from boobjuice.persistence.utils import DataAccessError, IllegalArgumentError
from boobjuice.utils import date_utils

class PumpedMilk:

	PARAM_TIMESTAMP = 'timestamp'
	PARAM_MASS = 'mass'
	PARAM_DURATION = 'duration'

	def __init__(self) -> None:
		conn = get_connection()

		try:
			query = get_query('create_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query)
		except mariadb.Error as e:
			raise DataAccessError(f'Error initializing table: {e}')
		finally:
			conn.close()

	def get(self) -> list[dict]:
		conn = get_connection()
		results = []

		try:
			query = get_query('select_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query)
			for (timestamp, mass, duration) in cur:
				timestamp = date_utils.timestamp_from_datetime(timestamp, date_utils.ISO_8601)
				results.append({'timestamp':timestamp, 'mass':mass, 'duration':duration})
		except mariadb.Error as e:
			raise DataAccessError(f'Error selecting from database: {e}')
		finally:
			conn.close()

		return results

	def insert(self, data:dict) -> None:
		validate_data('pumped_milk.insert', data, [self.PARAM_MASS, self.PARAM_DURATION])

		timestamp = self.get_timestamp(data, optional=True)
		mass = data.get(self.PARAM_MASS)
		duration = data.get(self.PARAM_DURATION)

		if timestamp is None:
			timestamp = date_utils.current_timestamp(date_utils.ISO_8601)
		
		conn = get_connection()

		try:
			query = get_query('insert_pumped_milk.txt')

			cur = conn.cursor()
			cur.execute(query, (timestamp, mass, duration))
		except mariadb.Error as e:
			raise DataAccessError(f'Error inserting to database: {e}')
		finally:
			conn.close()

	def update(self, data:dict) -> None:
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

	def delete(self, data:dict) -> None:
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
	
	def get_timestamp(self, data:dict, optional:bool=False) -> str:
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
			return date_utils.convert_timestamp(timestamp, date_utils.ISO_8601)
		except ValueError:
			print(timestamp)
			raise IllegalArgumentError('invalid timestamp format')