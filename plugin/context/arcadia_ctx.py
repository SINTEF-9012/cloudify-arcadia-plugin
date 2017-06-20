from plugin.utils.klasses import Singleton

from proxy_tools import proxy


class ARCADIAContext(object):

	__metaclass = Singleton

	def __init__(self):
		self._components = dict()
		self._relationships = dict()
		self._service_graph_instance = None
		self._client = None

	@property
	def client(self):
		if self._client == None:
			raise NotImplementedError('should not be none!')
		return self._client

	@client.setter
	def client(self, _instance):
		self._client = _instance

	@property
	def service_graph(self):
		return self._service_graph_instance

	@service_graph.setter
	def service_graph(self, _instance):
		if not self._service_graph_instance == None:
			raise Exception('service graph is already set, do you have two service graphs?')
		self._service_graph_instance = _instance

	@property
	def components(self):
		return self._components

	@property
	def relationships(self):
		return self._relationships

	def test_component(self, _instance):
		obj_id = id(_instance)
		if not self._components.get(obj_id):
			self._components[obj_id] = _instance
		return obj_id

	def test_relationship(self, _relationship):
		obj_id = id(_relationship)
		if not self._relationships.get(obj_id):
			self._relationships[obj_id] = _relationship
		return obj_id

current_arcadia_context = ARCADIAContext()

@proxy
def actx():
	return current_arcadia_context
