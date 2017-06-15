from plugin.srv_graph.abstract.abc_graph_elements import ABCGraphElement
from plugin.utils.klasses import Singleton

class GraphElement(ABCGraphElement):

	def __init__(self, _pretty_printer=None, _instance=None):
		self.pretty_printer = _pretty_printer
		self._instance = _instance

	def print_element(self):
		return self.pretty_printer.print_pretty(self)

	def get_instance(self):
		return self._instance


class ComponentDependencyElement(GraphElement):

	def __init__(self, _pretty_printer=None, _source=None, _target=None, _instance=None):
		super(ComponentDependencyElement, self).__init__(_pretty_printer, _instance)
		self.source = _source
		self.target = _target

	def add_source(self, source_node):
		self.source = source_node

	def add_target(self, target_node):
		self.target = target_node


class ComponentElement(GraphElement):

	def __init__(self, _pretty_printer=None, _dependencies=None, _instance=None):
		super(ComponentElement, self).__init__(_pretty_printer, _instance)
		self.dependencies = _dependencies if _dependencies != None else []

	def add_dependency(self, component_dependency):
		self.dependencies.append(component_dependency)


class ServiceGraphElement(GraphElement):

	def __init__(self, _pretty_printer=None, _components=None, _policies=None, _instance=None):
		super(ServiceGraphElement, self).__init__(_pretty_printer, _instance)
		self.components = _components if _components != None else []
		self.policies = _policies if _policies != None else []

	def add_component(self, component_element):
		self.components.append(component_element)

	def add_policy(self, policy_element):
		self.policies.append(policy_element)


class RuntimePolicyElement(GraphElement):

	def __init__(self, _pretty_printer=None, _instance=None):
		super(RuntimePolicyElement, self).__init__(_pretty_printer, _instance)


class ComponentFactory(object):

	def __init__(self, _pretty_printer=None):
		self._pretty_printer = _pretty_printer

	def create_component(self, _instance=None, _dependencies=None):
		return ComponentElement(self._pretty_printer, _dependencies, _instance)

	def create_component_dependency(self, _instance=None, _source=None, _target=None):
		return ComponentDependencyElement(self._pretty_printer, _source, _target, _instance)

	def create_service_graph(self, _instance=None, _components=None, _policies=None):
		return ServiceGraphElement(self._pretty_printer, _components, _policies, _instance)

	def create_policy(self, _instance=None):
		return RuntimePolicyElement(self._pretty_printer, _instance)



#component_factory = ComponentFactory()
#ComponentFactoryFacade.setFactory(component_factory)
#ComponentFactoryFacade.INSANCE.createComponentElement()

class ComponentFactoryFacade(object):
	
	__metaclass__ = Singleton

	INSTANCE = None

	def __init__(self, _factory):
		self.INSTANCE = _factory

	@classmethod
	def set_factory(cls, _factory):
		cls.INSTANCE = _factory

