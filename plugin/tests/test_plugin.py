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


from os import path
import unittest
import re

from cloudify.test_utils import workflow_test

from plugin.srv_graph.graph_element import ServiceGraphElement
from plugin.srv_graph.graph_element import ComponentElement
from plugin.srv_graph.graph_element import ComponentDependencyElement
from plugin.srv_graph.graph_element import ComponentFactory
from plugin.srv_graph.graph_element import ComponentFactoryFacade
from plugin.srv_graph.graph_builder import GraphBuilder

from plugin.srv_graph.pretty_printer import DefaultPrettyPrinter
from plugin.srv_graph.pretty_printer import ARCADIAPrettyPrinter

from plugin.tests.mocks.nodes import CloudifyWorlkflowNodeInstanceMock
from plugin.tests.mocks.nodes import CloudifyWorkflowRelationshipInstanceMock

from plugin.context import actx



def flatten_str(string):
    return re.sub('[\n\s\t]', '', string)

class TestPlugin(unittest.TestCase):

#    @workflow_test(path.join('blueprint', 'blueprint.yaml'),
#                   resources_to_copy=[path.join('blueprint',
#                                                'test_plugin.yaml')],
#                   inputs={'test_input': 'new_test_input'})
#    def test_my_task(self, cfy_local):
#        # execute install workflow
#        """#

#        :param cfy_local:
#        """
#        cfy_local.execute('install', task_retries=0)#

#        # extract single node instance
#        instance = cfy_local.storage.get_node_instances()[0]#

#        # assert runtime properties is properly set in node instance
#        self.assertEqual(instance.runtime_properties['some_property'],
#                         'new_test_input')#

#        # assert deployment outputs are ok
#        self.assertDictEqual(cfy_local.outputs(),
#                             {'test_output': 'new_test_input'})#

#    @workflow_test(path.join('blueprint', 'blueprint.yaml'),
#                   resources_to_copy=[path.join('blueprint',
#                                                'test_plugin.yaml')])
#    def test_create_component(self, cfy_local):
#        # execute install workflow
#        """#
#        :param cfy_local:
#        """
#        cfy_local.execute('install', task_retries=0)#
#        # extract single node instance
#        print "!!!! test_create_component"
#        instance = cfy_local.storage.get_node_instances()[0]


    @workflow_test(path.join('blueprint', 'blueprint.yaml'),
                   resources_to_copy=[path.join('blueprint',
                                                'test_plugin.yaml')])
    def test_install_arcadia_workflow(self, cfy_local):
        expected_rusult = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <ServiceGraph xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ArcadiaModellingArtefacts.xsd">
              <DescriptiveSGMetadata>
                <SGID>wordpress_mysql_service_graph_id</SGID>
                <SGName>SimpleWordPressServiceGraph</SGName>
                <SGDescription>SGDescription</SGDescription>
              </DescriptiveSGMetadata>
              <GraphNodeDescriptor>
                <GraphNode>
                  <NID>graph_node_mysql_id</NID>
                  <CNID>mysql_id</CNID>
                </GraphNode>
                <GraphNode>
                    <NID>graph_node_wordpress_id</NID>
                    <CNID>wordpress_id</CNID>
                    <GraphDependency>
                        <CEPCID>mysqltcp_cepcid</CEPCID>
                        <ECEPID>mysqltcp</ECEPID>
                        <NID>NID</NID>
                    </GraphDependency>
                </GraphNode>
              </GraphNodeDescriptor>
              <RuntimePolicyDescriptor>
                <RuntimePolicy>
                  <RPID>RPID</RPID>
                  <RPName>RPName</RPName>
                </RuntimePolicy>
              </RuntimePolicyDescriptor>
            </ServiceGraph>       
        '''

        cfy_local.execute('install_arcadia', 
            task_retries=0,
            parameters={ 'test_mode' : True }, 
            allow_custom_parameters=True)

        factory = ComponentFactory(ARCADIAPrettyPrinter())
        graph_builder = GraphBuilder(_comp_factory = factory)
        service_graph = graph_builder.build(actx.service_graph)

        result = service_graph.print_element()

        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))


    def test_pretty_print(self):
        expected_result = '''
        <service_graph> 
        service_graph
         <graph_node>
         mysql
         </graph_node>
         <graph_node>
         wordpress
          <graph_node_dependency>
          mysql->wordpress
          </graph_node_dependency>
         </graph_node>
        </service_graph>
        '''
        default_pretty_printer = DefaultPrettyPrinter()

        service_graph = ServiceGraphElement(default_pretty_printer, _instance="service_graph")
        mysql = ComponentElement(default_pretty_printer, _instance="mysql")
        wordpress = ComponentElement(default_pretty_printer, _instance="wordpress")

        dependency = ComponentDependencyElement(default_pretty_printer, mysql, wordpress, "wordpress_to_mysql_realationship")

        wordpress.add_dependency(dependency)

        service_graph.add_component(mysql)
        service_graph.add_component(wordpress)

        result = service_graph.print_element()
        self.assertEqual(flatten_str(result), flatten_str(expected_result))


    def test_graph_node_print(self):
        expected_rusult = '''
            <GraphNode>
              <NID>graph_node_mysql_id</NID>
              <CNID>mysql_id</CNID>
            </GraphNode>            
        '''
        mock_instance = CloudifyWorlkflowNodeInstanceMock()
        mock_instance._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mock_instance._node_instance.runtime_properties['cnid'] = 'mysql_id'
        pretty_printer = ARCADIAPrettyPrinter()
        ComponentFactoryFacade.set_factory(ComponentFactory(pretty_printer))
        mysql = ComponentFactoryFacade.INSTANCE.create_component(mock_instance)
        result = mysql.print_element()
        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))


    def test_graph_node_dependency_print(self):
        expected_rusult = '''
            <GraphDependency>
                <CEPCID>mysqltcp_cepcid</CEPCID>
                <ECEPID>mysqltcp</ECEPID>
                <NID>NID</NID>
            </GraphDependency>
        '''

        wrap_comp_type = ['cloudify.nodes.Root', 'cloudify.nodes.SoftwareComponent', 'cloudify.arcadia.nodes.WrappedComponent']

        mock_instance = CloudifyWorlkflowNodeInstanceMock()
        mock_instance._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mock_instance._node_instance.runtime_properties['cnid'] = 'mysql_id'
        mock_instance._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
        mock_instance._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

        con_to_type = ['cloudify.relationships.depends_on', 'cloudify.relationships.connected_to', 
            'cloudify.arcadia.relationships.connected_to', 'wordpress_connected_to_mysql']
        mock_relationship = CloudifyWorkflowRelationshipInstanceMock(node_instance = mock_instance, 
                                                            relationship_instance = {
                                                                'runtime_properties' : {'nid': 'NID'}
                                                            },
                                                            type_hierarchy = con_to_type)
        
        ComponentFactoryFacade.set_factory(ComponentFactory(ARCADIAPrettyPrinter()))

        mysql_cmp = ComponentFactoryFacade.INSTANCE.create_component(_instance = mock_instance)
        mysql_dependency = ComponentFactoryFacade.INSTANCE.create_component_dependency(_instance = mock_relationship, _target = mysql_cmp)

        result = mysql_dependency.print_element()
        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))


    def test_graph_with_dependencies(self):
        expected_rusult = '''
            <GraphNode>
                <NID>graph_node_wordpress_id</NID>
                <CNID>wordpress_id</CNID>
                <GraphDependency>
                    <CEPCID>mysqltcp_cepcid</CEPCID>
                    <ECEPID>mysqltcp</ECEPID>
                    <NID>NID</NID>
                </GraphDependency>
            </GraphNode>
        '''

        wrap_comp_type = ['cloudify.nodes.Root', 'cloudify.nodes.SoftwareComponent', 'cloudify.arcadia.nodes.WrappedComponent']

        mock_wordpress = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type)
        mock_wordpress._node_instance.runtime_properties['nid'] = 'graph_node_wordpress_id'
        mock_wordpress._node_instance.runtime_properties['cnid'] = 'wordpress_id'

        mock_msql = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type)
        mock_msql._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mock_msql._node_instance.runtime_properties['cnid'] = 'mysql_id'
        mock_msql._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
        mock_msql._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

        con_to_type = ['cloudify.relationships.depends_on', 'cloudify.relationships.connected_to', 
            'cloudify.arcadia.relationships.connected_to', 'wordpress_connected_to_mysql']

        mock_relationship = CloudifyWorkflowRelationshipInstanceMock(node_instance = mock_msql, 
                                                            relationship_instance = {
                                                                'runtime_properties' : {'nid': 'NID'}
                                                            },
                                                            type_hierarchy = con_to_type)

        ComponentFactoryFacade.set_factory(ComponentFactory(ARCADIAPrettyPrinter()))
        wp_cmp = ComponentFactoryFacade.INSTANCE.create_component(_instance = mock_wordpress)
        mysql_cmp = ComponentFactoryFacade.INSTANCE.create_component(_instance = mock_msql)

        mysql_dep = ComponentFactoryFacade.INSTANCE.create_component_dependency(_instance = mock_relationship, _source = wp_cmp, _target = mysql_cmp)
        wp_cmp.add_dependency(mysql_dep)

        result = wp_cmp.print_element()
        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))


    def test_complete_service_graph(self):
        expected_rusult = '''
            <?xml version="1.0" encoding="UTF-8"?>
            <ServiceGraph xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="ArcadiaModellingArtefacts.xsd">
              <DescriptiveSGMetadata>
                <SGID>wordpress_mysql_service_graph_id</SGID>
                <SGName>SimpleWordPressServiceGraph</SGName>
                <SGDescription>SGDescription</SGDescription>
              </DescriptiveSGMetadata>
              <GraphNodeDescriptor>
                <GraphNode>
                  <NID>graph_node_mysql_id</NID>
                  <CNID>mysql_id</CNID>
                </GraphNode>
                <GraphNode>
                    <NID>graph_node_wordpress_id</NID>
                    <CNID>wordpress_id</CNID>
                    <GraphDependency>
                        <CEPCID>mysqltcp_cepcid</CEPCID>
                        <ECEPID>mysqltcp</ECEPID>
                        <NID>NID</NID>
                    </GraphDependency>
                </GraphNode>
              </GraphNodeDescriptor>
              <RuntimePolicyDescriptor>
                <RuntimePolicy>
                  <RPID>RPID</RPID>
                  <RPName>RPName</RPName>
                </RuntimePolicy>
              </RuntimePolicyDescriptor>
            </ServiceGraph>       
        '''

        srv_graph_type = ['cloudify.nodes.Root', 'cloudify.arcadia.nodes.ServiceGraph']
        runtime_type = ['cloudify.nodes.Root', 'cloudify.arcadia.nodes.RuntimePolicy']
        wrap_comp_type = ['cloudify.nodes.Root', 'cloudify.nodes.SoftwareComponent', 'cloudify.arcadia.nodes.WrappedComponent']

        sg_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = srv_graph_type)
        sg_mock._node_instance.runtime_properties['sgid'] = 'wordpress_mysql_service_graph_id'
        sg_mock._node_instance.runtime_properties['sgname'] = 'SimpleWordPressServiceGraph'
        sg_mock._node_instance.runtime_properties['sgdesc'] = 'SGDescription'

        wp_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type)
        wp_mock._node_instance.runtime_properties['nid'] = 'graph_node_wordpress_id'
        wp_mock._node_instance.runtime_properties['cnid'] = 'wordpress_id'

        mysql_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type)
        mysql_mock._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mysql_mock._node_instance.runtime_properties['cnid'] = 'mysql_id'
        mysql_mock._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
        mysql_mock._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

        rp_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = runtime_type)
        rp_mock._node_instance.runtime_properties['rpid'] = 'RPID'
        rp_mock._node_instance.runtime_properties['rpname'] = 'RPName'

        sg_mock._contained_instances.append(mysql_mock)
        sg_mock._contained_instances.append(wp_mock)
        sg_mock._contained_instances.append(rp_mock)

        sg_mock._node_instance['id'] = 'service_graph_gm17g6'
        mysql_mock._node_instance['id'] = 'mysql_x1m8sh'
        wp_mock._node_instance['id'] = 'wordpress_k8lr3c'
        rp_mock._node_instance['id'] = 'runtime_policy_7vy2nn'

        con_in_type = ['cloudify.relationships.contained_in', 'cloudify.arcadia.relationships.contained_in']
        con_to_type = ['cloudify.relationships.depends_on', 'cloudify.relationships.connected_to', 
            'cloudify.arcadia.relationships.connected_to', 'wordpress_connected_to_mysql']

        mysql_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(
                                                                        node_instance = sg_mock,
                                                                        type_hierarchy = con_in_type)
        wp_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(
                                                                    node_instance = sg_mock, type_hierarchy = con_in_type)
        wp_mock._relationship_instances['mysql_x1m8sh'] = CloudifyWorkflowRelationshipInstanceMock(
                                                            node_instance = mysql_mock, 
                                                            relationship_instance = {
                                                                'runtime_properties' : {'nid': 'NID'} 
                                                            },
                                                            type_hierarchy = con_to_type)
        rp_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(
                                                                    node_instance = sg_mock,
                                                                    type_hierarchy = con_in_type)

        graph_builder = GraphBuilder(_comp_factory = ComponentFactory(ARCADIAPrettyPrinter()))
        service_graph = graph_builder.build(sg_mock)

        result = service_graph.print_element()

        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))


    def test_service_graph_builder(self):
        srv_graph_type = ['cloudify.nodes.Root', 'cloudify.arcadia.nodes.ServiceGraph']
        runtime_type = ['cloudify.nodes.Root', 'cloudify.arcadia.nodes.RuntimePolicy']
        wrap_comp_type = ['cloudify.nodes.Root', 'cloudify.nodes.SoftwareComponent', 'cloudify.arcadia.nodes.WrappedComponent']
        sg_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = srv_graph_type)
        mysql_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type)
        wp_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = wrap_comp_type)
        rp_mock = CloudifyWorlkflowNodeInstanceMock(type_hierarchy = runtime_type)

        sg_mock._contained_instances.append(wp_mock)
        sg_mock._contained_instances.append(mysql_mock)
        sg_mock._contained_instances.append(rp_mock)

        sg_mock._node_instance['id'] = 'service_graph_gm17g6'
        mysql_mock._node_instance['id'] = 'mysql_x1m8sh'
        wp_mock._node_instance['id'] = 'wordpress_k8lr3c'
        rp_mock._node_instance['id'] = 'runtime_policy_7vy2nn'

        con_to_type = ['cloudify.relationships.depends_on', 'cloudify.relationships.connected_to',
                            'cloudify.arcadia.relationships.connected_to', 'wordpress_connected_to_mysql']
        con_in_type = ['cloudify.relationships.contained_in', 'cloudify.arcadia.relationships.contained_in']

        mysql_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=sg_mock, type_hierarchy=con_in_type)
        wp_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=sg_mock, type_hierarchy=con_in_type)
        wp_mock._relationship_instances['mysql_x1m8sh'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=mysql_mock, type_hierarchy=con_to_type)
        rp_mock._relationship_instances['service_graph_gm17g6'] = CloudifyWorkflowRelationshipInstanceMock(node_instance=sg_mock, type_hierarchy=con_in_type)


        graph_builder = GraphBuilder(_comp_factory = ComponentFactory(ARCADIAPrettyPrinter()))
        service_graph = graph_builder.build(sg_mock)

        self.assertTrue(isinstance(service_graph, ServiceGraphElement))
        self.assertTrue(len(service_graph.components) == 2)
        self.assertTrue(len(service_graph.policies) == 1)

        def find_component(array, component):
            for comp in array:
                if comp._instance == component:
                    return comp
            return

        mysql_comp = find_component(service_graph.components, mysql_mock)
        wp_comp = find_component(service_graph.components, wp_mock)
        self.assertTrue(mysql_comp)
        self.assertTrue(wp_comp)
        self.assertTrue(len(wp_comp.dependencies) == 1)
        self.assertTrue(wp_comp.dependencies[0].target._instance == mysql_mock)
