from calendar import timegm


def from_timezone_to_timestamp(timezone_obj):
	return timegm(timezone_obj.timetuple())


def format_date_obj(date_obj):
	return date_obj.strftime('%Y-%m-%d')
