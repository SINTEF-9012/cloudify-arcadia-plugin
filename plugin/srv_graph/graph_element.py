from plugin.abstract.abc_graph_elements import ABCGraphElement
from plugin.utils.klasses import Singleton
from plugin.srv_graph.pretty_printer import DefaultXMLVisitor
from plugin.srv_graph.pretty_printer import DefaultPrettyPrinter
from plugin.srv_graph.pretty_printer import ARCADIAPrettyPrinter


class GraphElement(ABCGraphElement):

	def __init__(self, _instance=None):
		self._instance = _instance
		self._allowed_priners = [DefaultXMLVisitor, DefaultPrettyPrinter, ARCADIAPrettyPrinter]

	def accept(self, printer):
		return len(filter(lambda klass: isinstance(printer, klass), self._allowed_priners)) > 0		

	def get_instance(self):
		return self._instance


class ComponentDependencyElement(GraphElement):

	def __init__(self, _source=None, _target=None, _instance=None):
		super(ComponentDependencyElement, self).__init__(_instance)
		self.source = _source
		self.target = _target

	def print_element(self, printer):
		if self.accept(printer):
			element = printer.visit_srv_graph_comp_dep(self)
			return printer.output_text(element)
		return ''

	def add_source(self, source_node):
		self.source = source_node

	def add_target(self, target_node):
		self.target = target_node


class ComponentElement(GraphElement):

	def __init__(self, _dependencies=None, _instance=None):
		super(ComponentElement, self).__init__(_instance)
		self.dependencies = _dependencies if _dependencies != None else []

	def print_element(self, printer):
		if self.accept(printer):
			element = printer.visit_srv_graph_comp(self)
			return printer.output_text(element)
		return ''

	def add_dependency(self, component_dependency):
		self.dependencies.append(component_dependency)


class ServiceGraphElement(GraphElement):

	def __init__(self, _components=None, _policies=None, _instance=None):
		super(ServiceGraphElement, self).__init__(_instance)
		self.components = _components if _components != None else []
		self.policies = _policies if _policies != None else []

	def print_element(self, printer):
		if self.accept(printer):
			element = printer.visit_srv_graph(self)
			return printer.output_text(element)
		return ''

	def add_component(self, component_element):
		self.components.append(component_element)

	def add_policy(self, policy_element):
		self.policies.append(policy_element)


class RuntimePolicyElement(GraphElement):

	def __init__(self, _instance=None):
		super(RuntimePolicyElement, self).__init__(_instance)

	def print_element(self, printer):
		if self.accept(printer):
			element = printer.visit_srv_graph_policy(self)
			return printer.output_text(element)
		return ''

class ComponentFactory(object):

	def create_component(self, _instance=None, _dependencies=None):
		return ComponentElement(_dependencies, _instance)

	def create_component_dependency(self, _instance=None, _source=None, _target=None):
		return ComponentDependencyElement(_source, _target, _instance)

	def create_service_graph(self, _instance=None, _components=None, _policies=None):
		return ServiceGraphElement(_components, _policies, _instance)

	def create_policy(self, _instance=None):
		return RuntimePolicyElement(_instance)



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