from datetime import datetime
from typing import Optional

ISO_STD = '%Y-%m-%d %H:%M'
ISO_8601 = '%Y-%m-%dT%H:%M'

FORMATS = [
	ISO_STD,
	ISO_8601,
]

def current_datetime() -> datetime:
	return datetime.now()

def current_timestamp(format:str=ISO_8601) -> str:
	return timestamp_from_datetime(current_datetime(), format)

def datetime_from_timestamp(timestamp:Optional[str], format:str=ISO_8601) -> datetime:
	if timestamp is None:
		return None
	
	try:
		return datetime.strptime(timestamp, format)
	except ValueError:
		return None

def timestamp_from_datetime(datetime:Optional[datetime], format:str=ISO_8601) -> str:
	if datetime is None:
		return None

	try:
		return datetime.strftime(format)
	except ValueError:
		return None

def convert_timestamp(timestamp:Optional[str], format:str=ISO_8601) -> str:
	if timestamp is None:
		return None

	if datetime_from_timestamp(timestamp, format) is not None:
		return timestamp
	
	datetime = None
	
	for orig_format in FORMATS:
		if format == orig_format:
			continue

		datetime = datetime_from_timestamp(timestamp, orig_format)
		if datetime is not None:
			break
	
	if datetime is not None:
		return timestamp_from_datetime(datetime, format)
	
	return None