import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
import numpy as np
import unittest

testGraphBuilder=NetWork("TestGraphBuilder")
# Graph from project Figure (link below)
# LINK: Content\Project 3.pdf
projectGraphMatrix = [[0.0, 0.9, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.2, 0.1, 0.4, 0.3, 0.0, 0.0, 0.0, 0.0],
                      [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], 
                      [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.1, 0.0], 
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], 
                      [0.4, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0], 
                      [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
                      [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  
                      [0.0, 0.0, 0.8, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0]]

projectGraphEdgeDict = dict({'q_0': {'q_1': {'weight': 0.9}, 'q_3': {'weight': 0.1}},
                            'q_1': {'q_2': {'weight': 0.2}, 'q_3': {'weight': 0.1}, 'q_4': {'weight': 0.4}, 'q_5': {'weight': 0.3}},
                            'q_2': {'q_5': {'weight': 1.0}},
                            'q_3': {'q_4': {'weight': 1.0}},
                            'q_4': {'q_6': {'weight': 0.9}, 'q_8': {'weight': 0.1}},
                            'q_5': {'q_9': {'weight': 1.0}},
                            'q_6': {'q_0': {'weight': 0.4}, 'q_3': {'weight': 0.2}, 'q_7': {'weight': 0.4}},
                            'q_7': {'q_4': {'weight': 1.0}},
                            'q_8': {'q_7': {'weight': 1.0}},
                            'q_9': {'q_2': {'weight': 0.8}, 'q_4': {'weight': 0.1}, 'q_8': {'weight': 0.1}}})


class TestGraphBuilder(unittest.TestCase):

    def test_graph_name_setter(self):
        # Check that graph names gets set correctly
        self.assertEqual(testGraphBuilder.graph_name,"Graph--TestGraphBuilder")
        # Check setter functionality
        text_graph_name = 'Project Graph Test'
        testGraphBuilder.setGraphName(text_graph_name)
        self.assertEqual(testGraphBuilder.graph_name, f"Graph--{text_graph_name}")
     

if __name__ == '__main__':
    unittest.main()