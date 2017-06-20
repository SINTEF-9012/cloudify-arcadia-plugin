
class ARCADIAPolicyAPI(object):

	def __init__(self, client, **kwargs):
		self.client = client

	def init_policy(self, _instance):
		self.client.create_policy(_instance)
		self.client.config_policy(_instance)