class BaseEnum(object):
	@classmethod
	def values_list(cls):
		return [getattr(cls, a) for a in dir(cls) if not a.startswith('__') and not callable(getattr(cls, a))]

	@classmethod
	def values(cls):
		return {
			a: getattr(cls, a)
			for a in dir(cls) if not a.startswith('__') and not callable(getattr(cls, a))
		}

	@classmethod
	def reverse_values(cls):
		return {
			getattr(cls, a): a
			for a in dir(cls) if not a.startswith('__') and not callable(getattr(cls, a))
		}
