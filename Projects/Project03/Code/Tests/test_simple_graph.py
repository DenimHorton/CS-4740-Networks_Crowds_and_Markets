import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
import numpy as np
import unittest

testGraph=NetWork("TestGraph")

# Graph for simple functionality tests.
simpleGraphLst = [[1, 2, 3],
                  [4, 5, 6],
                  [7, 8, 9]]

tst_lambda_aray = np.array([0.1,0.2,0.3])

class TestGraphBuilder(unittest.TestCase):

    def test_simple_network_np_matrix_build(self):
        projectGraphNP=np.array(simpleGraphLst)
        testGraph.buildGraphFromJSON('.\\Inputs\\GraphTest00.json')
        comparison = testGraph.network_np_matrix == projectGraphNP
        self.assertTrue(comparison.all())

    def test_simple_lambda_setup(self):
        comparison = tst_lambda_aray == testGraph.lambda_opinions
        self.assertTrue(comparison.all())   
        
    def test_simple_graph(self):
        self.assertEqual(3, len(testGraph.nodes))
        self.assertEqual(9, testGraph.number_of_edges())

    # def test_adjancecny_dict(self):
    #     testGraph.buildGraphFromJSON('.\\Inputs\\GraphTest01.json')
    #     adjanc_tst_set = dict()
    #     # for i in testGraph.adjacency():
    #     #     adjanc_tst_set.add(i)
    #     self.assertDictEqual(adjanc_tst_set, projectGraphEdgeDict)

if __name__ == '__main__':
    unittest.main()