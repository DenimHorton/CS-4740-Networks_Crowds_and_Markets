import sys, os
import numpy as np
import unittest
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
from Tools.func_tester import *
from Tools.func_timer import *

testGraphBuilder=NetWork("TestGraph")

class TestGraphFunctionTimeComplexity(unittest.TestCase):
    @timer
    def test_graph_name_setter(self):
        # Check that graph names gets set correctly
        self.assertEqual(testGraphBuilder.graph_name,"Graph--TestGraph")
        # Check setter functionality
        text_graph_name = 'Project Graph Test'
        testGraphBuilder.setGraphName(text_graph_name)
        self.assertEqual(testGraphBuilder.graph_name, f"Graph--{text_graph_name}")    

if __name__ == '__main__':
    unittest.main()