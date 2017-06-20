
class ARCADIAComponentAPI(object):

	def __init__(self, client, **kwargs):
		self.client = client

	def init_component(self, _instance):
		self.client.create_comp(_instance)
		self.client.config_comp(_instance)