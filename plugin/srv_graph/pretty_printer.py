from plugin.srv_graph.graph_element import *
from plugin.srv_graph.abstract import ABCPrettyPrinter


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
		result = "<service_graph> \n" + str(service_graph) + "\n"
		for component in service_graph.components:
			result += self._print_component(component)
		result+="</service_graph>\n"
		return result

	def _print_component(self, component):
		result = " <graph_node>\n " + str(component) + "\n"
		for dependency in component.dependencies:
			result+= self._print_dependency(dependency)
		result += " </graph_node>\n"
		return result

	def _print_dependency(self, dependency):
		result = "  <graph_node_dependency>\n  " + \
				str(dependency.source) + "->" + str(dependency.target) + "\n"
		result += "  </graph_node_dependency>\n"
		return result

