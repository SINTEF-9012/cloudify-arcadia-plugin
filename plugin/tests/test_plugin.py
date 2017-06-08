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

from plugin.srv_graph.pretty_printer import DefaultPrettyPrinter

from plugin.tests.mocks.node import CloudifyWorlkflowNodeInstanceMock
from plugin.tests.mocks.node import CloudifyWorkflowRelationshipInstanceMock


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
        cfy_local.execute('install_arcadia', task_retries=0)


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

        pretty_printer = DefaultPrettyPrinter()
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

        mock_instance = CloudifyWorlkflowNodeInstanceMock()
        mock_instance._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mock_instance._node_instance.runtime_properties['cnid'] = 'mysql_id'
        mock_instance._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
        mock_instance._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

        mock_relationship = CloudifyWorkflowRelationshipInstanceMock(node_instance=mock_instance, 
                                                            mock_relationship={'nid': 'NID'})

        pretty_printer = DefaultPrettyPrinter()
        ComponentFactoryFacade.set_factory(ComponentFactory(pretty_printer))
        mysql_dependency = ComponentFactoryFacade.INSTANCE.create_component_dependency(mock_relationship)

        result = mysql_dependency.print_element()

        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))

    def test_graph_with_dependencies():
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

        mock_wordpress = CloudifyWorlkflowNodeInstanceMock()
        mock_wordpress._node_instance.runtime_properties['nid'] = 'graph_node_wordpress_id'
        mock_wordpress._node_instance.runtime_properties['cnid'] = 'wordpress_id'

        mock_msql = CloudifyWorlkflowNodeInstanceMock()
        mock_msql._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mock_msql._node_instance.runtime_properties['cnid'] = 'mysql_id'
        mock_msql._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
        mock_msql._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

        mock_relationship = CloudifyWorkflowRelationshipInstanceMock(node_instance=mock_msql, 
                                                            mock_relationship={'nid': 'NID'})

        pretty_printer = DefaultPrettyPrinter()
        ComponentFactoryFacade.set_factory(pretty_printer)

        wp_cmp = ComponentFactoryFacade.INSTANCE.create_component(mock_wordpress)
        mysql_dep = ComponentFactoryFacade.INSTANCE.create_component_dependency(mock_relationship)
        wp_cmp.add_dependency(mysql_dep)

        restult = wp_cmp.print_element()

        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))

    def test_complete_service_graph():
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

        mock_wordpress = CloudifyWorlkflowNodeInstanceMock()
        mock_wordpress._node_instance.runtime_properties['nid'] = 'graph_node_wordpress_id'
        mock_wordpress._node_instance.runtime_properties['cnid'] = 'wordpress_id'

        mock_msql = CloudifyWorlkflowNodeInstanceMock()
        mock_msql._node_instance.runtime_properties['nid'] = 'graph_node_mysql_id'
        mock_msql._node_instance.runtime_properties['cnid'] = 'mysql_id'
        mock_msql._node_instance.runtime_properties['cepcid'] = 'mysqltcp_cepcid'
        mock_msql._node_instance.runtime_properties['ecepid'] = 'mysqltcp'

        mock_relationship = CloudifyWorkflowRelationshipInstanceMock(node_instance=mock_msql, 
                                                            mock_relationship={'nid': 'NID'})


        mock_runtime = CloudifyWorlkflowNodeInstanceMock()
        mock_runtime._node_instance.runtime_properties['rpid'] = 'RPID'
        mock_runtime._node_instance.runtime_properties['rpname'] = 'RPName'

        pretty_printer = DefaultPrettyPrinter()
        ComponentFactoryFacade.set_factory(pretty_printer)

        wp_cmp = ComponentFactoryFacade.INSTANCE.create_component(mock_wordpress)
        mysql_dep = ComponentFactoryFacade.INSTANCE.create_component_dependency(mock_relationship)
        wp_cmp.add_dependency(mysql_dep)


        service_graph = ComponentFactoryFacade.INSTANCE.create_service_graph()

        restult = service_graph.print_element()

        self.assertEqual(flatten_str(result), flatten_str(expected_rusult))