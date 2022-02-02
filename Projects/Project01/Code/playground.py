import random
from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import time
from logger import Logger
import datetime
import os 

os.path.join("./")

log = Logger()

def timer(func):
    def timerwrapper(*args, **kwargs):
        time_strt = time.time()
        time_stp = time.time()
        log.trace(f"[Execute Start:\t\t{time.gmtime(time_strt).tm_hour}:{time.gmtime(time_strt).tm_min}:{time.gmtime(time_strt).tm_sec}]\n")
        log.trace(f"[Execute Start:\t\t{time.gmtime(time_stp).tm_hour}:{time.gmtime(time_stp).tm_min}:{time.gmtime(time_stp).tm_sec}]\n")
        log.trace(f"[Overall Execution: {(time_stp - time_strt) / 60 :3.5} (Mins)]\n".format())
        return None
    return timerwrapper

@timer
def edge_connect_prob():
    edge_weight = random.randint(0, 100)/100
    print(edge_weight)
    if edge_weight >= 0.50:
        return False
    return True


number_of_nodes = 0
number_of_nodes = random.randint(2, 10)
log.trace(f"\tNumber of nodes {number_of_nodes}\n")

set_of_psbl_node_pairs = list(combinations([f"n_{node}" for node in range(0, number_of_nodes)], 2))
# print(set_of_psbl_node_pairs)

G = nx.Graph()

for pair_nodes in set_of_psbl_node_pairs:
    if edge_connect_prob():  
        G.add_edge(pair_nodes[0], pair_nodes[1], weight=1)

for node_pair, neighbor in G.adj.items():
    print(f"{node_pair}:{neighbor}")

nx.draw(G, pos=nx.circular_layout(G, scale=1, center=None, dim=2), with_labels=True, node_size=600, width=2.5, node_shape="8", node_color="#000000", font_color="#FFFFFF")
plt.show()