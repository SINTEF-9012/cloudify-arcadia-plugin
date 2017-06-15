########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.


# ctx is imported and used in operations
from cloudify import ctx
from cloudify.workflows import ctx as wctx

# put the operation decorator on any function that is a task
from cloudify.decorators import operation
from cloudify.decorators import workflow

from plugin.srv_graph.graph_element import ComponentFactoryFacade
from plugin.context import actx
from plugin.api.component import ARCADIAComponentAPI
from plugin.api.relationship import ARCADIARelationshipAPI
from plugin.api.service_graph import ARCADIAServiceGraphAPI



#@operation
#def my_task(some_property, **kwargs):
#    # setting node instance runtime property
#    ctx.instance.runtime_properties['some_property'] = some_property


@operation
def create_component(**kwargs):
	print "!!!!!!!!!!!!!!!! calling create commponent for the instance with " + ctx.instance.id + " and the node" + ctx.node.name
	api = ARCADIAComponentAPI(test_mode=kwargs.get('test_mode'))
	api.create_component(_instance=actx.components[kwargs.get('id')])


@operation
def preconfigure_source(**kwargs):
	print "**************** priconfigure_source"
	api = ARCADIARelationshipAPI(test_mode=kwargs.get('test_mode'))
	api.preconfig_src_relationship(_instance=actx.relationships[kwargs.get('id')])


@workflow
def install_arcadia(operations, **kwargs):
	print "**************** install workflow is initialized ****************"
	graph = wctx.graph_mode()
	send_event_starting_tasks = {}
	send_event_done_tasks = {}
	for node in wctx.nodes:
		for instance in node.instances:
			send_event_starting_tasks[instance.id] = instance.send_event('Starting to run operation')
			send_event_done_tasks[instance.id] = instance.send_event('Done running operation')

	for node in wctx.nodes:
		for instance in node.instances:
			sequence = graph.sequence()
			inst_kwargs = dict() 
			inst_kwargs['id'] = actx.test_component(instance)
			inst_kwargs['test_mode'] = kwargs.get('test_mode')
			sequence.add(
				send_event_starting_tasks[instance.id],
				instance.execute_operation("create", kwargs=inst_kwargs),
				send_event_done_tasks[instance.id])

	for node in wctx.nodes:
		sequence = graph.sequence()
		for instance in node.instances:
			for relationship in instance.relationships:
				rel_kwargs = dict()
				rel_kwargs['id'] = actx.test_relationship(relationship)
				rel_kwargs['test_mode'] = kwargs.get('test_mode')
				sequence.add(
					relationship.execute_source_operation('preconfigure', kwargs=rel_kwargs))

	for node in wctx.nodes:
		for instance in node.instances:
			for rel in instance.relationships:
				instance_starting_task = send_event_starting_tasks.get(instance.id)
				target_done_task = send_event_done_tasks.get(rel.target_id)
				if instance_starting_task and target_done_task:
					graph.add_dependency(instance_starting_task, target_done_task)

	graph.execute()

	api = ARCADIAServiceGraphAPI(test_mode=kwargs.get('test_mode'))
	service_graph_tree = api.generate_service_graph(actx.service_graph)
	api.install_service_graph(service_graph_tree)