
class ARCADIACompResponse(object):

	def __init__(self, cepcid=None, ecepcid=None):
		self._cepcid = cepcid
		self._ecepid = ecepcid

	@property
	def cepcid(self):
		return self._cepcid

	@property
	def ecepid(self):
		return self._ecepid