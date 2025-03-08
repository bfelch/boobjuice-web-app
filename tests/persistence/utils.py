import mariadb

from typing import Optional

class Connection:
	def __init__(self, error:bool=False, iter_list:list[dict]=None):
		self.error = error
		self.iter_list = iter_list

	def cursor(self):
		if self.error:
			raise mariadb.Error
		return Cursor(self.iter_list)
	
	def close(self):
		pass

class Cursor:
	def __init__(self, iter_list:Optional[list[dict]]=None) -> None:
		self.iter_list = iter_list

	def execute(self, query:str, params:Optional[list]=None) -> None:
		print(query)
		marker_count = query.count('?')
		if params is None:
			assert marker_count == 0
		else:
			assert marker_count == len(params)
	
	def __iter__(self):
		yield self.iter_list