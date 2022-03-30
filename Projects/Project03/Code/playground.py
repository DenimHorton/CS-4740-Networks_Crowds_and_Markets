import networkx as nx
import unittest

class Graph(nx.Graph):
    def __init__(self, grph_nm=""):
        super().__init__()
        self.graph_name = f"Graph--{grph_nm:03}"

    def __str__(self):
        objStr = f"Grpah with {len(self.nodes)} nodes and {len(self.edges)} edges . . . \n"
        objStr += f"Also here are my Attributes and class methods"
        for i in self.__dict__:
            objStr += f"\t{i}+\n"        
        return objStr

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