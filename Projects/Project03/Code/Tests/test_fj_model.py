import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common.network import NetWork 
from Common.friedkin_johnsen_model import FriedkinJohnsenModel 
from Tools.func_tester import *
from Tools.func_timer import *
import numpy as np
import unittest

testGraphFunctionality=NetWork(grph_nm="TestGraph", jsn_fl_pth='.\\Inputs\\GraphProject00.json')
testFJModelFunctionality = FriedkinJohnsenModel(testGraphFunctionality)

tstMtrxWAddRw = np.array([[0.0,  0.9,  0.0,  0.1,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.2,  0.1,  0.4,  0.3,  0.0,  0.0,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.9,  0.0,  0.1,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0 ],
                          [0.4,  0.0,  0.0,  0.2,  0.0,  0.0,  0.0,  0.4,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  1.0,  0.0,  0.0,  0.0 ],
                          [0.0,  0.0,  0.8,  0.0,  0.1,  0.0,  0.0,  0.0,  0.1,  0.0,  0.0 ],
                          [0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0 ]])

class TestGraphFunctionality(unittest.TestCase):
    
    def test_1_add_node(self):
        testFJModelFunctionality.addNodeToNetwork()
        self.assertEqual(tstMtrxWAddRw.all(), testFJModelFunctionality.network.network_np_matrix.all())
        self.assertSetEqual(set(testFJModelFunctionality.network.nodes), set(['q_1', 'q_3', 'q_2', 'q_4', 'q_5', 'q_6', 'q_8', 'q_9', 'q_7', 'q_11', 'q_10']))

    def test_2_n_size_network(self):
        self.assertEqual(testFJModelFunctionality.n_size, len(testFJModelFunctionality.network.network_np_matrix))

    def test_3_add_edge(self):
        # Test edges for test file 
        tst_edge_set = set([('q_1', 'q_2'), ('q_1', 'q_4'), ('q_2', 'q_3'), ('q_2', 'q_4'), ('q_2', 'q_5'),
                            ('q_2', 'q_6'), ('q_4', 'q_5'), ('q_3', 'q_6'), ('q_5', 'q_7'), ('q_5', 'q_9'),
                            ('q_6', 'q_10'), ('q_7', 'q_1'), ('q_7', 'q_4'), ('q_7', 'q_8'), ('q_9', 'q_8'),
                            ('q_10', 'q_3'), ('q_10', 'q_5'), ('q_10', 'q_9'), ('q_8', 'q_5')])
        # Test is set of exsisting edges checkouts with out added in edge
        self.assertSetEqual(set(testFJModelFunctionality.network.edges), tst_edge_set)
        # Add edge to network from chossen node, 10, to the new node, 11.
        testFJModelFunctionality.addEdgeToNetwork(10, 11)
        # Add edege to test set
        tst_edge_set.add(('q_10', 'q_11'))
        # Check if network has newly added edges
        self.assertSetEqual(set(testFJModelFunctionality.network.edges), tst_edge_set)
        # Intlialze row accumulator
        row_acum = 0
        # Go through each column to add up the value in the row 
        for col in testFJModelFunctionality.network.network_np_matrix[9]:
            row_acum += col
        # If not 1 fail, else the row is substochastic for this row in the network adj. matrix
        if row_acum != 1:
            self.fail() 
        # Adds the edge to test matrix
        tstMtrxWAddRw[9][10] = 0.5
        # Checks to make sure the edge gets added to the actual network adj. matrix.
        self.assertEqual(tstMtrxWAddRw.all(), testFJModelFunctionality.network.network_np_matrix.all())
      

if __name__ == '__main__':
    unittest.main()