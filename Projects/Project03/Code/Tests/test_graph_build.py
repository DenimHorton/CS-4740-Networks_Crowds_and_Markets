import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
import numpy as np
import unittest

testGraph=NetWork("TestGraph")

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

# Graph for simple functionality tests.
simpleGraphLst = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]

        

class TestGraphBuilder(unittest.TestCase):

    def test_simple_network_np_matrix_build(self):
        projectGraphNP=np.array(simpleGraphLst)
        testGraph.buildGraphFromJSON('.\\Inputs\\GraphTest00.json')
        comparison = testGraph.network_np_matrix == projectGraphNP
        self.assertTrue(comparison.all())

    def test_simple_graph(self):
        self.assertEqual(10, len(testGraph.nodes))
        self.assertEqual(19, len(testGraph.edges))

    def test_assignment_network_np_matrix_build(self):
        projectGraphNP=np.array(projectGraphMatrix)
        testGraph.buildGraphFromJSON('.\\Inputs\\GraphTest01.json')
        comparison = testGraph.network_np_matrix == projectGraphNP
        self.assertTrue(comparison.all())    

    def test_project_graph(self):
        self.assertEqual(10, len(testGraph.nodes))
        self.assertEqual(19, len(testGraph.edges)) 

    # def test_adjancecny_dict(self):
    #     testGraph.buildGraphFromJSON('.\\Inputs\\GraphTest01.json')
    #     adjanc_tst_set = dict()
    #     # for i in testGraph.adjacency():
    #     #     adjanc_tst_set.add(i)
    #     self.assertDictEqual(adjanc_tst_set, projectGraphEdgeDict)




if __name__ == '__main__':
    unittest.main()