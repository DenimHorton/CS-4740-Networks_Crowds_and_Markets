import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playground import * 
import unittest

graph1=Graph(1)

class TestGraphBuilder(unittest.TestCase):
    
    def test_simple_build(self):
        print(graph1)
        self.assertEqual(graph1.graph_name,"Graph--001")