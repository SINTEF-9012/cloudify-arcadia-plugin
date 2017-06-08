import collections


class NodeInstanceMock(dict):
	
	def __init__(self, node_instance):
		self.update(node_instance)

	@property
	def id(self):
		return self.get('id')

	@property
	def runtime_properties(self):
		return self.get('runtime_properties')


class CloudifyWorlkflowNodeInstanceMock(object):

	def __init__(self, *args, **kwargs):
		self._node_instance = kwargs.get('node_instance') \
			if kwargs.get('node_instance') else NodeInstanceMock({'runtime_properties' : {}})

		clist = kwargs.get('_contained_instances')
		self._contained_instances = list(clist) if clist else []

		self._relationship_instances = collections.OrderedDict()

class CloudifyWorkflowRelationshipInstanceMock(object):

	def __init__(self, *args, **kwargs):
		self.node_instance = kwargs.get('node_instance')
		self._relationship_instance = kwargs.get('relationship_instance') \
			if kwargs.get('relationship_instance') else {}