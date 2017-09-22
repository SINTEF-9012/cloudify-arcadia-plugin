from plugin.srv_graph.graph_element import *
from plugin.abstract.abc_pretty_printer import ABCPrettyPrinter
import xml.etree.ElementTree as etree



class DefaultXMLVisitor(ABCPrettyPrinter):

	def output_text(self, node):
		return etree.tostring(node, method='xml')

	def visit_srv_graph(self, service_graph):
		_instance = service_graph.get_instance()
		name = _instance if isinstance(_instance, str) else str(_instance)
		element_tree = etree.Element('service_graph')
		element_tree.text = name
		for component in service_graph.components:
			element_tree.append(self.visit_srv_graph_comp(component))
		return element_tree

	def visit_srv_graph_comp(self, component):
		_instance = component.get_instance()
		name = _instance if isinstance(_instance, str) else str(_instance)
		element_tree = etree.Element('graph_node')
		element_tree.text = name
		for dependency in component.dependencies:
			element_tree.append(self.visit_srv_graph_comp_dep(dependency))
		return element_tree

	def visit_srv_graph_policy(self, policy):
		element_tree = etree.Element('policy')
		return element_tree

	def visit_srv_graph_comp_dep(self, dependency):
		_instance = dependency.source.get_instance() if dependency.source else "Unknown"
		name_source = _instance if isinstance(_instance, str) else str(_instance)
		_instance = dependency.target.get_instance() if dependency.target else "Unknown"
		name_target = _instance if isinstance(_instance, str) else str(_instance)
		name = str(name_source) + "-" + str(name_target)
		element_tree = etree.Element('graph_node_dependency')
		element_tree.text = name
		return element_tree

	def visit_component(self, component):
		element_tree = etree.Element('component')
		return element_tree


class DefaultPrettyPrinter(ABCPrettyPrinter):

	def output_text(self, node):
		pass

	def visit_srv_graph(self, service_graph):
		pass

	def visit_srv_graph_comp(self, component):
		pass

	def visit_srv_graph_policy(self, policy):
		pass

	def visit_srv_graph_comp_dep(self, dependency):
		pass

	def visit_component(self, component):
		pass

	def print_pretty(self, node):
		result = ""
		if isinstance(node, ServiceGraphElement):
			result = self._print_service_graph(node)
		elif isinstance(node, ComponentElement):
			result = self._print_component(node)
		elif isinstance(node, ComponentDependencyElement):
			result = self._print_dependency(node)
		else:
			raise NotImplementedError("unknown node type: " + node)
		return result

	def _print_service_graph(self, service_graph):
		_instance = service_graph.get_instance()
		name = _instance if isinstance(_instance, str) else str(_instance)
		result = "<service_graph> \n" + name + "\n"
		for component in service_graph.components:
			result += self._print_component(component)
		result+="</service_graph>\n"
		return result

	def _print_component(self, component):
		_instance = component.get_instance()
		name = _instance if isinstance(_instance, str) else str(_instance)
		result = " <graph_node>\n " + name + "\n"
		for dependency in component.dependencies:
			result+= self._print_dependency(dependency)
		result += " </graph_node>\n"
		return result

	def _print_dependency(self, dependency):
		_instance = dependency.source.get_instance() if dependency.source else "Unknown"
		name_source = _instance if isinstance(_instance, str) else str(_instance)
		_instance = dependency.target.get_instance() if dependency.target else "Unknown"
		name_target = _instance if isinstance(_instance, str) else str(_instance)
		result = "  <graph_node_dependency>\n  " + \
				str(name_source) + "->" + str(name_target) + "\n"
		result += "  </graph_node_dependency>\n"
		return result


class ARCADIAPrettyPrinter(ABCPrettyPrinter):

	def output_text(self, node):
		pass

	def visit_srv_graph(self, service_graph):
		pass

	def visit_srv_graph_comp(self, component):
		pass

	def visit_srv_graph_policy(self, policy):
		pass

	def visit_srv_graph_comp_dep(self, dependency):
		pass

	def visit_component(self, component):
		pass

	def print_pretty(self, node):
		result = ""
		if isinstance(node, ServiceGraphElement):
			result = self._print_service_graph(node)
		elif isinstance(node, ComponentElement):
			result = self._print_component(node)
		elif isinstance(node, ComponentDependencyElement):
			result = self._print_dependency(node)
		elif isinstance(node, RuntimePolicyElement):
			result = self._print_policy(node)
		else:
			raise NotImplementedError("unknown node type: " + node)
		return result

	def _print_service_graph(self, service_graph):
		_instance = service_graph.get_instance()
		_node_instance = _instance._node_instance

		result = '<?xml version="1.0" encoding="UTF-8"?>\n'
		result += '<ServiceGraph xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ArcadiaModellingArtefacts.xsd">\n'

		result += ' <DescriptiveSGMetadata>\n'
		result += '  <SGID>' + str(_node_instance.runtime_properties['sgid']) + '</SGID>\n'
		result += '  <SGName>' + _node_instance.runtime_properties['sgname'] + '</SGName>\n'
		result += '  <SGDescription>' + _node_instance.runtime_properties['sgdesc'] + '</SGDescription>\n'
		result += ' </DescriptiveSGMetadata>\n'

		result += ' <GraphNodeDescriptor>\n'
		for component in service_graph.components:
			result += self._print_component(component)
		result += ' </GraphNodeDescriptor>\n'

		result += ' <RuntimePolicyDescriptor>\n'
		for policy in service_graph.policies:
			result += self._print_policy(policy)
		result += ' </RuntimePolicyDescriptor>\n'

		result += '</ServiceGraph>\n'
		return result

	def _print_component(self, component):
		_instance = component.get_instance()
		_node_instance = _instance._node_instance
		
		result = '  <GraphNode>\n'
		result += '   <NID>' + str(_node_instance.runtime_properties['nid']) + '</NID>\n'
		result += '   <CNID>' + _node_instance.runtime_properties['cnid'] + '</CNID>\n'
		for dependency in component.dependencies:
			result += self._print_dependency(dependency)
		result += '  </GraphNode>\n'
		return result

	def _print_component_standalone(self, component):
		_instance = component.get_instance()
		_node = _instance._node._node
		result = '<Component>'
		result += '    <CNID>' + _node.properties['external_component_id'] + '</CNID>\n'
		result += '    <CEPCID>' + _node.properties['component_cepcid'] + '</CEPCID>\n'
		result += '    <ECEPID>' + _node.properties['component_ecepid'] + '</ECEPID>\n'
		result += '</Component> \n'
		return result

	def _print_dependency(self, dependency):
		_instance = dependency.get_instance()
		runtime_prop = _instance._relationship_instance['runtime_properties']
		_instance_target = dependency.target.get_instance()
		_node_instance_target = _instance_target._node_instance

		result = '   <GraphDependency>\n'
		result += '    <CEPCID>' + _node_instance_target.runtime_properties['cepcid'] + '</CEPCID>\n'
		result += '    <ECEPID>' + _node_instance_target.runtime_properties['ecepid'] + '</ECEPID>\n'
		result += '    <NID>' + str(runtime_prop['nid']) + '</NID>\n'
		result += '   </GraphDependency>\n'
		return result

	def _print_policy(self, policy):
		_instance = policy.get_instance()
		_node_instance = _instance._node_instance

		result = '  <RuntimePolicy>\n'
		result += '   <RPID>' + str(_node_instance.runtime_properties['rpid']) + '</RPID>\n'
		result += '   <RPName>' + _node_instance.runtime_properties['rpname'] + '</RPName>\n'
		result += '  </RuntimePolicy>\n'
		return result