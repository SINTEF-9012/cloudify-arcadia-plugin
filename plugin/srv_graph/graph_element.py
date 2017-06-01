

class GraphElement(object):

	def __init__(self, _pretty_printer=None):
		self.pretty_printer = _pretty_printer


	def print_element(self):
		return self.pretty_printer.print_pretty(self)


class ComponentDependencyElement(GraphElement):

	def __init__(self, _pretty_printer=None, _source=None, _target=None):
		super(ComponentDependencyElement, self).__init__(_pretty_printer)
		self.source = _source
		self.target = _target

	def add_source(self, source_node):
		self.source = source_node

	def add_target(self, target_node):
		self.target = target_node


class ComponentElement(GraphElement):

	def __init__(self, _pretty_printer=None, _depenedencies=None):
		super(ComponentElement, self).__init__(_pretty_printer)
		self.dependencies = _depenedencies if _depenedencies != None else []

	def add_dependency(self, component_dependency):
		self.dependencies.append(component_dependency)


class ServiceGraphElement(GraphElement):

	def __init__(self, _pretty_printer=None, _components=None):
		super(ServiceGraphElement, self).__init__(_pretty_printer)
		self.components = _components if _components != None else []

	def add_component(self, component_element):
		self.components.append(component_element)