import pytest

from datetime import datetime

from boobjuice.utils import date_utils

def test_datetime_from_timestamp_none():
	dt = date_utils.datetime_from_timestamp(None)

	assert dt is None

def test_datetime_from_timestamp_invalid():
	timestamp = '2024-08-32T17:36'
	dt = date_utils.datetime_from_timestamp(timestamp)

	assert dt is None

def test_datetime_from_timestamp_valid():
	timestamp = '2024-08-07T17:36'
	dt = date_utils.datetime_from_timestamp(timestamp)

	assert dt == datetime(2024, 8, 7, 17, 36)

def test_timestamp_from_datetime_none():
	timestamp = date_utils.timestamp_from_datetime(None)

	assert timestamp is None

def test_timestamp_from_datetime_valid():
	dt = datetime(2024, 8, 7, 17, 36)
	timestamp = date_utils.timestamp_from_datetime(dt)

	assert timestamp == '2024-08-07T17:36'

def test_convert_timestamp_none():
	assert date_utils.convert_timestamp(None) is None

def test_convert_timestamp_invalid():
	timestamp = date_utils.convert_timestamp('2024-08-32T17:36')

	assert timestamp is None

def test_convert_timestamp_valid():
	timestamp = date_utils.convert_timestamp('2024-08-07T17:36', date_utils.ISO_STD)

	assert timestamp == '2024-08-07 17:36'