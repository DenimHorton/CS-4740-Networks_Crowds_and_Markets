from network import NetWork
import numpy as np

class FriedkinJohnsenModel:
    def __init__(self, network=NetWork, trn_ses=0):
        self.net_work = network
        self.n_size = len(network.network_np_matrix)
        self.step_t_db = np.zeros((self.n_size, self.n_size))

    def __str__(self):
        objStr = "\t--- Friedkin Johnsen Model ---\n"
        objStr += f"\t Row-Stochastic  Matrix ({self.n_size} x {self.n_size})\n"
        objStr += "\t--- Network  ---\n"
        objStr += self.net_work.__str__(True)
        return objStr

