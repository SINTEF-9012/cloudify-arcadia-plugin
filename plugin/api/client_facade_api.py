from plugin.api.rest_api_client import ARCADIARestAPIClient
from plugin.utils.tools import Tools
from plugin.errors.exceptions import ARCADIAServerRequestError


class ARCADIAClientFacade(object):
	
	def __init__(self, *args, **kwargs):
		self._rest_api = ARCADIARestAPIClient()
		self._pretty_printer = ARCADIAPrettyPrinter()

	def create_comp(self, _instance):
		use_external_resource = _instance._node._node.properties['use_external_resource']
		if not use_external_resource:
			node_name = _instance._node_instance['name']
			raise NotImplementedError('cannot create a component (not implemented): '\
				' use_external_resource is set to false for: "' + node_name +'"')

	def config_comp(self, _instance):
		cnid = _instance._node._node.properties['cnid']
		result = self._rest_api.get_component_info(cnid)

		if result['rc'] != 0:
			raise ARCADIAServerRequestError(message = result['message'])

		component = result['response']

		_instance._node_instance.runtime_properties['nid'] = Tools.generate_unique_id(_instance)
		_instance._node_instance.runtime_properties['cnid'] = cnid

		if component.cepcid:
			_instance._node_instance.runtime_properties['cepcid'] = component.cepcid

		if component.ecepid:
			_instance._node_instance.runtime_properties['ecepid'] = component.ecepid

	def create_srv_graph(self, _instance):
		use_external_resource = _instance._node._node.properties['use_external_resource']
		if use_external_resource:
			node_name = _instance._node_instance['name']
			raise NotImplementedError('cannot use existing service graph (not implemented): '\
				'use_external_resource is set to true for: "' + node_name +'"')

	def config_srv_graph(self, _instance):
		#generate this id
		_instance._node_instance.runtime_properties['sgid'] = Tools.generate_unique_id(_instance)
		
		sgname = _instance._node._node.properties['service_graph_name']
		sgdesc = _instance._node._node.properties['service_graph_desc']

		_instance._node_instance.runtime_properties['sgname'] = sgname
		_instance._node_instance.runtime_properties['sgdesc'] = sgdesc

	def create_policy(self, _instance):
		use_external_resource = _instance._node._node.properties['use_external_resource']
		if not use_external_resource:
			node_name = _instance._node_instance['name']
			raise NotImplementedError('cannot create a policy (not implemented): '
				'use_external_resource is set to false for: "' + node_name +'"')

	def config_policy(self, _instance):
		rpid = _instance._node._node.properties['external_runtime_policy_id']
		rpname = _instance._node._node.properties['runtime_policy_name']

 		_instance._node_instance.runtime_properties['rpid'] = rpid
		_instance._node_instance.runtime_properties['rpname'] = rpname

	def preconfig_src_relationship(self, _instance):
		#nid should be generated
		_instance._relationship_instance['runtime_properties'] = {'nid': Tools.generate_unique_id(_instance)}

	def generate_service_graph(self, _service_graph):
		factory = ComponentFactory(self._pretty_printer)
		graph_builder = GraphBuilder(_comp_factory = factory)
 		self._service_graph_tree = graph_builder.build(_service_graph)

	def install_service_graph(self):
		result = self._rest_api.register_service_graph(self._service_graph_tree)

		if result['rc'] != 0:
			raise ARCADIAServerRequestError(message = result['message'])