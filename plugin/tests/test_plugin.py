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

from cloudify.test_utils import workflow_test

from plugin.srv_graph.graph_element import ServiceGraphElement
from plugin.srv_graph.graph_element import ComponentElement
from plugin.srv_graph.graph_element import ComponentDependencyElement

from plugin.srv_graph.pretty_printer import DefaultPrettyPrinter


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


#    @workflow_test(path.join('blueprint', 'blueprint.yaml'),
#                   resources_to_copy=[path.join('blueprint',
#                                                'test_plugin.yaml')])
#    def test_install_arcadia_workflow(self, cfy_local):
#        cfy_local.execute('install_arcadia', task_retries=0)


    def test_pretty_print(self):
        expected_result = 'something'
        default_pretty_printer = DefaultPrettyPrinter()

        service_graph = ServiceGraphElement(default_pretty_printer)
        mysql = ComponentElement(default_pretty_printer)
        wordpress = ComponentElement(default_pretty_printer)

        dependency = ComponentDependencyElement(default_pretty_printer, mysql, wordpress)

        wordpress.add_dependency(dependency)

        service_graph.add_component(mysql)
        service_graph.add_component(wordpress)

        result = service_graph.print_element()

        self.assertEqual(result, expected_result)