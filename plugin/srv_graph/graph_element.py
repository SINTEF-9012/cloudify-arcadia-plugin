from plugin.srv_graph.abstract.abc_graph_elements import ABCGraphElement

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

	def __init__(self, _pretty_printer=None, _depenedencies=None, _instance=None):
		super(ComponentElement, self).__init__(_pretty_printer, _instance)
		self.dependencies = _depenedencies if _depenedencies != None else []

	def add_dependency(self, component_dependency):
		self.dependencies.append(component_dependency)


class ServiceGraphElement(GraphElement):

	def __init__(self, _pretty_printer=None, _components=None, _instance=None):
		super(ServiceGraphElement, self).__init__(_pretty_printer, _instance)
		self.components = _components if _components != None else []

	def add_component(self, component_element):
		self.components.append(component_element)


class ComponentFactory(object):

	def __init__(self, _pretty_printer=None):
		self._pretty_printer = _pretty_printer

	def createComponent(self, _instance=None):
		return ComponentElement(self._pretty_printer, _instance)

	def createComponentDependency(self, _instance=None, _source=None, _target=None):
		return ComponentDependencyElement(self._pretty_printer, _source, _target, _instance)

	def createServiceGraph(self, _instance=None, _components=None):
		return ServiceGraphElement(self,_pretty_printer, _components, _instance)


class Singleton(type):

	_instances = {}

	def __call__(cls, *args, **kwargs):
		if cls not in cls._instances:
			cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

		return cls._instances[cls]

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
