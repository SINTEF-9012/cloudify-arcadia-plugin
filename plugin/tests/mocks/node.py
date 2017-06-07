

class NodeInstanceMock(dict):
	
	def __init__(self, node_instance):
		self.update(node_instance)

	@property
	def runtime_properties(self):
		return self.get('runtime_properties')


class CloudifyWorlkflowNodeInstanceMock(object):

	def __init__(self, *args, **kwargs):
		self._node_instance = kwargs.get('node_instance') \
			if kwargs.get('node_instance') else NodeInstanceMock({'runtime_properties' : {}})


class CloudifyWorkflowRelationshipInstanceMock(object):

	def __init__(self, *args, **kwargs):
		self.node_instance = kwargs.get('node_instance')
		self._relationship_instance = kwargs.get('relationship_instance') \
			if kwargs.get('relationship_instance') else {}