import networkx as nx
import sys, os
import numpy as np
import matplotlib.pyplot as plt
import unittest
import json
import time
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tools.func_tester import *

class NetWork(nx.DiGraph):
    def __init__(self, grph_nm="", jsn_fl_pth='.\\Inputs\\GraphTest00.json'):
        super().__init__()
        self.graph_name = f"Graph--{grph_nm}"
        self.network_np_matrix = np.array
        self.lambda_opnions = np.array
        self.pandas_df = pd.DataFrame
        self.buildGraphFromJSON(jsn_fl_pth)
        # self.buildPandasDF()

    def __str__(self):
        objStr = f"Grpah with {len(self.nodes)} nodes and {len(self.edges)} edges . . . \n"
        objStr += f"Also here are my Attributes and class methods"
        for i in self.__dict__:
            objStr += f"\t{i}+\n"        
        return objStr
    
    def setGraphName(self, new_grph_nm):
        self.graph_name = f"Graph--{new_grph_nm}"

    def buildPandasDF(self):
        found_edges = np.where(self.network_np_matrix!=0.0)
        found_edges_weights = [ self.network_np_matrix[found_edges[0][edge_wght]][found_edges[1][edge_wght]] for edge_wght in range(len(found_edges[0]))]
        self.pandas_df = pd.DataFrame({'STRT': found_edges[0], 'END': found_edges[1], 'WEIGHT': found_edges_weights})        
        return self.pandas_df

    def buildGraphFromJSON(self, json_file_path):
        jsonFile = open(json_file_path)
        data = json.load(jsonFile)
        np_lst_rows = []
        for tstGraph in data['TestGraphs']:
            for tstGraphMtrxRow in tstGraph['Matrix']:
                np_lst_rows.append(tstGraphMtrxRow)
        self.network_np_matrix = np.array(np_lst_rows)
        jsonFile.close()
        self.buildGraphFromNPArray_withForLoop()

    def buildGraphFromNPArray_withForLoop(self):        
        n = len(self.network_np_matrix)
        for row in range(n):
            for col in range(n):
                effect = self.network_np_matrix[row][col]
                if effect != 0.0:
                    self.add_edge(f"q_{row}", f"q_{col}", weight = effect)

    def showNetworkGraph(self, network_graph_title=""):
        # Set tittle of graph
        plt.title(f"{self.graph_name}\n{network_graph_title}")
        # Set graph visual representation attributes.
        nx.draw(self, pos=nx.circular_layout(self, scale=1, center=None, dim=2), 
                                                   with_labels=True, node_size=300, 
                                                   width=2.5, node_shape="8", 
                                                   node_color="#000000", 
                                                   font_color="#FFFFFF")        
        # Show each graph.                    
        plt.show()

    def showNetworkGraphWithLabels(self, network_graph_title=""): 
        # Set tittle of graph
        plt.title(f"{self.graph_name}\n{network_graph_title}")
        labels = {e: self.edges[e]['weight'] for e in self.edges}
        # Set graph visual representation attributes.
        nx.draw_networkx_edge_labels(self, pos=nx.circular_layout(self, scale=1, center=None, dim=2),  edge_labels=labels)      
        # Show each graph.                    
        plt.show()      

    # def buildGraphFromArray_withNPWhere(self, array): 
    '''
    Method takes 5 times as long compared to for loop 
    '''       
    #     found_edges = np.where(self.network_np_matrix!=0.0)
    #     found_edges_loc = zip(found_edges[0], found_edges[1])
    #     for i in found_edges_loc:
    #         print(f"\t{i}:\t{array[i[0]][i[1]]}")
    #         self.add_edge(i[0], i[1], weight = array[i[0]][i[1]])

    # @recursiveMethodTester
    # def buildMatrixFromJSON(self, json_file_path):
    '''
    Proved to be jsut a little bit slower barely made any difference at 5000 recrusive calls
    '''
    #     jsonFile = open(json_file_path)
    #     data = json.load(jsonFile)
    #     np_lst_rows = []
    #     for tstGraph in data['TestGraphs']:
    #         for tstGraphMtrxRow in tstGraph['Matrix']:
    #             np_lst_rows.append(tstGraphMtrxRow)
    #     self.network_np_matrix = np.array(np_lst_rows)
    #     jsonFile.close()
    #     self.buildGraphFromNPArray_withForLoop(self.network_np_matrix)    
  


class EndPointWorker:
    '''
    '''
    def __init__(self, end_point):
        self.end_point = end_point 
        self.worker_thread = None
        self.running = False

    def start(self):
        self._log('Started thread')

class EndPoint:
    def __init__(self, src_name, dst_name):
        self.src_name = src_name
        self.dst_name = dst_name

graph1 = NetWork(grph_nm="Play Ground Graph 01")
print(graph1.pandas_df)

# graph1.showNetworkGraphWithLabels()


for i in graph1.adjacency():
    print(i)

# graph1.showNetworkGraph()

# for i in graph1.edges():
#     print(f"{i}:{graph1.network_np_matrix[i[0]][i[1]]}")
