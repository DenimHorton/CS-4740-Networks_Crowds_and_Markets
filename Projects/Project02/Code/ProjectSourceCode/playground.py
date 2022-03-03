import logging
from re import X
from black import format_file_contents
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import math, random, time, logging, json, glob, os
from matplotlib.animation import FuncAnimation
from alive_progress import alive_bar
 
logging.basicConfig(filename='Content\\LogInfo\\logInfo.log', filemode='w', level=logging.INFO)
logging = logging.getLogger('alive_progress')

team_map = {0:"Empty Space", 1:"Red Residence", -1:"Blue Residence"}

files = glob.glob('./Content/**/*.png', recursive=True)


for f in files:
    try:
        os.remove(f)
    except OSError as e:
        print("Error: %s : %s" % (f, e.strerror))

class GraphGenerator(object):
    def __init__(self, t=0.5, os=0.5, mxd=0.5, g_size=20, grph_ind_num="TestDefault", num_iter = 100):
        self.graph_instance_name = f"Graph-{grph_ind_num}"
        self.graph = np.array
        self.graph_size = g_size * g_size
        self.t_value = t
        self.open_spots = os  
        self.red_blue_split = mxd
        self.runtime = 0.0
        self.num_of_iterations = num_iter
        self.iter_tracker = dict([(i, 0) for i in range(0, self.num_of_iterations)])

    def __str__(self):
        obj_str = f"----------- {self.graph_instance_name} -----------\n"
        obj_str += f"Graph size:\t\t\t\t{self.red_blue_split}\n"
        obj_str += f"Graph Mixed Residence Percentage:\t{self.red_blue_split}\n"
        obj_str += f"Graph Open Spot Percentage:\t\t{self.open_spots}\n"  
        obj_str += f"Graph \'t-value:\':\t\t\t{self.t_value}\n"
        obj_str += f"Runtime:\t\t\t\t{self.runtime}\n"
        obj_str += f"Graph:\n{self.graph}"
        return obj_str 

    def showGraph(self, iter=0):
        plt.matshow(self.graph, cmap='seismic')
        plt.title(f"{self.graph_instance_name}-{iter:03}")
        plt.show()
        plt.close()

    def saveGraph(self, iter=0):
        plt.matshow(self.graph, cmap='seismic')
        plt.title(f"{self.graph_instance_name}-{iter:03}")
        plt.savefig(f".\\Content\\GenoratedGraphs\\{self.graph_instance_name}-{iter:03}.png")
        plt.close()


    def setGraphName(self, new_name):
        self.graph_instance_name = f"Graph-{new_name}"

    def createGraph(self):
        number_of_residence = self.graph_size - int(self.graph_size * self.open_spots)
        red_residence = int(number_of_residence * self.red_blue_split)
        blue_residence = number_of_residence - red_residence 

        temp_arry_lst = []

        for red_res in range(0, red_residence):
            temp_arry_lst.append(1) 
        for blu_res in range(0, blue_residence):
            temp_arry_lst.append(-1)
        for open_res in range(0, self.graph_size - number_of_residence):
            temp_arry_lst.append(0)
        
        random.shuffle(temp_arry_lst)
        
        generated_graph = np.array(temp_arry_lst).reshape(int(math.sqrt(self.graph_size)), int(math.sqrt(self.graph_size)))  
        
        self.graph=generated_graph

    def isContent(self, indx_row, indx_col, verbosity=False):
        if verbosity:
            logging.info(f"  Checking if this residence is content . . .")

        blue_counter, red_counter, open_counter = self.getNeighborCount(indx_row, indx_col, verbosity=verbosity)
        num_local_neghbors = (8 - open_counter)

        # Has only open spots around it.
        if num_local_neghbors == 0:
            return True, 0.0
        elif (self.graph[indx_row][indx_col] == 1 ) and (blue_counter / num_local_neghbors  < self.t_value):
            return True, blue_counter / num_local_neghbors 

        elif (self.graph[indx_row][indx_col] == -1 ) and (blue_counter / num_local_neghbors  < self.t_value):
            return True, blue_counter / num_local_neghbors

        elif (self.graph[indx_row][indx_col] == 1 ) and (blue_counter / num_local_neghbors  >= self.t_value):
            return False, blue_counter / num_local_neghbors 
            
        elif (self.graph[indx_row][indx_col] == -1 ) and (red_counter / num_local_neghbors  >= self.t_value):
            return False, red_counter / num_local_neghbors 
        # Evaluating open spot which will be content because its an open spot . . . 
        else:
            return True,  1.0


    def getNeighborCount(self, indx_row, indx_col, verbosity=False):

        sub_arry_lst = []
        
        for col in range(indx_col-1, indx_col+2):
            for row in range(indx_row-1, indx_row+2):
                try:
                    sub_arry_lst.append(str(self.graph[row][col]))
                except IndexError:
                    if verbosity:
                        logging.warning(f"\t\tIndex:({row}, {col}) is out of bounds.")
                    sub_arry_lst.append("N/A")
        sub_arry_lst[4] = "R"

        blue_counter = sub_arry_lst.count("-1")
        red_counter = sub_arry_lst.count("1")
        open_counter = sub_arry_lst.count("0")

        if verbosity:
            # This takes the local neighborhood of an array 3 x 3 where the 
            # index (row and coloumn) are passed as the middle residence.
            local_neighborhood = np.array(sub_arry_lst).reshape((3, 3))
            # local_neighborhood[1][1] = "R"
            team = self.graph[indx_row][indx_col]
            logging.info(f"\t{team_map.get(team)}:\t({indx_row}, {indx_col})")
            logging.info(f"\t{local_neighborhood[0]}")
            logging.info(f"\t{local_neighborhood[1]}")
            logging.info(f"\t{local_neighborhood[2]}")
            logging.info(f"\t\tRed Counter:\t{red_counter}")
            logging.info(f"\t\tBlue Counter:\t{blue_counter}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  ")  

        return blue_counter, red_counter, open_counter

    def runSchellingSegregation(self, verbosity=False, fname="./Content/test.json"):
        temp_graph = self.graph.copy()   
        t1 = time.time()
        iter = 0
        graph_ctf = 0.0

        with alive_bar(self.num_of_iterations, bar='solid', title=f'{self.graph_instance_name}') as bar:
            for iter in range(0, self.num_of_iterations):
                if graph_ctf >= 1.0:
                    logging.info(f"Homophily! Segregation achived: {graph_ctf}")
                    print(f"\t{self.graph_instance_name}: {graph_ctf}")
                    self.saveGraph(iter)
                    break
                if iter % (self.num_of_iterations / 5) == 0:
                    print(f"\t{self.graph_instance_name}: {graph_ctf}")
                    logging.info(f"\tIteration {iter:>3} : CTF : {graph_ctf:0.4f}")
                    self.saveGraph(iter)

                for row in range(0, len(self.graph[0])):
                    for col in range(0, len(self.graph[row])):
    
                        if verbosity:
                            logging.info(f" Graph neighbor {team_map.get(self.graph[row][col]):>3} @ ({row}, {col})")

                        content_or_not, contentdeness = self.isContent(row, col)
                        if content_or_not:
                            if verbosity:
                                logging.info(f"\tContent! (%{contentdeness:0.2})")
                        else:
                            posible_new_streets = np.where(self.graph==0)
                            posible_new_address = tuple(zip(posible_new_streets[0], posible_new_streets[1]))
                            random_new_space = random.choice(posible_new_address)
                            if verbosity:
                                logging.warning("\tDiscontent! (%{contentdeness:0.2})")
                                logging.warning(f"\tPossible New Address':\t\t{posible_new_address}")
                                logging.warning(f"\tCONGRATIONLATIONS {team_map.get(self.graph[row][col])}!! YOUR MOVING TO YOUR NEW HOME which is at ({random_new_space[0]}, {random_new_space[1]}). Moving into {team_map.get(self.graph[random_new_space[0]][random_new_space[1]])} ")
                                 
                            self.graph[random_new_space[0]][random_new_space[1]] = self.graph[row][col]
                            self.graph[row][col] = 0

                graph_ctf =  self.calculateCTF(verbosity=verbosity)
                self.iter_tracker[iter] = graph_ctf
               
                bar()
                            
            t2 = time.time()
            self.runtime = t2 - t1 
            self.showGraph(iter=iter)
            logging.info(f"\t{self.graph_instance_name}: {graph_ctf}")    
            self.graph = temp_graph

    def calculateCTF(self, verbosity=False):

        total_neighbors = 0
        total_cross_neighbors = 0
        
        if verbosity:
            logging.info(f" Calculating CTF . . . ")

        for street in range(0, len(self.graph)):
            for residence in range(0, len(self.graph[street])):
                blu_neighbors, red_neighbors, open_neighbors = self.getNeighborCount(street, residence, verbosity=verbosity)
                total_neighbors += (blu_neighbors + red_neighbors)
                if self.graph[street][residence] == 1:
                    total_cross_neighbors += red_neighbors
                elif self.graph[street][residence] == -1:
                    total_cross_neighbors += blu_neighbors

        ctf = total_cross_neighbors / total_neighbors
        if verbosity:
            logging.info(f"\tCTF:\t{ctf}")
        return ctf


def PlotGraphCTFOverIter(graph_iter_lst, number_iters, verbosity=False):
    # print(Graph)
    plt.plot(graph_iter_lst.keys(), graph_iter_lst.values())
    x_vals_lst = [x_tick_val for x_tick_val in range(0, number_iters)]
    y_vals_lst = [y_tick_val for y_tick_val in np.linspace(min(graph_iter_lst.values()), max(graph_iter_lst.values()), 10)]
    plt.xlabel('Iterations')
    plt.ylabel('CTF')
    plt.xticks(x_vals_lst)
    plt.yticks(y_vals_lst)
    plt.title(f'Popullation Schelling Segregation\nAverage CTF Over ({len(graph_iter_lst.keys())}) Iterations')
    plt.show()
    
def PlotAvgGraphCTFOverIter(Graph, amount_episodes=3, verbosity=False):
    graph_agv_acum_dict = dict([(i, j) for i, j in Graph.iter_tracker.items()]) 
    for episode in range(0, amount_episodes):

        # Test Schelling Segregation 
        Graph.setGraphName(f" AvgTestsRun-{episode:03}")
        # Graph.runSchellingSegregationAtRandom(verbosity=verbosity)
        Graph.runSchellingSegregation(verbosity=verbosity)


        [graph_agv_acum_dict.update({i : j + Graph.iter_tracker.get(i)}) for i, j in graph_agv_acum_dict.items()]
        
        logging.info(f"\tAverage Run Reults {amount_episodes}:{graph_agv_acum_dict}")
    
    [graph_agv_acum_dict.update({i : j / amount_episodes}) for i, j in graph_agv_acum_dict.items()]

    PlotGraphCTFOverIter(graph_agv_acum_dict, Graph.num_of_iterations, verbosity=True)


'''
Test showing graphing functionality
'''
# GLOBAL number of tst to run for each configuration to calculate avg.
TST_GRAPH_RUNS = 3

# Quickly shows what works and how through log statments when verbose is turned to 'True'.
# We only run for 10 iterations with modest values to give multiple logical branch offs
# and to show overall functionality.
logging.info(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
logging.info(f"- - - - - - - - - - - - - -  - - Test Proof Of Concept - - - - - - - - - - - - - - - - -") 
logging.info(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ") 
tstGraph = GraphGenerator(g_size=5, t=0.1, os=0.2, mxd=0.5, num_iter=15)
tstGraph.createGraph()
# Test Schelling Segregation 
tstGraph.runSchellingSegregation(verbosity=True)
logging.info(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ")
logging.info(f"- - - - - - - - - - - - - Average Test Run (Limited Verbosity) - - - - - - - - - - - - -") 
logging.info(f"- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ") 
avgTstGraph = GraphGenerator(g_size=50, t=0.3, os=0.1, mxd=0.3, num_iter=100)
avgTstGraph.createGraph()

PlotAvgGraphCTFOverIter(avgTstGraph, amount_episodes=1, verbosity=False)













    # def chooseRandomSpot(self):
    #     while True:
    #         x =  random.choice([i for i in range(0, int(math.sqrt(self.graph_size)))])
    #         y =  random.choice([i for i in range(0, int(math.sqrt(self.graph_size)))])
    #         if self.graph[x][y] != 0:
    #             break
    #     return x, y
    # 
    # def chooserandomResidence(self):
    #     psbl_nw_adrs = np.where(self.graph != 0)
    #     psbl_nw_lst_set = [(psbl_nw_adrs[0][i], psbl_nw_adrs[1][i])for i in range(0, len(psbl_nw_adrs[0]))]
    #     rndm_res_indx = np.random.choice(range(0, len(psbl_nw_lst_set)))
    #     x = psbl_nw_lst_set[rndm_res_indx][0]
    #     y = psbl_nw_lst_set[rndm_res_indx][1]
    #     return x, y

    # def runSchellingSegregationAtRandom(self, verbosity=False):
    #     temp_graph = self.graph.copy()   
    #     t1 = time.time()
    #     iter = 0
    #     graph_ctf = 0.0

    #     with alive_bar(self.num_of_iterations, bar='solid', title=f'{self.graph_instance_name}') as bar:
    #         for iter in range(0, self.num_of_iterations):
    #             if graph_ctf >= 1:
    #                 logging.info(f"Homophily! Segregation achived: {graph_ctf}")
    #                 self.showGraph()
    #                 break
    #             if iter % 5 == 0:
    #                 print(f"\t{self.graph_instance_name}: {graph_ctf}")
    #                 logging.info(f"\tIteration {iter} : {graph_ctf}")

    #             # random_index_row, random_index_col = self.chooseRandomSpot()
    #             random_index_row, random_index_col = self.chooserandomResidence()
    
    #             if verbosity:
    #                 logging.info(f" Graph neighbor {team_map.get(self.graph[random_index_row][random_index_col]):>3} @ ({random_index_row}, {random_index_col})")

    #             content_or_not, contentdeness = self.isContent(random_index_row, random_index_col)
    #             if content_or_not:
    #                 if verbosity:
    #                     logging.info(f"\tContent! (%{contentdeness:0.2})")
    #             else:
    #                 posible_new_streets = np.where(self.graph==0)
    #                 random_new_space = random.choice(range(0, len(posible_new_streets[0])))
    #                 if verbosity:
    #                     logging.warning("\tDiscontent! (%{contentdeness:0.2})")
    #                     logging.warning(f"\tPossible Row Address:\t\t{posible_new_streets[0]}")
    #                     logging.warning(f"\tPossible Column Address:\t{posible_new_streets[1]}")                
    #                     logging.warning(f"\tCONGRATIONLATIONS {team_map.get(self.graph[random_index_row][random_index_col])}!! YOUR MOVING TO YOUR NEW HOME which is at ({posible_new_streets[0][random_new_space]}, {posible_new_streets[1][random_new_space]}). Moving into {team_map.get(self.graph[posible_new_streets[0][random_new_space]][posible_new_streets[1][random_new_space]])} ")
                    
    #                 self.graph[posible_new_streets[0][random_new_space]][posible_new_streets[1][random_new_space]] = self.graph[random_index_row][random_index_col]
    #                 self.graph[random_index_row][random_index_col] = 0
    #             graph_ctf =  self.calculateCTF(verbosity=verbosity)
    #             self.iter_tracker[iter] = graph_ctf

    #             bar()
    #     t2 = time.time()
    #     self.runtime = t2 - t1 
    #     self.showGraph()
    #     logging.info(f"\t{self.graph_instance_name}: {graph_ctf}")    
    #     self.graph = temp_graph