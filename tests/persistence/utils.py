import mariadb

class Connection:
	def __init__(self, error=False, iter_list=None):
		self.error = error
		self.iter_list = iter_list

	def cursor(self):
		if self.error:
			raise mariadb.Error
		return Cursor(self.iter_list)
	
	def close(self):
		pass

class Cursor:
	def __init__(self, iter_list=None):
		self.iter_list = iter_list

	def execute(self, query, params=None):
		print(query)
		marker_count = query.count('?')
		if params is None:
			assert marker_count == 0
		else:
			assert marker_count == len(params)
	
	def __iter__(self):
		yield self.iter_list

def mock_init(mocker):
	mocker.patch('boobjuice.persistence.database.PumpedMilk.__init__', return_value=None)

def mock_connection(mocker, error=False, iter_list=None):
	mocker.patch('boobjuice.persistence.database.get_connection', return_value=Connection(error=error, iter_list=iter_list))