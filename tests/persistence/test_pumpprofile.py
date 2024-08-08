import pytest

from tests.persistence.utils import Connection

from boobjuice.persistence import PumpProfile, DataAccessError, IllegalArgumentError

def mock_init(mocker):
	mocker.patch('boobjuice.persistence.pumpprofile.PumpProfile.__init__', return_value=None)

def mock_connection(mocker, error=False, iter_list=None):
	mocker.patch('boobjuice.persistence.pumpprofile.get_connection', return_value=Connection(error=error, iter_list=iter_list))

def test_init_db_error(mocker):
	mock_connection(mocker, error=True)

	try:
		PumpProfile()
		pytest.fail('should have failed to init database', pytrace=True)
	except DataAccessError:
		assert True

def test_init_success(mocker):
	mock_connection(mocker)

	try:
		PumpProfile()
	except DataAccessError:
		pytest.fail('failed to init database', pytrace=True)

def test_get_db_error(mocker):
	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.get()
		pytest.fail('should have failed to get from database', pytrace=True)
	except DataAccessError as e:
		assert 'selecting' in e.message

def test_get_success(mocker):
	profile_tuple = pump_profile_tuple(1, 'profile', None, None)

	mock_init(mocker)
	mock_connection(mocker, iter_list=profile_tuple)

	pumpProfile = PumpProfile()

	try:
		profile_list = pumpProfile.get()
		assert len(profile_list) == 1

		profile_dict = profile_list[0]
		assert profile_dict[pumpProfile.PARAM_ID] == profile_tuple[0]
		assert profile_dict[pumpProfile.PARAM_NAME] == profile_tuple[1]
		assert profile_dict[pumpProfile.PARAM_DESCRIPTION] == profile_tuple[2]
		assert profile_dict[pumpProfile.PARAM_COLOR] == profile_tuple[3]
	except DataAccessError:
		pytest.fail('failed to get from database', pytrace=True)

def test_insert_missing_name(mocker):
	profile_dict = pump_profile_dict(None, None, None, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.insert(profile_dict)
		pytest.fail('should have failed on insert validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'name' in e.message

def test_insert_db_error(mocker):
	profile_dict = pump_profile_dict(None, 'profile', None, None)

	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.insert(profile_dict)
		pytest.fail('should have failed to insert to database', pytrace=True)
	except DataAccessError as e:
		assert 'inserting' in e.message

def test_insert_success(mocker):
	profile_dict = pump_profile_dict(None, 'profile', 'description', 'AAAAAA')

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.insert(profile_dict)
		assert True
	except IllegalArgumentError:
		pytest.fail('failed to insert to database', pytrace=True)

def test_update_missing_id(mocker):
	profile_dict = pump_profile_dict(None, None, None, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.update(profile_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'id' in e.message

def test_update_missing_name(mocker):
	profile_dict = pump_profile_dict(1, None, None, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.update(profile_dict)
		pytest.fail('should have failed on update validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'name' in e.message

def test_update_db_error(mocker):
	profile_dict = pump_profile_dict(1, 'profile', None, None)

	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.update(profile_dict)
		pytest.fail('should have failed to update database', pytrace=True)
	except DataAccessError as e:
		assert 'updating' in e.message

def test_update_success(mocker):
	profile_dict = pump_profile_dict(1, 'profile', None, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.update(profile_dict)
		assert True
	except DataAccessError:
		pytest.fail('failed to update database', pytrace=True)

def test_delete_missing_id(mocker):
	profile_dict = pump_profile_dict(None, None, None, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.delete(profile_dict)
		pytest.fail('should have failed on delete validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'id' in e.message

def test_delete_db_error(mocker):
	profile_dict = pump_profile_dict(1, 'profile', None, None)

	mock_init(mocker)
	mock_connection(mocker, error=True)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.delete(profile_dict)
		pytest.fail('should have failed to delete from database', pytrace=True)
	except DataAccessError as e:
		assert 'deleting' in e.message

def test_delete_success(mocker):
	profile_dict = pump_profile_dict(1, 'profile', None, None)

	mock_init(mocker)
	mock_connection(mocker)

	pumpProfile = PumpProfile()

	try:
		pumpProfile.delete(profile_dict)
		assert True
	except DataAccessError:
		pytest.fail('failed to delete from database', pytrace=True)

def pump_profile_tuple(id, name, description, color):
	return (id, name, description, color)

def pump_profile_dict(id, name, description, color):
	return {'id':id, 'name':name, 'description':description, 'color':color}