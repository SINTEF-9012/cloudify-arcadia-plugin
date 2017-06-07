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


#@operation
#def my_task(some_property, **kwargs):
#    # setting node instance runtime property
#    ctx.instance.runtime_properties['some_property'] = some_property


@operation
def create_component(**kwargs):
	print "!!!!!!!!!!!!!!!! calling create commponent for the instance with " + ctx.instance.id + " and the node" + ctx.node.name

@operation
def preconfigure_source(**kwargs):
	print "**************** priconfigure_source"

@workflow
def install_arcadia(operations, **kwargs):
	print "**************** install workflow is initialized ****************"
	graph = wctx.graph_mode()
	send_event_starting_tasks = {}
	send_event_done_tasks = {}
	for node in wctx.nodes:
		for instance in node.instances:
			instance._node_instance['runtime_properties']['sometheing'] = "hello"
			send_event_starting_tasks[instance.id] = instance.send_event('Starting to run operation')
			send_event_done_tasks[instance.id] = instance.send_event('Done running operation')

	for node in wctx.nodes:
		for instance in node.instances:
			sequence = graph.sequence()
			sequence.add(
				send_event_starting_tasks[instance.id],
				instance.execute_operation("create", kwargs=None),
				send_event_done_tasks[instance.id])

	for node in wctx.nodes:
		sequence = graph.sequence()
		for instance in node.instances:
			for relationship in instance.relationships:
				relationship._relationship_instance['hdelj'] = 'sdfsfd'
				sequence.add(relationship.execute_source_operation('preconfigure', kwargs=None))

	for node in wctx.nodes:
		for instance in node.instances:
			for rel in instance.relationships:
				instance_starting_task = send_event_starting_tasks.get(instance.id)
				target_done_task = send_event_done_tasks.get(rel.target_id)
				if instance_starting_task and target_done_task:
					graph.add_dependency(instance_starting_task, target_done_task)

	graph.execute()
	create_arcadia_service_graph()

def create_arcadia_service_graph():
	print "creating service grapth"