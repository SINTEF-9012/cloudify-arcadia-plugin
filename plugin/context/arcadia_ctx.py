from plugin.utils.klasses import Singleton

from proxy_tools import proxy


class ARCADIAContext(object):

	__metaclass = Singleton

	def __init__(self):
		self._components = dict()
		self._relationships = dict()
		self._service_graph_instance = None

	@property
	def service_graph(self):
		return self._service_graph_instance

	@service_graph.setter
	def service_graph_setter(self, _instance):
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
