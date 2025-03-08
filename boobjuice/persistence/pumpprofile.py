import mariadb

from boobjuice.persistence.utils import get_connection, get_query, validate_data
from boobjuice.persistence.utils import DataAccessError

class PumpProfile:

	PARAM_ID = 'id'
	PARAM_NAME = 'name'
	PARAM_DESCRIPTION = 'description'
	PARAM_COLOR = 'color'

	def __init__(self) -> None:
		conn = get_connection()

		try:
			query = get_query('create_profile.txt')

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
			query = get_query('select_profiles.txt')

			cur = conn.cursor()
			cur.execute(query)
			for (id, name, description, color) in cur:
				results.append({'id':id, 'name':name, 'description':description, 'color':color})
		except mariadb.Error as e:
			raise DataAccessError(f'Error selecting from database: {e}')
		finally:
			conn.close()

		return results

	def insert(self, data:dict) -> None:
		validate_data('profile.insert', data, [self.PARAM_NAME])

		name = data.get(self.PARAM_NAME)
		description = data.get(self.PARAM_DESCRIPTION)
		color = data.get(self.PARAM_COLOR)
		
		conn = get_connection()

		try:
			query = get_query('insert_profile.txt')

			cur = conn.cursor()
			cur.execute(query, (name, description, color))
		except mariadb.Error as e:
			raise DataAccessError(f'Error inserting to database: {e}')
		finally:
			conn.close()

	def update(self, data:dict) -> None:
		validate_data('profile.update', data, [self.PARAM_ID, self.PARAM_NAME])

		id = data.get(self.PARAM_ID)
		name = data.get(self.PARAM_NAME)
		description = data.get(self.PARAM_DESCRIPTION)
		color = data.get(self.PARAM_COLOR)
		
		conn = get_connection()

		try:
			query = get_query('update_profile.txt')

			cur = conn.cursor()
			cur.execute(query, (name, description, color, id))
		except mariadb.Error as e:
			raise DataAccessError(f'Error updating database: {e}')
		finally:
			conn.close()

	def delete(self, data:dict) -> None:
		validate_data('profile.delete', data, [self.PARAM_ID])
		
		id = data.get(self.PARAM_ID)
		
		conn = get_connection()

		try:
			query = get_query('delete_profile.txt')

			cur = conn.cursor()
			cur.execute(query, (id,))
		except mariadb.Error as e:
			raise DataAccessError(f'Error deleting from database: {e}')
		finally:
			conn.close()