import pytest

from boobjuice.persistence.utils import validate_data, IllegalArgumentError

def test_validate_data_none():
	try:
		validate_data('test_method', None, None)
		pytest.fail('should have failed on validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'object' in e.message

def test_validate_data_missing():
	try:
		validate_data('test_method', {}, ['param'])
		pytest.fail('should have failed on validation', pytrace=True)
	except IllegalArgumentError as e:
		assert 'param' in e.message

def test_validate_data_success():
	try:
		validate_data('test_method', {'param':'test_param'}, ['param'])
		assert True
	except IllegalArgumentError:
		pytest.fail('should not have failed on validation', pytrace=True)