import pytest
import mariadb

from datetime import datetime
from boobjuice.persistence.database import PumpedMilk, DataAccessError, IllegalArgumentError

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

def test_init_db_error(mocker):
	mock_connection(mocker, error=True)

	try:
		pumpedMilk = PumpedMilk()
		pytest.fail('should have failed to init database', pytrace=True)
	except DataAccessError:
		assert True

def test_init_success(mocker):
	mock_connection(mocker)

	global pumpedMilk
	try:
		pumpedMilk = PumpedMilk()
	except DataAccessError:
		pytest.fail('failed to init database', pytrace=True)

def test_get_db_error(mocker):
	mock_connection(mocker, error=True)

	try:
		pumpedMilk.get()
		pytest.fail('should have failed to get from database', pytrace=True)
	except DataAccessError:
		assert True

def test_get_success(mocker):
	pumped_tuple = pumped_milk_tuple('2024-07-25T19:16', 200, 20)
	mock_connection(mocker, iter_list=pumped_tuple)

	try:
		pumped_list = pumpedMilk.get()
		assert len(pumped_list) == 1

		pumped_dict = pumped_list[0]
		assert pumped_dict[pumpedMilk.PARAM_TIMESTAMP] == pumped_tuple[0].strftime(pumpedMilk.ISO_STD)
		assert pumped_dict[pumpedMilk.PARAM_MASS] == pumped_tuple[1]
		assert pumped_dict[pumpedMilk.PARAM_DURATION] == pumped_tuple[2]
	except DataAccessError:
		pytest.fail('failed to get from database', pytrace=True)

def test_insert_missing_mass(mocker):
	pumped_dict = pumped_milk_dict(None, None, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed on insert validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'mass' in e.message

def test_insert_missing_duration(mocker):
	pumped_dict = pumped_milk_dict(None, 200, None)
	mock_connection(mocker)

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed on insert validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'duration' in e.message

def test_insert_db_error(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)
	mock_connection(mocker, error=True)

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed to insert to database', pytrace=True)
	except DataAccessError:
		assert True

def test_insert_success_no_timestamp(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.insert(pumped_dict)
		assert True
	except IllegalArgumentError as e:
		pytest.fail('failed to insert to database', pytrace=True)

def test_insert_success_with_timestamp(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.insert(pumped_dict)
		assert True
	except IllegalArgumentError as e:
		pytest.fail('failed to insert to database', pytrace=True)

def test_update_missing_timestamp(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'timestamp' in e.message

def test_update_missing_mass(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', None, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'mass' in e.message

def test_update_missing_duration(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, None)
	mock_connection(mocker)

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'duration' in e.message

def test_update_db_error(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)
	mock_connection(mocker, error=True)

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed to update database', pytrace=True)
	except DataAccessError:
		assert True

def test_update_success(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.update(pumped_dict)
		assert True
	except DataAccessError:
		pytest.fail('failed to update database', pytrace=True)

def test_delete_missing_timestamp(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.delete(pumped_dict)
		pytest.fail('should have failed on delete validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'timestamp' in e.message

def test_delete_db_error(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)
	mock_connection(mocker, error=True)

	try:
		pumpedMilk.delete(pumped_dict)
		pytest.fail('should have failed to delete from database', pytrace=True)
	except DataAccessError:
		assert True

def test_delete_success(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)
	mock_connection(mocker)

	try:
		pumpedMilk.delete(pumped_dict)
		assert True
	except DataAccessError:
		pytest.fail('failed to delete from database', pytrace=True)

def test_get_timestamp_optional_not_in():
	assert pumpedMilk.get_timestamp({}, optional=True) is None

def test_get_timestamp_optional_none():
	assert pumpedMilk.get_timestamp({'timestamp':None}, optional=True) is None

def test_get_timestamp_required_not_in():
	try:
		pumpedMilk.get_timestamp({})
	except IllegalArgumentError as e:
		assert 'required' in e.message

def test_get_timestamp_required_none():
	try:
		pumpedMilk.get_timestamp({'timestamp':None})
	except IllegalArgumentError as e:
		assert 'required' in e.message

def test_get_timestamp_wrong_format():
	try:
		pumpedMilk.get_timestamp({'timestamp':'2024/07/25 19:16'})
	except IllegalArgumentError as e:
		assert 'invalid' in e.message

def test_get_timestamp_success():
	timestamp = pumpedMilk.get_timestamp({'timestamp':'2024-07-25T19:16'})
	assert timestamp is not None

def mock_connection(mocker, error=False, iter_list=None):
	mocker.patch('boobjuice.persistence.database.get_connection', return_value=Connection(error=error, iter_list=iter_list))

def pumped_milk_tuple(timestamp, mass, duration):
	return (datetime.strptime(timestamp, pumpedMilk.ISO_8601), mass, duration)

def pumped_milk_dict(timestamp, mass, duration):
	return {'timestamp':timestamp, 'mass':mass, 'duration':duration}