
class ARCADIARelationshipAPI(object):

	def __init__(self, client, **kwargs):
		self.client = client

	def preconfig_src_relationship(self, _instance):
		self.client.preconfig_src_relationship(_instance)