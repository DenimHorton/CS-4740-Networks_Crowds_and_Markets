import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playground import * 
import unittest

testGraph=Graph("TestGraph")

class TestGraphBuilder(unittest.TestCase):
    
    def test_simple_build(self):

        projectGraphLst = [[0.0, 0.9, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.2, 0.1, 0.4, 0.3, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.4, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.1, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0],
                        [0.4, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, 0.8, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0]]
        projectGraphNP=np.array(projectGraphLst)
        testGraph.buildGraphFromJSON('.\\Inputs\\GraphTest01.json')
        comparison = testGraph.network == projectGraphNP
        self.assertTrue(comparison.all())

    def test_graph_name_setter(self):
        # Check that graph names gets set correctly
        self.assertEqual(testGraph.graph_name,"Graph--TestGraph")
        # Check setter functionality
        text_graph_name = 'Project Graph Test'
        testGraph.setGraphName(text_graph_name)
        self.assertEqual(testGraph.graph_name, f"Graph--{text_graph_name}")