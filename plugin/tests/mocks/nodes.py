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

	@property
	def type_hierarchy(self):
		"""
		:return: The type hierarchy of this node.
		:rtype: list
		"""
		return self['type_hierarchy']


class NodeMock(dict):

	def __init__(self, properties):
		self.update(properties)
	
	@property
	def properties(self):
		return self.get('properties')

	@property
	def type_hierarchy(self):
		return self['type_hierarchy']


class CloudifyWorkflowNodeMock(object):

	def __init__(self, node):
		self._node = node

	@property
	def type_hierarchy(self):
		"""The node type hierarchy"""
		return self._node.type_hierarchy


class CloudifyWorlkflowNodeInstanceMock(object):

	def __init__(self, *args, **kwargs):
		self._node_instance = kwargs.get('node_instance') \
			if kwargs.get('node_instance') else NodeInstanceMock({'runtime_properties' : {}})

		clist = kwargs.get('_contained_instances')
		self._contained_instances = list(clist) if clist else []

		self._relationship_instances = collections.OrderedDict()

		properties = dict(kwargs.get('node_properties')) \
			if kwargs.get('node_properties') else dict()

		properties['type_hierarchy'] = list(kwargs.get('type_hierarchy')) \
			if kwargs.get('type_hierarchy') else []

		self._node = kwargs.get('node') if kwargs.get('node') \
											else CloudifyWorkflowNodeMock(NodeMock(properties))


class RelationshipInstanceMock(dict):
	
	def __init__(self, relationship):
		self.update(relationship)


#	@property
#	def type_hierarchy(self):
#		"""
#		:return: The type hierarchy of this node.
#		:rtype: list
#		"""
#		return self['type_hierarchy']


class CloudifyWorkflowRelationshipMock(object):

	def __init__(self, relationship):
		self._relationship = relationship

#	@property
#	def type_hierarchy(self):
#		return self._relationship.type_hierarchy


class CloudifyWorkflowRelationshipInstanceMock(object):

	def __init__(self, *args, **kwargs):
		self.node_instance = kwargs.get('node_instance')
		self._relationship_instance = kwargs.get('relationship_instance') \
			if kwargs.get('relationship_instance') else {}

		self._relationship = kwargs.get('relationship') if kwargs.get('relationship') \
				else CloudifyWorkflowRelationshipMock(RelationshipInstanceMock({}))

		self._relationship._relationship['type_hierarchy'] = list(kwargs.get('type_hierarchy')) \
			if kwargs.get('type_hierarchy') else []