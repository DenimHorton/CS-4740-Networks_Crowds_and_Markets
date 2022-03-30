import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
import numpy as np
import unittest

testGraph=NetWork("TestGraph")

class TestGraphBuilder(unittest.TestCase):
        
    def test_graph_name_setter(self):
        # Check that graph names gets set correctly
        self.assertEqual(testGraph.graph_name,"Graph--TestGraph")
        # Check setter functionality
        text_graph_name = 'Project Graph Test'
        testGraph.setGraphName(text_graph_name)
        self.assertEqual(testGraph.graph_name, f"Graph--{text_graph_name}")


if __name__ == '__main__':
    unittest.main()