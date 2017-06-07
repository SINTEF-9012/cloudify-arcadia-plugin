from plugin.srv_graph.graph_element import *
from plugin.srv_graph.abstract.abc_pretty_printer import ABCPrettyPrinter


class DefaultPrettyPrinter(ABCPrettyPrinter):

	def print_pretty(self, node):
		result = ""
		if type(node) is ServiceGraphElement:
			result = self._print_service_graph(node)
		elif type(node) is ComponentElement:
			result = self._print_component(node)
		elif type(node) is ComponentDependencyElement:
			result = self._print_dependency(node)
		else:
			raise NotImplementedError("unknown node type: " + node)
		return result

	def _print_service_graph(self, service_graph):
		_instance = service_graph.get_instance()
		name = _instance if type(_instance) == str else str(_instance)
		result = "<service_graph> \n" + name + "\n"
		for component in service_graph.components:
			result += self._print_component(component)
		result+="</service_graph>\n"
		return result

	def _print_component(self, component):
		_instance = component.get_instance()
		name = _instance if type(_instance) == str else str(_instance)
		result = " <graph_node>\n " + name + "\n"
		for dependency in component.dependencies:
			result+= self._print_dependency(dependency)
		result += " </graph_node>\n"
		return result

	def _print_dependency(self, dependency):
		_instance = dependency.source.get_instance() if dependency.source else "Unknown"
		name_source = _instance if type(_instance) == str else str(_instance)
		_instance = dependency.target.get_instance() if dependency.target else "Unknown"
		name_target = _instance if type(_instance) == str else str(_instance)
		result = "  <graph_node_dependency>\n  " + \
				str(name_source) + "->" + str(name_target) + "\n"
		result += "  </graph_node_dependency>\n"
		return result

