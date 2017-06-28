

class ARCADIAServerRequestError(Exception):

	def __init__(self, message = None, exception = None):
		self.message = message
		self.exception = exception