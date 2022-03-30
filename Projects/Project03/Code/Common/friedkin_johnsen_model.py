from network import NetWork
import numpy as np

class FriedkinJohnsenModel:
    def __init__(self, network=NetWork):
        self.traing_session = 0
        self.net_work = network
        n_size = len(network.network_np_matrix)
        self.step_t_db = np.zeros((n_size, n_size))

    def __str__(self):
        objStr = "\t--- Friedkin Johnsen Model ---\n"
        objStr += "Network"
        objStr += self.net_work.__str__(True)
        return objStr

