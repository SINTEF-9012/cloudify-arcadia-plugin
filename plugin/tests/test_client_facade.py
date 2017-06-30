import unittest

from plugin.tests.mocks.nodes import CloudifyWorlkflowNodeInstanceMock
from plugin.tests.mocks.nodes import CloudifyWorkflowRelationshipInstanceMock
from plugin.tests.mocks.client import ARCADIAClientMock
from plugin.tests.mocks.client import ARCADIARestAPIClientMock
from plugin.errors.exceptions import ARCADIAServerRequestError


class TestPlugin(unittest.TestCase):


	def setUp(self):
		srv_graph_type = ['cloudify.nodes.Root', 'cloudify.arcadia.nodes.ServiceGraph']
		runtime_type = ['cloudify.nodes.Root', 'cloudify.arcadia.nodes.RuntimePolicy']
		wrap_comp_type = ['cloudify.nodes.Root', 'cloudify.nodes.SoftwareComponent', 'cloudify.arcadia.nodes.WrappedComponent']

		con_to_type = ['cloudify.relationships.depends_on', 'cloudify.relationships.connected_to',
							'cloudify.arcadia.relationships.connected_to', 'wordpress_connected_to_mysql']
		con_in_type = ['cloudify.relationships.contained_in', 'cloudify.arcadia.relationships.contained_in']

		sg_node_properties = dict()
		sg_node_properties['use_external_resource'] = False
		#sg_node_properties['service_graph_name'] = 'SimpleWordPressServiceGraph'
		#sg_node_properties['service_graph_desc'] = 'SGDescription'

		mysql_node_properteis = dict()
		mysql_node_properteis['use_external_resource'] = True
		#mysql_node_properteis['external_component_id'] = 'graph_node_mysql_id'

		wp_node_properteis = dict()
		wp_node_properteis['use_external_resource'] = True
		#wp_node_properteis['external_component_id'] = 'graph_node_wordpress_id'

		rp_node_properteis = dict()
		rp_node_properteis['use_external_resource'] = True
		#rp_node_properteis['external_runtime_policy_id'] = 'RPID'
		#rp_node_properteis['runtime_policy_name'] = 'RPName'

		self.sg_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = srv_graph_type, node_properties = sg_node_properties)
		self.mysql_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type, node_properties = mysql_node_properteis)
		self.wp_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type, node_properties = wp_node_properteis)
		self.rp_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = runtime_type, node_properties = rp_node_properteis)

		self.sg_mock._contained_instances.append(self.wp_mock)
		self.sg_mock._contained_instances.append(self.mysql_mock)
		self.sg_mock._contained_instances.append(self.rp_mock)

		self.sg_mock._node_instance['id'] = 'service_graph_gm17g6'
		self.mysql_mock._node_instance['id'] = 'mysql_x1m8sh'
		self.wp_mock._node_instance['id'] = 'wordpress_k8lr3c'
		self.rp_mock._node_instance['id'] = 'runtime_policy_7vy2nn'


		self.mysql_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=self.sg_mock, type_hierarchy=con_in_type)
		self.wp_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=self.sg_mock, type_hierarchy=con_in_type)
		self.wp_mock._relationship_instances['mysql_x1m8sh'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=self.mysql_mock, type_hierarchy=con_to_type)
		self.rp_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=self.sg_mock, type_hierarchy=con_in_type)


	def test_client_facade_success(self):
		rest_api_mock = ARCADIARestAPIClientMock()
		rest_api_mock.fail_request = False
		facade = ARCADIAClientFacade(api_client = rest_api_mock)

		try:
			facade.create_comp(mysql_mock)
			facade.config_comp(mysql_mock)

			facade.create_comp(wp_mock)
			facade.config_comp(wp_mock)

			facade.create_policy(rp_mock)
			facade.config_policy(rp_mock)

			facade.create_srv_graph(sg_mock)
			facade.config_srv_graph(sg_mock)

			facade.generate_service_graph(sg_mock)
			facade.install_service_graph()
		except ARCADIAServerRequestError:
			self.assertTrue(False, 'none of the calls should fail')


	def test_client_facade_failed_create_component(self):
		rest_api_mock = ARCADIARestAPIClientMock()
		rest_api_mock.fail_request = True
		facade = ARCADIAClientFacade(api_client = rest_api_mock)

		exception_raised = False
		try:
			facade.create_comp(mysql_mock)
			facade.config_comp(mysql_mock)
		except ARCADIAServerRequestError:
			exception_raised = True

		self.assertTrue(exception_raised, 'exception was not raised!')


	def test_client_facade_failed_submit_graph(self):
		rest_api_mock = ARCADIARestAPIClientMock()
		rest_api_mock.fail_request = False
		facade = ARCADIAClientFacade(api_client = rest_api_mock)

		facade.create_comp(mysql_mock)
		facade.config_comp(mysql_mock)

		facade.create_comp(wp_mock)
		facade.config_comp(wp_mock)

		facade.create_policy(rp_mock)
		facade.config_policy(rp_mock)

		facade.create_srv_graph(sg_mock)
		facade.config_srv_graph(sg_mock)

		rest_api_mock.fail_request = True

		exception_raised = False
		try:
			facade.generate_service_graph(sg_mock)
			facade.install_service_graph()
		except ARCADIAServerRequestError:
			exception_raised = True

		self.assertFalse(exception_raised, 'exception was raised!')