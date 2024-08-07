import pytest

from datetime import datetime

from tests.persistence.utils import Connection

from boobjuice.persistence import PumpedMilk, DataAccessError, IllegalArgumentError
from boobjuice.utils import ISO_STD, ISO_8601

def mock_init(mocker):
	mocker.patch('boobjuice.persistence.pumpedmilk.PumpedMilk.__init__', return_value=None)

def mock_connection(mocker, error=False, iter_list=None):
	mocker.patch('boobjuice.persistence.pumpedmilk.get_connection', return_value=Connection(error=error, iter_list=iter_list))

def test_init_db_error(mocker):
	mock_connection(mocker, error=True)

	try:
		PumpedMilk()
		pytest.fail('should have failed to init database', pytrace=True)
	except DataAccessError:
		assert True

def test_init_success(mocker):
	mock_connection(mocker)

	try:
		PumpedMilk()
	except DataAccessError:
		pytest.fail('failed to init database', pytrace=True)

def test_get_db_error(mocker):
	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.get()
		pytest.fail('should have failed to get from database', pytrace=True)
	except DataAccessError as e:
		assert 'selecting' in e.message

def test_get_success(mocker):
	pumped_tuple = pumped_milk_tuple('2024-07-25T19:16', 200, 20)

	mock_init(mocker)
	mock_connection(mocker, iter_list=pumped_tuple)

	pumpedMilk = PumpedMilk()

	try:
		pumped_list = pumpedMilk.get()
		assert len(pumped_list) == 1

		pumped_dict = pumped_list[0]
		assert pumped_dict[pumpedMilk.PARAM_TIMESTAMP] == pumped_tuple[0].strftime(ISO_STD)
		assert pumped_dict[pumpedMilk.PARAM_MASS] == pumped_tuple[1]
		assert pumped_dict[pumpedMilk.PARAM_DURATION] == pumped_tuple[2]
	except DataAccessError:
		pytest.fail('failed to get from database', pytrace=True)

def test_insert_missing_mass(mocker):
	pumped_dict = pumped_milk_dict(None, None, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed on insert validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'mass' in e.message

def test_insert_missing_duration(mocker):
	pumped_dict = pumped_milk_dict(None, 200, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed on insert validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'duration' in e.message

def test_insert_db_error(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)

	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.insert(pumped_dict)
		pytest.fail('should have failed to insert to database', pytrace=True)
	except DataAccessError as e:
		assert 'inserting' in e.message

def test_insert_success_no_timestamp(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.insert(pumped_dict)
		assert True
	except IllegalArgumentError as e:
		pytest.fail('failed to insert to database', pytrace=True)

def test_insert_success_with_timestamp(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.insert(pumped_dict)
		assert True
	except IllegalArgumentError as e:
		pytest.fail('failed to insert to database', pytrace=True)

def test_update_missing_timestamp(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'timestamp' in e.message

def test_update_missing_mass(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', None, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'mass' in e.message

def test_update_missing_duration(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'duration' in e.message

def test_update_db_error(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)

	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.update(pumped_dict)
		pytest.fail('should have failed to update database', pytrace=True)
	except DataAccessError as e:
		assert 'updating' in e.message

def test_update_success(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.update(pumped_dict)
		assert True
	except DataAccessError:
		pytest.fail('failed to update database', pytrace=True)

def test_delete_missing_timestamp(mocker):
	pumped_dict = pumped_milk_dict(None, 200, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.delete(pumped_dict)
		pytest.fail('should have failed on delete validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'timestamp' in e.message

def test_delete_db_error(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)

	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.delete(pumped_dict)
		pytest.fail('should have failed to delete from database', pytrace=True)
	except DataAccessError as e:
		assert 'deleting' in e.message

def test_delete_success(mocker):
	pumped_dict = pumped_milk_dict('2024-07-25T19:16', 200, 20)

	mock_init(mocker)
	mock_connection(mocker)

	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.delete(pumped_dict)
		assert True
	except DataAccessError:
		pytest.fail('failed to delete from database', pytrace=True)

def test_get_timestamp_optional_not_in(mocker):
	mock_init(mocker)

	pumpedMilk = PumpedMilk()
	assert pumpedMilk.get_timestamp({}, optional=True) is None

def test_get_timestamp_optional_none(mocker):
	mock_init(mocker)
	
	pumpedMilk = PumpedMilk()
	assert pumpedMilk.get_timestamp({'timestamp':None}, optional=True) is None

def test_get_timestamp_required_not_in(mocker):
	mock_init(mocker)
	
	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.get_timestamp({})
	except IllegalArgumentError as e:
		assert 'required' in e.message

def test_get_timestamp_required_none(mocker):
	mock_init(mocker)
	
	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.get_timestamp({'timestamp':None})
	except IllegalArgumentError as e:
		assert 'required' in e.message

def test_get_timestamp_wrong_format(mocker):
	mock_init(mocker)
	
	pumpedMilk = PumpedMilk()

	try:
		pumpedMilk.get_timestamp({'timestamp':'2024/07/25 19:16'})
	except IllegalArgumentError as e:
		assert 'invalid' in e.message

def test_get_timestamp_success(mocker):
	mock_init(mocker)
	
	pumpedMilk = PumpedMilk()
	timestamp = pumpedMilk.get_timestamp({'timestamp':'2024-07-25T19:16'})
	assert timestamp is not None

def pumped_milk_tuple(timestamp, mass, duration):
	return (datetime.strptime(timestamp, ISO_8601), mass, duration)

def pumped_milk_dict(timestamp, mass, duration):
	return {'timestamp':timestamp, 'mass':mass, 'duration':duration}