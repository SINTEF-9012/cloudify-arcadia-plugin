from abc import ABCMeta
from abc import abstractmethod
#import xml.etree.ElementTree as etree
from lxml import etree


class GraphVisitor(object):

	__metaclass__ = ABCMeta

	@abstractmethod
	def visit_srv_graph(self, service_graph):
		pass

	@abstractmethod
	def visit_srv_graph_comp(self, component):
		pass

	@abstractmethod
	def visit_srv_graph_policy(self, policy):
		pass

	@abstractmethod
	def visit_srv_graph_comp_dep(self, dependency):
		pass

	@abstractmethod
	def visit_component(self, component):
		pass


class ABCPrettyPrinter(GraphVisitor):

	__metaclass__ = ABCMeta

	@abstractmethod
	def output_text(self, node):
		pass


class ABCXMLPrinter(ABCPrettyPrinter):

	__metaclass__ = ABCMeta

	def output_text(self, node):
		return etree.tostring(node, method='xml')