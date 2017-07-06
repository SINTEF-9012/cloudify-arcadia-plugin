import unittest
from os import path
from cloudify.test_utils import workflow_test
from plugin.context import actx


class TestPlugin(unittest.TestCase):

	def setUp(self):
		actx._components = dict()
		actx._relationships = dict()
		actx._service_graph_instance = None
		actx._client = None
		actx._service_graph_tree = None

	@workflow_test(path.join('blueprint', 'blueprint.yaml'),
			resources_to_copy=[path.join('blueprint', 'test_plugin.yaml')])
	def test_install_arcadia_workflow_e2e(self, cfy_local):
		cfy_local.execute('install_arcadia', task_retries=0)

		service_graph = actx.client._service_graph_tree
		self.assertTrue(isinstance(service_graph, ServiceGraphElement))
		self.assertTrue(len(service_graph.components) == 2)
		self.assertTrue(len(service_graph.policies) == 1)

		def find_component(array, component):
			for comp in array:
				if comp._instance._node_instance['name'] == component:
					return comp
		return

		mysql_comp = find_component(service_graph.components, 'mysql')
		wp_comp = find_component(service_graph.components, 'wordpress')
		self.assertTrue(mysql_comp)
		self.assertTrue(wp_comp)
		self.assertTrue(len(wp_comp.dependencies) == 1)
		self.assertTrue(wp_comp.dependencies[0].target._instance == mysql_comp._instance)

		cepcid = mysql_comp._instance._node_instance.runtime_properties.get('cepcid')
		ecepid = mysql_comp._instance._node_instance.runtime_properties.get('ecepid')
		self.assertTrue(cepcid == 'mysqltcp_cepcid')
		self.assertTrue(ecepid == 'mysqltcp')

		cepcid = wp_comp._instance._node_instance.runtime_properties.get('cepcid')
		ecepid = wp_comp._instance._node_instance.runtime_properties.get('ecepid')
		self.assertIsNone(cepcid)
		self.assertIsNone(ecepid)