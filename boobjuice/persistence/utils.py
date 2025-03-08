import mariadb

import os
from typing import Optional

def get_connection() -> mariadb.Connection:
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

def get_query(filename:str) -> str:
	dir = os.path.dirname(__file__)
	return open(os.path.join(dir, 'queries', filename), 'r').read()

def validate_data(method:str, data:Optional[dict], params:list[str]=[]) -> None:
	if data is None:
		raise IllegalArgumentError(f'object is invalid for {method}')
	
	for param in params:
		if data.get(param) is None:
			raise IllegalArgumentError(f'{param} is invalid for {method}')

class DataAccessError(Exception):
	def __init__(self, message='failed to connect to database'):
		self.message = message

class IllegalArgumentError(Exception):
	def __init__(self, message='argument is not valid'):
		self.message = message