from xmlrpc.client import Boolean
import numpy as np
import matplotlib.pyplot as plt
import random, time
from alive_progress import alive_bar


class City():
    def __init__(self, cty_nm="Default City Name", n=10, opn_pct=0.3, mxd_pct=0.4):
        self.city_name = cty_nm
        self.city_size = n * n
        self.city_n_dimn = n
        self.empt_pct = opn_pct
        self.red_blue_split = mxd_pct
        self.tot_pop = 0
        self.cross_type_neighbours = 0
        self.same_type_neighbours = 0
        self.tot_red_res = 0
        self.tot_blu_res = 0
        self.tot_opn_adrs = 0
        self.city = np.array
        self.generateRadnPopCity()
        self.setResidenceAddresses()
        self.ctf = 0

    def __str__(self):
        city_str = ""
        for city_strt in self.city:
            for adres in range(0, len(city_strt)):
                city_str += f"{city_strt[adres].team}\n" 
                city_str += f"\tAddress:\t{city_strt[adres].address}\n" 
                city_str += f"\tT-Value:\t{city_strt[adres].t_value}\n" 
                city_str += f"\tContent:\t{city_strt[adres].isContent}\n" 
        return city_str
    
    def setOpenPercentage(self, op):
        self.empt_pct = op

    def setMixedPercentage(self, mp):
        self.red_blue_split = mp

    def setTValue(self, tvl):
        for strt in self.city:
            for adrs in range(0, len(strt)):
                if strt[adrs] != 0:
                    strt[adrs].t_value = tvl

    def getCityGraph(self, iter=0, graph_name="defualt"):
        city_graph_array = np.zeros((self.city_n_dimn, self.city_n_dimn))
        for i in range(self.city_n_dimn):
            for j in range(self.city_n_dimn):
                if self.city[i][j].team == "Blue":
                    city_graph_array[i][j] = 1
                elif self.city[i][j].team == "Red":
                    city_graph_array[i][j] = -1
                else:
                    city_graph_array[i][j] = 0
        # Matplot graph to show grid of 'city' 
        plt.matshow(city_graph_array, cmap='seismic')
        # Set title of graph to be shown 
        plt.title(f"{self.city_name}-{graph_name}")
        # Show the graph
        plt.show()
        # time.sleep(30)
        # Close the graph
        plt.close()       

    def setResidenceAddresses(self):
        for strt in range(0, self.city_n_dimn):
            for adrs in range(0, self.city_n_dimn):
                self.city[strt][adrs].address = (strt, adrs)
                if self.city[strt][adrs].team != 0:
                    blu_res, red_res, opn_ards = self.getLocalNeghborhood(strt, adrs)
                    if self.city[strt][adrs].team == "Blue":
                        self.city[strt][adrs].mixed_neighboour_count = red_res
                        self.city[strt][adrs].same_neighbour_count = blu_res
                    elif self.city[strt][adrs].team == "Red":
                        self.city[strt][adrs].mixed_neighboour_count = blu_res
                        self.city[strt][adrs].same_neighbour_count = red_res
                    # Set content level
                    self.city[strt][adrs].contentOrNot()

    def getDiscontentResidence(self):
        dicontent_residence = []
        for strt in range(0, self.city_n_dimn):
            for adrs in range(0, self.city_n_dimn):
                # print(self.city[strt][adrs])
                if self.city[strt][adrs].isContent == False:
                    print("Discontent!")
                    dicontent_residence.append(self.city[strt][adrs].address)
                else:
                    print("Content!")
        return dicontent_residence

    def getLocalNeghborhood(self, indx_row, indx_col):
        # Temp list to build small neighboring residence 
        sub_arry_lst = []
        # Iterate through local neighbors and build list
        for row in range(indx_row-1, indx_row+2):
            for col in range(indx_col-1, indx_col+2):
                # If a invalid 'residence address' (out side of the city limits) set to "N/A"
                try:
                    if col == -1 or row == -1:
                        sub_arry_lst.append("N/A")
                    else:
                        sub_arry_lst.append(str(self.city[col][row].team))
                except IndexError:
                    sub_arry_lst.append("N/A")
        sub_arry_lst[4] = "RES"
        # print(np.array(sub_arry_lst).reshape((3, 3)))
        # Replace the residence value with something other than its original value to make sure it is not counted when seraching
        # the 'sub_arry_lst' for the amount of each type of neighbor and empty spaces.
        # Count up 'Red residence'
        blue_counter = sub_arry_lst.count("Blue")
        # Count up 'Blue residence'
        red_counter = sub_arry_lst.count("Red")
        # Count up 'Empty spots'
        open_counter = sub_arry_lst.count("Open")
        return blue_counter, red_counter, open_counter

    def generateRadnPopCity(self, blue_t_val=0.3, red_t_val=0.3):
        # Get total number of residence with set percentage of open spots
        self.tot_pop = self.city_size - int(self.city_size * self.empt_pct)
        # Get number of 'Blue residence'
        self.tot_blu_res = int(self.tot_pop * self.red_blue_split)
        # Get number of 'Red residence'
        self.tot_red_res = self.tot_pop - self.tot_blu_res 
        # Instasiate empty list to populate with residence
        residence_lst = []
        # Add 'Red residence' to list 
        for red_res in range(0, self.tot_red_res):
            residence_lst.append(RedResidence(red_t_val)) 
            # residence_lst.append(RedResidence(red_t_val)) 
        # Add 'Blue residence' to list 
        for blu_res in range(0, self.tot_blu_res):
            residence_lst.append(BlueResidence(blue_t_val))
            # residence_lst.append(BlueResidence(blue_t_val))
        # Add 'Open spots' to list 
        for open_res in range(0, self.city_size - self.tot_pop):
            residence_lst.append(OpenAddress(0.0))
        random.shuffle(residence_lst)
        # Set np.array to city attribute to represent city population residence and thier location 
        self.city = np.array(residence_lst, dtype=object).reshape((self.city_n_dimn, self.city_n_dimn))

    def pickRandomOpenSpot(self):
        psb_new_adrs =np.where(self.city.astype(OpenAddress))
        return random.choice(list(zip(psb_new_adrs[0], psb_new_adrs[1])))

    def pickClosestOpenSpot(self):
        random.choice(np.where(list(zip(self.city.astype(OpenAddress)))))    
        return 

    def modifyResidence(self, new_pct_empty, new_red_blue_split):
        return 0

    def calculateCTF(self):
        same_neighbour_acum = 0
        mixed_neighbour_acum = 0
        for i in range(0, len(self.city)):
            for j in range(0, len(self.city)):
                mixed_neighbour_acum += self.city[i][j].mixed_neighbour_count
                same_neighbour_acum +=  self.city[i][j].same_neighbour_count                            
        self.ctf = mixed_neighbour_acum / same_neighbour_acum + mixed_neighbour_acum

    def checkNewAddress(self, adress_to_check, new_resident):
        self.city[adress_to_check[0]][adress_to_check[1]].contentOrNot(new_resident)


class OpenAddress(object):
    def __init__(self, res_t_val):
        self.team = "Open"
        self.t_value = res_t_val
        self.address = set()
        self.same_neighbour_count = 0
        self.mixed_neighboour_count = 0
        self.isContent = Boolean

    def contentOrNot(self, resident_team):
        # Gets the total number of actual 'residence' (not including open spots) 
        num_local_neghbors = resident_team.same_neighbour_count + resident_team.mixed_neighboour_count
        if num_local_neghbors == 0:
            self.isContent = False
        else:
            content_lvl = self.same_neighbour_count / num_local_neghbors
            if content_lvl >= self.t_value:
                self.isContent = True
                return True
            else:
                self.isContent = False
                return False

    def moveToOpenAddress(self, new_address):
        self.address = new_address
        
class RedResidence(OpenAddress):
    def __init__(self, res_t_val):
        super(RedResidence, self).__init__(res_t_val)
        self.team = "Red"


class BlueResidence(OpenAddress):
    def __init__(self, res_t_val):
        super(BlueResidence, self).__init__(res_t_val)
        self.team = "Blue"

def setCapturePoint():
    return 0

def runSchellingSegregationSim(City, num_iterations=30, method='discontent order'):
    # Intialize dict to keep track of CTF for each iteration
    iter_ctf_track_dict = dict([(i, 0) for i in range(0, num_iterations)])
    # Store copy of original randomnly populated city to reset at end of simulation 
    temp_graph = np.copy(City.city)         
    # Get starting time for method
    t1 = time.time()        
    # Initialize city CTF and previous CTF
    city_ctf = 0.0
    # Clear iter CTF tracker for next run
    [iter_ctf_track_dict.update({i : 0}) for i in iter_ctf_track_dict.keys()]
    # Show status bar for Schelling Segreagation simulations 
    with alive_bar(num_iterations, bar='solid', title=f'{City.city_name}') as bar:
        for iter in range(0, num_iterations):
            # Using dicontent method
            if method == 'discontent order':
                discontent_residence_lst = City.getDiscontentResidence()   
                print(discontent_residence_lst)     
                for i in discontent_residence_lst:
                    if City.ctf <= 0.5:
                        print(f"Achived segregation . . .")
                        break
                    print(f"Discontent Resident{i}")
                    max_tries = 10
                    couldMove = False
                    pick_try = 0
                    moving_adr = City.pickRandomOpenSpot()
                    # moving_adr = City.pickClosestOpenSpot()                    
                    while pick_try < max_tries:
                        print(f"Moving from {i} to ({moving_adr[0]}, {moving_adr[1]})")
                        if City.checkNewAddress(moving_adr):
                            City.moveToOpenAddress(moving_adr)
                            couldMove = True
                            break
                        else:
                            moving_adr = City.pickRandomOpenSpot()
                            # moving_adr = City.pickClosestOpenSpot() 
                        ick_try += 1   
                    if not couldMove:
                        print(f"We cant move this residence . . .")
                City.ctf = City.calculateCTF() 

            elif method == 'row major':
                for row in range(0, len(City.city_n_dimn)):
                    for col in range(0, len(City.city_n_dimn)):
                        if City.ctf <= 0.5:
                            print(f"Achived segregation . . .")
                            break
                        print(f"{City.city[row][col]}")
                        if City.city[row][col].isContent:
                            print("Content!")
                        else:
                            print("Discontent!")
                            moving_adr = City.pickRandomOpenSpot()
                            # moving_adr = City.pickClosestOpenSpot()
                            while pick_try < max_tries:
                                print(f"Moving from {i} to ({moving_adr[0]}, {moving_adr[1]})")
                                if City.checkNewAddress(moving_adr):
                                    City.moveToOpenAddress(moving_adr)
                                    couldMove = True
                                    break
                                else:
                                    moving_adr = City.pickRandomOpenSpot()
                                    # moving_adr = City.pickClosestOpenSpot() 
                                pick_try += 1   
                            if not couldMove:
                                print(f"We cant move this residence . . .")
                        City.ctf = City.calculateCTF()
            bar()









sumCity = City(n=5, mxd_pct=0.2, opn_pct=0.2)

print(sumCity)
runSchellingSegregationSim(sumCity)
sumCity.getCityGraph()

# print(sumCity)


