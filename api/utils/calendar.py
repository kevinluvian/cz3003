from calendar import timegm


def from_timezone_to_timestamp(timezone_obj):
	return timegm(timezone_obj.timetuple())
