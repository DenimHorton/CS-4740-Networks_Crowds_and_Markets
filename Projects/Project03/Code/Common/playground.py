import networkx as nx
import sys, os
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from friedkin_johnsen_model import FriedkinJohnsenModel
from network import NetWork
from end_point_worker import EndPointWorker
from end_point import EndPoint

graph1 = NetWork(grph_nm="Play Ground Graph 01", jsn_fl_pth='.\\Inputs\\GraphTest01.json'  )

jfModel = FriedkinJohnsenModel(graph1)



# print(jfModel)

jfModel.performStep()

# graph1.showNetworkGraph()

# for i in graph1.adjacency():
#     print(i)
 

