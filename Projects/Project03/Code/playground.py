import networkx as nx
import numpy as np
import unittest
import json

class Graph(nx.Graph):
    def __init__(self, grph_nm=""):
        super().__init__()
        self.graph_name = f"Graph--{grph_nm}"
        self.network = np.array

    def __str__(self):
        objStr = f"Grpah with {len(self.nodes)} nodes and {len(self.edges)} edges . . . \n"
        objStr += f"Also here are my Attributes and class methods"
        for i in self.__dict__:
            objStr += f"\t{i}+\n"        
        return objStr
    
    def setGraphName(self, new_grph_nm):
        self.graph_name = f"Graph--{new_grph_nm}"

    def buildGraphFromJSON(self, json_file_path):
        jsonFile = open(json_file_path)
        data = json.load(jsonFile)
        np_lst_rows = []
        for tstGraph in data['TestGraphs']:
            for tstGraphMtrxRow in tstGraph['Matrix']:
                np_lst_rows.append(tstGraphMtrxRow)
        self.network = np.array(np_lst_rows)
        jsonFile.close()

class EndPoint:
    def __init__(self, src_name, dst_name):
        self.src_name = src_name
        self.dst_name = dst_name

    # def start(end_):
    #     self.

class EndPointWorker:
    '''
    '''
    def __init__(self, end_point):
        self.end_point = end_point 
        self.worker_thread = None
        self.running = False

    def start(self):
        self._log('Started thread')




# graph1 = Graph()
# print(graph1)