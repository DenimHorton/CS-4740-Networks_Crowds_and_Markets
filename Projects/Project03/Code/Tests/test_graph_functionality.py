import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
from Tools.func_tester import *
from Tools.func_timer import *
import numpy as np
import unittest

testGraphFunctionality=NetWork(grph_nm="TestGraph", jsn_fl_pth='.\\Inputs\\GraphTest03.json')

class TestGraphFunctionality(unittest.TestCase):
    
    def test_graph_name_setter(self):
        # Check that graph names gets set correctly
        self.assertEqual(testGraphFunctionality.graph_name,"Graph--TestGraph")
        # Check setter functionality
        text_graph_name = 'Project Graph Test'
        testGraphFunctionality.setGraphName(text_graph_name)
        self.assertEqual(testGraphFunctionality.graph_name, f"Graph--{text_graph_name}")
        
    def test_row_shochasticy(self):
        for row in testGraphFunctionality.network_np_matrix:
            row_acum = 0
            for col in row:
                row_acum += col
            if row_acum != 1:
                self.fail()             

if __name__ == '__main__':
    unittest.main()