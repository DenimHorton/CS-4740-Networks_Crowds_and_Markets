from network import NetWork
import numpy as np

class FriedkinJohnsenModel:
    def __init__(self, network=NetWork, trn_ses=0):
        self.training_session = trn_ses
        self.net_work = network
        n_size = len(network.network_np_matrix)
        self.step_t_db = np.zeros((n_size, n_size))

    def __str__(self):
        objStr = "\t--- Friedkin Johnsen Model ---\n"
        objStr += self.net_work.__str__(True)
        objStr += "\t--- Network  ---\n"
        objStr += self.net_work.__str__(True)
        return objStr

