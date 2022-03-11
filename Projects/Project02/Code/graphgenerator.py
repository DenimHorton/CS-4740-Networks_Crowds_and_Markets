import logging
from re import X
import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
import math, random, time, logging, glob, os, sys, shutil
from matplotlib.animation import FuncAnimation
from alive_progress import alive_bar
from PIL import Image
 
'''
File/Program Configuration Setup
'''

save_log_path = f".\\Content\\LogInfo\\"
isExist = os.path.exists(save_log_path)

if not isExist:
    os.makedirs(save_log_path)

logging.basicConfig(filename=f"{save_log_path}loginfo.log", filemode='w', level=logging.INFO)
logging = logging.getLogger('alive_progress')

team_map = {0:"Empty Space", 1:"Red Residence", -1:"Blue Residence"}

class City(object):
    def __init__(self, t=0.5, os=0.5, mxd=0.5, g_size=20, grph_ind_num="TestDefault",
                 num_iter = 100, cap_pt_lst=[] ):
        # Contentedness threshold
        self.t_value = t
        # Percentage of open spaces in generated graph
        self.open_spots = os
        # Percentage of 'Red' residence versus 'Blue'  
        self.red_blue_split = mxd        
        # Graph name to indicate 'deliverable' or 'TestDefault' as default **kwarg     
        self.city_name = f"Graph-{grph_ind_num}"
        # Instance of graph create on instansiation of 
        self.city = self.generateRandomCityPop()
        # Set the total poulation size from either defualt **kwarg or passed 'g_size' parm
        self.city_size = g_size * g_size
        # Instansiate timmer
        self.runtime = 0.0
        # Instansiate
        self.num_of_iterations = num_iter
        self.iter_tracker = dict([(i, 0) for i in range(0, self.num_of_iterations)])
        self.capture_points = cap_pt_lst

    def __str__(self):
        obj_str = f"----------- {self.city_name} -----------\n"
        obj_str += f"Graph size:\t\t\t\t{self.red_blue_split}\n"
        obj_str += f"Graph Mixed Residence Percentage:\t{self.red_blue_split}\n"
        obj_str += f"Graph Open Spot Percentage:\t\t{self.open_spots}\n"  
        obj_str += f"Graph \'t-value:\':\t\t\t{self.t_value}\n"
        obj_str += f"Runtime:\t\t\t\t{self.runtime}\n"
        obj_str += f"Graph:\n{self.city}"
        return obj_str 

    def setTValue(self, t_v):
        self.t_value=t_v

    def setOSValue(self, o_spts):
        self.open_spots=o_spts

    def setMixedValue(self, mxd):
        self.t_value=mxd

    def setGraphName(self, new_name):
        self.city_name = f"Graph-{new_name}"

    def showGraph(self, iter=0):
        plt.matshow(self.city, cmap='seismic')
        plt.title(f"{self.city_name}-{iter:03}")
        plt.show()
        plt.close()

    def saveGraph(self, iter=0, epsd=0):
        sub_dir=f"{epsd}"   
        plt.matshow(self.city, cmap='seismic')
        plt.title(f"{self.city_name}\nT-Value:%{self.t_value}Mixed:%{self.red_blue_split}Openspot:%{self.open_spots}-{iter:03}")
        save_grph_path = f".\\Content\\GeneratedGraphs\\{self.city_name}-{self.t_value}-{self.red_blue_split}-{self.open_spots}"
        isExist = os.path.exists(save_grph_path)
        if not isExist:
            os.makedirs(save_grph_path)
        plt.savefig(f"{save_grph_path}\\{self.city_name}-{iter:03}.png")
        plt.close()

    def generateRandomCityPop(self):
        # Get total number of spots that are occupied by 'residence' 
        number_of_residence = self.city_size - int(self.city_size * self.open_spots)
        # Get total number of 'Blue residence'
        blue_residence = int(number_of_residence * self.red_blue_split)
        # Get total number of 'Red residence'
        red_residence = number_of_residence - blue_residence 
        # Instantiate empty list to store all possible 'residence'  
        generated_residence = []
        # Populate list with 'Red residnce'
        for red_res in range(0, red_residence):
            generated_residence.append(1) 
        # Populate list with 'Blue residnce'
        for blu_res in range(0, blue_residence):
            generated_residence.append(-1)
        # Populate list with 'No residnce' or 'open spots'
        for open_res in range(0, self.city_size - number_of_residence):
            generated_residence.append(0)
        # Shuffle the list of residence
        random.shuffle(generated_residence)
        # Generate numpy array with shuffled list to represnt the city
        self.city = np.array(generated_residence).reshape(int(math.sqrt(self.city_size)), int(math.sqrt(self.city_size)))  

    def isContent(self, indx_row, indx_col, verbosity=False):
        if verbosity:
            logging.info(f"  Checking if this residence is content . . .")

        blue_counter, red_counter, open_counter = self.getNeighborCount(indx_row, indx_col, verbosity=verbosity)
        num_local_neghbors = (8 - open_counter)

        # Has only open spots around it.
        if num_local_neghbors == 0:
            return True, 0.0
        elif (self.city[indx_row][indx_col] == 1 ) and (blue_counter / num_local_neghbors  < self.t_value):
            return True, blue_counter / num_local_neghbors 

        elif (self.city[indx_row][indx_col] == -1 ) and (blue_counter / num_local_neghbors  < self.t_value):
            return True, blue_counter / num_local_neghbors

        elif (self.city[indx_row][indx_col] == 1 ) and (blue_counter / num_local_neghbors  >= self.t_value):
            return False, blue_counter / num_local_neghbors 
            
        elif (self.city[indx_row][indx_col] == -1 ) and (red_counter / num_local_neghbors  >= self.t_value):
            return False, red_counter / num_local_neghbors 
        # Evaluating open spot which will be content because its an open spot . . . 
        else:
            return True,  1.0

    def getNeighborCount(self, indx_row, indx_col, verbosity=False):

        sub_arry_lst = []
        
        for col in range(indx_col-1, indx_col+2):
            for row in range(indx_row-1, indx_row+2):
                try:
                    sub_arry_lst.append(str(self.city[row][col]))
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
            team = self.city[indx_row][indx_col]
            logging.info(f"\t{team_map.get(team)}:\t({indx_row}, {indx_col})")
            logging.info(f"\t{local_neighborhood[0]}")
            logging.info(f"\t{local_neighborhood[1]}")
            logging.info(f"\t{local_neighborhood[2]}")
            logging.info(f"\t\tRed Counter:\t{red_counter}")
            logging.info(f"\t\tBlue Counter:\t{blue_counter}\n- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -  ")  

        return blue_counter, red_counter, open_counter

    def runSchellingSegregation(self, verbosity=False, capture_iter_num = 5):
        temp_graph = self.city.copy()   
        t1 = time.time()
        iter = 0
        graph_ctf = 0.0

        with alive_bar(self.num_of_iterations, bar='solid', title=f'{self.city_name}') as bar:
            for iter in range(0, self.num_of_iterations):
                if graph_ctf >= 1.0:
                    logging.info(f"Homophily! Segregation achived: {graph_ctf}")
                    print(f"\t{self.city_name}: {graph_ctf}")
                    self.saveGraph(iter, epsd=self.city_name)
                    break
                if iter % (self.num_of_iterations / capture_iter_num) == 0 or iter in self.capture_points:
                    print(f"\t{self.city_name}: {graph_ctf}")
                    logging.info(f"\tIteration {iter:>3} : CTF : {graph_ctf:0.4f}")
                    self.saveGraph(iter, epsd=self.city_name)

                for row in range(0, len(self.city[0])):
                    for col in range(0, len(self.city[row])):
    
                        if verbosity:
                            logging.info(f" Graph neighbor {team_map.get(self.city[row][col]):>3} @ ({row}, {col})")

                        content_or_not, contentdeness = self.isContent(row, col)
                        if content_or_not:
                            if verbosity:
                                logging.info(f"\tContent! (%{contentdeness:0.2})")
                        else:
                            posible_new_streets = np.where(self.city==0)
                            posible_new_address = tuple(zip(posible_new_streets[0], posible_new_streets[1]))
                            random_new_space = random.choice(posible_new_address)
                            if verbosity:
                                logging.warning("\tDiscontent! (%{contentdeness:0.2})")
                                logging.warning(f"\tPossible New Address':\t\t{posible_new_address}")
                                logging.warning(f"\tCONGRATIONLATIONS {team_map.get(self.city[row][col])}!! YOUR MOVING TO YOUR NEW HOME which is at ({random_new_space[0]}, {random_new_space[1]}). Moving into {team_map.get(self.city[random_new_space[0]][random_new_space[1]])} ")
                                 
                            self.city[random_new_space[0]][random_new_space[1]] = self.city[row][col]
                            self.city[row][col] = 0

                graph_ctf =  self.calculateCTF(verbosity=verbosity)
                self.iter_tracker[iter] = graph_ctf
               
                bar()
                            
            t2 = time.time()
            self.runtime = t2 - t1 

            if verbosity:
                self.showGraph(iter=iter)
                self.saveGraph(iter, epsd=self.city_name)
            logging.info(f"\t{self.city_name}: {graph_ctf}")    
            self.city = temp_graph

    def calculateCTF(self, verbosity=False):

        total_neighbors = 0
        total_cross_neighbors = 0
        
        if verbosity:
            logging.info(f" Calculating CTF . . . ")

        for street in range(0, len(self.city)):
            for residence in range(0, len(self.city[street])):
                blu_neighbors, red_neighbors, open_neighbors = self.getNeighborCount(street, residence, verbosity=verbosity)
                total_neighbors += (blu_neighbors + red_neighbors)
                if self.city[street][residence] == 1:
                    total_cross_neighbors += red_neighbors
                elif self.city[street][residence] == -1:
                    total_cross_neighbors += blu_neighbors

        ctf = total_cross_neighbors / total_neighbors
        if verbosity:
            logging.info(f"\tCTF:\t{ctf}")
        return ctf