from plugin.srv_graph.pretty_printer import ARCADIAPrettyPrinter

from plugin.srv_graph.graph_element import ComponentFactory
from plugin.srv_graph.graph_element import ComponentFactoryFacade
from plugin.srv_graph.graph_builder import GraphBuilder
from plugin.api.responses import ARCADIACompResponse

from mock import MagicMock


class ARCADIAClientMock(object):
	
	def __init__(self, *args, **kwargs):
		self._service_graph_tree = None
		self._service_graph_printed = None

	def create_comp(self, _instance):
		pass

	def config_comp(self, _instance):
		if _instance._node_instance['name'] == 'mysql':
			#print "!!!!!!!!!!!!!!!!!!!!!"
			#print _instance._node._node.properties['component_jar_path']
			_instance._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
			_instance._node_instance.runtime_properties['cnid'] = 'mysql_id'
			_instance._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
			_instance._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

		if _instance._node_instance['name'] == 'wordpress':
			_instance._node_instance.runtime_properties['nid'] = 'graph_node_wordpress_id'
			_instance._node_instance.runtime_properties['cnid'] = 'wordpress_id'

	def create_srv_graph(self, _instance):
		pass

	def config_srv_graph(self, _instance):
		_instance._node_instance.runtime_properties['sgid'] = 'wordpress_mysql_service_graph_id'
		_instance._node_instance.runtime_properties['sgname'] = 'SimpleWordPressServiceGraph'
		_instance._node_instance.runtime_properties['sgdesc'] = 'SGDescription'

	def create_policy(self, _instance):
		pass

	def config_policy(self, _instance):
 		_instance._node_instance.runtime_properties['rpid'] = 'RPID'
		_instance._node_instance.runtime_properties['rpname'] = 'RPName'

	def preconfig_src_relationship(self, _instance):
		_instance._relationship_instance['runtime_properties'] = {'nid': 'NID'}


	def generate_service_graph(self, _service_graph):
		factory = ComponentFactory(ARCADIAPrettyPrinter())
		graph_builder = GraphBuilder(_comp_factory = factory)
 		self._service_graph_tree = graph_builder.build(_service_graph)

	def install_service_graph(self):
		self._service_graph_printed = self._service_graph_tree.print_element()



class ARCADIARestAPIClientMock(object):
	
	def __init__(self, *args, **kwargs):
		self.fail_request = False

	def get_component_info(self, cnid):
		#simulating a failure call
		if self.fail_request:
			return {'rc' : 1, 'message' : 'failed to request server, wrong params'}

		#simulating a success call
		mock_response = MagicMock(spec=ARCADIACompResponse)
		if cnid == 'graph_node_mysql_id':
			#no
			pass
		elif cnid == 'graph_node_wordpress_id':
			mock_response.cepcid = 'mysqltcp_cepcid'
			mock_response.ecepid = 'mysqltcp'
		
		return {'rc' : 0, 'message' : 'SUCCESS', 'response' : mock_response}


	def register_service_graph(self, service_tree):
		#simulating a failure call
		if self.fail_request:
			return {'rc' : 1, 'message' : 'failed to request server, wrong params'}

		#simulatiing a success call

		return {'rc' : 0, 'message' : 'SUCCESS'}