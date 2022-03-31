from network import NetWork
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tools.print_matrix_pretty import *


class FriedkinJohnsenModel:
    def __init__(self, network=NetWork, trn_ses=0, max_steps=20):
        self.network = network
        self.n_size = len(network.network_np_matrix)
        self.max_steps = max_steps
        self.step_t_db = np.zeros((max_steps, self.n_size))
        

    def __str__(self):
        objStr = "\n\t--- Friedkin Johnsen Model ---"
        objStr += f"\n Row-Stochastic Matrix size:\n\t\t{self.n_size} x {self.n_size}"
        objStr += f"\n Time Steps:\n"
        objStr = printPrettyMatrix(objStr, self.step_t_db)
        objStr += "\n\t--- Network  ---\n"
        objStr += self.network.__str__(True)
        return objStr

    def performStep(self):
        t = 0
        for i in range(self.max_steps):
            print(self.network.network_np_matrix)
            print(self.network.lambda_opinions_diag)
            print(self.step_t_db[0])
            print(np.identity(self.n_size))
            print(self.network.network_np_matrix @ self.network.lambda_opinions_diag)
            print((self.network.network_np_matrix @ self.network.lambda_opinions_diag * np.transpose(self.step_t_db[t-1])) + (np.identity(self.n_size)) - self.network.network_np_matrix)
            # self.step_t_db[t]= (self.network.network_np_matrix @ self.network.lambda_opinions_diag * np.transpose(self.step_t_db[t-1])) + (np.identity(self.n_size)) - self.network.network_np_matrix
            t += 1
