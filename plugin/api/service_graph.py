
class ARCADIAServiceGraphAPI(object):

	def __init__(self, client, **kwargs):
		self.client = client

	def generate_service_graph(self, _instance):
		pass

	def print_service_graph(self, _instance):
		pass

	def install_service_graph(self, _instance):
		pass

	def init_service_graph(self, _instance):
		self.client.create_srv_graph(_instance)
		self.client.config_srv_graph(_instance)