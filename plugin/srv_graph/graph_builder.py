from plugin.srv_graph.graph_element import ComponentFactoryFacade
from plugin.srv_graph.pretty_printer import DefaultPrettyPrinter


class GraphBuilder(object):
	wrap_comp_type = 'cloudify.arcadia.nodes.WrappedComponent'
	runt_comp_type = 'cloudify.arcadia.nodes.RuntimePolicy'
	conto_rel_type = 'cloudify.arcadia.relationships.connected_to'

	def __init__(self, _comp_factory=None):
		ComponentFactoryFacade.set_factory(_comp_factory)

	def build(self, service_graph):
		dic_elem = {}
		relationships = []
		serv_graph = ComponentFactoryFacade.INSTANCE.create_service_graph(_instance=service_graph)
		dic_elem[service_graph._node_instance['id']] = serv_graph

		for instance in service_graph._contained_instances:
			for key, value in instance._relationship_instances.iteritems():
				#source_id, target_id, relationship_instance
				relationships.append((instance._node_instance['id'], key, value))

			if self.wrap_comp_type in instance._node.type_hierarchy:
				component = ComponentFactoryFacade.INSTANCE.create_component(_instance=instance)
				dic_elem[instance._node_instance['id']] = component
				serv_graph.add_component(component)
			elif self.runt_comp_type in instance._node.type_hierarchy:
				component = ComponentFactoryFacade.INSTANCE.create_policy(_instance=instance)
				dic_elem[instance._node_instance['id']] = component
				serv_graph.add_policy(component)

		for relationship in relationships:
			source_id, target_id, rel_obj = relationship[0], relationship[1], relationship[2]
			if self.conto_rel_type in rel_obj._relationship.type_hierarchy:
				dep_comp = ComponentFactoryFacade.INSTANCE.create_component_dependency(
					_instance=rel_obj, _source=dic_elem[source_id], _target=dic_elem[target_id])
				dic_elem[source_id].add_dependency(dep_comp)

		return serv_graph
