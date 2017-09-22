from plugin.srv_graph.graph_element import *
from plugin.abstract.abc_pretty_printer import ABCPrettyPrinter, ABCXMLPrinter
import xml.etree.ElementTree as etree



class DefaultXMLPrinter(ABCXMLPrinter):

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


class ARCADIAXMLPrinter(ABCXMLPrinter):

	def visit_srv_graph(self, service_graph):
		_instance = service_graph.get_instance()
		_node_instance = _instance._node_instance
		etree_sg = etree.Element('ServiceGraph')
		etree_sg.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
		etree_sg.set('xsi:noNamespaceSchemaLocation', 'ArcadiaModellingArtefacts.xsd')

		etree_meta = etree.SubElement(etree_sg, 'DescriptiveSGMetadata')
		etree_sgid = etree.SubElement(etree_meta, 'SGID')
		etree_sgid.text = str(_node_instance.runtime_properties['sgid'])
		etree_name = etree.SubElement(etree_meta, 'SGName')
		etree_name.text = _node_instance.runtime_properties['sgname']
		etree_desc = etree.SubElement(etree_meta, 'SGDescription')
		etree_desc.text = _node_instance.runtime_properties['sgdesc']

		etree_gdesc = etree.SubElement(etree_sg, 'GraphNodeDescriptor')
		for component in service_graph.components:
			etree_gdesc.append(self.visit_srv_graph_comp(component))

		etree_rpolicy = etree.SubElement(etree_sg, 'RuntimePolicyDescriptor')
		for policy in service_graph.policies:
			etree_rpolicy.append(self.visit_srv_graph_policy(policy))
		return etree_sg

	def visit_srv_graph_comp(self, component):
		_instance = component.get_instance()
		_node_instance = _instance._node_instance
		etree_component = etree.Element('GraphNode')
		nid = etree.Element('NID')
		nid.text = str(_node_instance.runtime_properties['nid'])
		cnid = etree.Element('CNID')
		cnid.text = str(_node_instance.runtime_properties['cnid'])
		etree_component.append(nid)
		etree_component.append(cnid)
		for dependency in component.dependencies:
			etree_dep = self.visit_srv_graph_comp_dep(dependency)
			etree_component.append(etree_dep)
		return etree_component

	def visit_srv_graph_policy(self, policy):
		_instance = policy.get_instance()
		_node_instance = _instance._node_instance
		etree_policy = etree.Element('RuntimePolicy')
		etree_rpid = etree.Element('RPID')
		etree_rpid.text = str(_node_instance.runtime_properties['rpid'])
		etree_rname = etree.Element('RPName')
		etree_rname.text = _node_instance.runtime_properties['rpname']

		etree_policy.append(etree_rpid)
		etree_policy.append(etree_rname)
		return etree_policy

	def visit_srv_graph_comp_dep(self, dependency):
		_instance = dependency.get_instance()
		runtime_prop = _instance._relationship_instance['runtime_properties']
		_instance_target = dependency.target.get_instance()
		_node_instance_target = _instance_target._node_instance
		etree_dep = etree.Element('GraphDependency')
		etree_cepcid = etree.Element('CEPCID')
		etree_cepcid.text = _node_instance_target.runtime_properties['cepcid']
		etree_ecepid = etree.Element('ECEPID')
		etree_ecepid.text = _node_instance_target.runtime_properties['ecepid']
		etree_nid = etree.Element('NID')
		etree_nid.text = str(runtime_prop['nid'])

		etree_dep.append(etree_cepcid)
		etree_dep.append(etree_ecepid)
		etree_dep.append(etree_nid)
		return etree_dep

	def visit_component(self, component):
		_instance = component.get_instance()
		_node = _instance._node._node
		etree_component = etree.Element('Component')
		etree_cnid = etree.Element('CNID')
		etree_cnid.text = _node.properties['external_component_id']
		etree_cepcid = etree.Element('CEPCID')
		etree_cepcid.text = _node.properties['component_cepcid']
		etree_ecepid = etree.Element('ECEPID')
		etree_ecepid.text = _node.properties['component_ecepid']
		etree_component.append(etree_cnid)
		etree_component.append(etree_cepcid)
		etree_component.append(etree_ecepid)
		return etree_component