import numpy as np
import matplotlib.pyplot as plt
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Tools.print_matrix_pretty import *
from Common.network import NetWork



class FriedkinJohnsenModel:
  def __init__(self, network=NetWork, trn_ses=0, max_steps=20):
      self.network = network
      self.n_size = len(network.network_np_matrix)
      self.time_step = 0
      self.step_t_db = np.array
      
  def __str__(self):
      objStr = "\n\t--- Friedkin Johnsen Model ---"
      objStr += f"\n Row-Stochastic Matrix size:\n\t\t{self.n_size} x {self.n_size}"
      objStr += f"\n Time Steps:\n"
      objStr = printPrettyMatrix(objStr, self.step_t_db)
      objStr += "\n\t--- Network  ---\n"
      objStr += self.network.__str__(True)
      return objStr

  def performTrainingSes(self, max_steps=10, plot_result=False, verbose=False):
    n = self.network.network_np_matrix.shape[0] # assuming everything is dimensioned right
    I = np.eye(n)
    self.step_t_db = np.zeros((n,max_steps))
    og_opinions = np.array([0 for i in range(len(self.network.network_np_matrix))])

    # print(self.step_t_db)
    self.step_t_db[:,0] = og_opinions     
    for step in range( max_steps):
      self.step_t_db = self.performFriedkinJohnsenStep(max_steps, og_opinions, step, I, 
                                      self.network.lambda_opinions, verbose)
      if verbose:
        print(f"T-Step Matrix:{self.step_t_db}")   
        print()            
    if plot_result:
      plt.plot(self.step_t_db.T)
    return self.step_t_db 

  def performFriedkinJohnsenStep(self, mx_stps, og_opnins, step, I, Lam,  verbose):
    if verbose:
      # print("Lam:")
      # print(Lam)
      # print(f"Adj.:")
      # print(self.network.network_np_matrix)
      # print(f"???:")
      # print(self.step_t_db[:,step-1])
      # print(f"I matrix:")
      # print(I)
      print("<Lam> @ <adj.> @ <step-t matrix [t-1]> + (<identity matrix> - <lambda diag>) @ <original opinions>" )
      print(Lam, " @ ", self.network.network_np_matrix, f" @ {self.step_t_db[:,step-1]} + ({I} - {Lam})@{og_opnins.T} ")
      print(Lam@self.network.network_np_matrix, f" @ {self.step_t_db[:,step-1]} + ({I} - {Lam})@{og_opnins.T} ")
      print(Lam@self.network.network_np_matrix@self.step_t_db[:,step-1], f" + ({I - Lam})@{og_opnins.T} ")
      print(f"{Lam@self.network.network_np_matrix@self.step_t_db[:,step-1]} + {(I-Lam)@og_opnins}")

    self.step_t_db[:,step] = Lam@self.network.network_np_matrix@self.step_t_db[:,step-1] + (I-Lam)@og_opnins
    
    return self.step_t_db

  def addNodeToNetwork(self):
    self.network.addNode(self.n_size)
    self.n_size += 1

  def addEdgeToNetwork(self, residence, new_neighbor):
    self.network.addEdge(residence, new_neighbor)

