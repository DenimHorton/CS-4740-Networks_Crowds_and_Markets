import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from tabulate import tabulate
import os

plt.rcParams["figure.figsize"] = (11, 7)


def friedkin_johnsen(Lam, A, x0, k, node_of_intrst, t_step_propganda_mtrx, plot_result = False, img_sav_pth_prefx="") :
    n = A.shape[0] # assuming everything is dimensioned right
    I = np.eye(n)
    xx = np.zeros((n,k))
    xx[:,0] = x0
    for i in range(1,k) :
        xx[:,i] = Lam@A@xx[:,i-1] + (I-Lam)@x0
        t_step_propganda_mtrx.append(sum(xx[0:-1,i]))
    if plot_result:
        plt.plot(xx.T, label=["Fake Node", "Node 0", "Node 1", "Node 2", "Node 3",
                              "Node 4", "Node 5", "Node 6", "Node 7", "Node 8", "Node 9"])
        plt.legend(bbox_to_anchor=(0.1, 1.15), loc='upper left', borderaxespad=0, ncol=6)
        plt.title(f"{node_of_intrst} ---0.5---> 'FAKE' ")
        plt.xlabel('Time Steps')
        plt.ylabel('All Nodes Opinions')
        plt.get_current_fig_manager().set_window_title(f"Results from Table 1.{node_of_intrst}")
        plt.savefig(f"./Outputs/Graphs/{img_sav_pth_prefx}NodeOpnionsBadEdge{node_of_intrst}.png")          
        # plt.show()
        # plt.close()

    return xx, t_step_propganda_mtrx

def draw_from_matrix(A,draw_labels=False, drw_method='arc3, rad = 0.1') :
    G = nx.from_numpy_matrix(np.matrix(A), create_using=nx.DiGraph)
    layout = nx.spring_layout(G,seed=0)
    nx.draw(G, layout, node_size=750, with_labels=True, font_weight='bold', font_size=15, connectionstyle=f"{drw_method}")
    if draw_labels :
        labels = nx.get_edge_attributes(G, "weight")
        nx.draw_networkx_edge_labels(G, pos=nx.circular_layout(), edge_labels=labels, label_pos=.33);

def addNodeToNetwork(og_network, og_opinions, lam_lst):
    new_network = []
    # Add new col to end of each row
    for row in range(len(og_network)):
        new_col = og_network[row].copy()
        new_col.append(0.0)
        new_network.append(new_col)
    new_row = [0.0 for col in range(len(new_network)+1)]
    mod_new_network = new_network.append(new_row)
    new_opinions = og_opinions.copy()
    new_opinions.append(1.0)
    new_lam_lst = lam_lst.copy()
    new_lam_lst.append(1.0)
    new_network[-1][-1] = 1.0
    return new_network, new_opinions, new_lam_lst

def addBadEdgeToNetwork(adjusted_network, node, bad_node):
    for edge in range(len(adjusted_network[node])):
        adjusted_network[node][edge] = adjusted_network[node][edge] * 0.5
    adjusted_network[node][bad_node] = 0.5
    return adjusted_network

def timestepsToPandaDF(t_step_matrix, p_t_stp_lst, save_table_path = "./Outputs/Tables/tableOutput"):
    node_lst = [node for node in range(len(t_step_matrix))]
    time_step_dict = {f"{node}" : [] for node in range(len(t_step_matrix))}

    for t_stp in range(len(t_step_matrix[0])):
        for node in range(len(t_step_matrix)):
            time_step_dict.get(f"{node}").append(t_step_matrix[node][t_stp]) 
    
    time_step_dict.update({"p(t)": p_t_stp_lst})

    time_table = pd.DataFrame(time_step_dict, index=[f"t={t_stp}" for t_stp in range(len(t_step_matrix[0]))])
    return dataframeToTable(time_table, len(t_step_matrix), save_table_path)

def dataframeToTable(data_frame, matrix_size, save_table_path):
    tabHeaders = [f"node_{node}" for node in range(matrix_size)]
    tabHeaders[-1] = f"node_fake"
    tabHeaders.append("P(t)")

    return_table = tabulate(data_frame, headers=tabHeaders, tablefmt="fancy_grid")

    with open(f'{save_table_path}Raw', 'w') as f:
        f.write("\n")
        f.write(f"{tabulate(data_frame, headers=tabHeaders)}\n")

    os.system(f'py -m tabulate -o {save_table_path}.txt {save_table_path}Raw')

    os.remove(f'{save_table_path}Raw')

    return return_table

def networkPropagandaModel(og_network, og_lam_vals, og_opnions, num_iterations, bad_node_neighbor, t_step_propganda_lst, draw_network=False, plot_result=False, img_sav_pth_prefx=""):
    # Add node to network 
    mod_network, mod_opnions, mod_lam = addNodeToNetwork(og_network, og_opnions, og_lam_vals) # Adds self-pointing edge to
    # Multiplies the nodes row (it's edges) by 0.5 and add 0.5 edge from bad node
    # to the one of the nodes of the original network. 
    prop_network = addBadEdgeToNetwork(mod_network, bad_node_neighbor, len(mod_network)-1)

    prop_lambda_diag_lst = np.diag(mod_lam).tolist()
    t_step_propganda_lst.append(sum(mod_opnions[0:-2]))
    result , result_propganda_val = friedkin_johnsen(np.array(prop_lambda_diag_lst), np.array(prop_network), np.array(mod_opnions), num_iterations, bad_node_neighbor, t_step_propganda_lst, plot_result, img_sav_pth_prefx) 
    return result, result_propganda_val

def plotProagandaValOverTime(p_of_t_matrix, node_of_intrest, img_sav_pth_prefx=""):
    plt.plot(p_of_t_matrix.T, label=f"Propaganda-Value")
    plt.legend(bbox_to_anchor=(0.1, 1.15), loc='upper left', borderaxespad=0, ncol=6)
    plt.title(f"Overall Propaganda Value when:\n{node_of_intrest} ---0.5---> 'FAKE' ")
    plt.xlabel('Time Step')
    plt.ylabel('Networks Overall P(t) value')
    plt.get_current_fig_manager().set_window_title(f"Overall Propaganda Value")
    plt.savefig(f"./Outputs/Graphs/{img_sav_pth_prefx}OverallPValsBadEdge{node_of_intrest}.png")   
    # plt.show()
    plt.close()


def plotAllProagandaValOverTime(all_prop_val, node_of_intrest, img_sav_pth_prefx=""):
    plt.plot(all_prop_val.T, label=["Node 0", "Node 1", "Node 2", "Node 3", "Node 4",
                                    "Node 5", "Node 6", "Node 7", "Node 8", "Node 9"])
    plt.legend(bbox_to_anchor=(0.1, 1.15), loc='upper left', borderaxespad=0, ncol=6)
    plt.title(f"All possible 'FAKE' neighbor node")
    plt.xlabel('Time Step')
    plt.ylabel('Each P(t) value of possible bad edges')
    plt.get_current_fig_manager().set_window_title(f"All possible 'FAKE' neighbor node")
    plt.savefig(f"./Outputs/Graphs/{img_sav_pth_prefx}AllOverallPValsBadEdge{node_of_intrest}.png")      
    # plt.show()
    plt.close()



###########################################################################################
#                                      Project Main     
###########################################################################################

# Project graph Adj. Matrix
proj_03_adj_ntwrk = [[0.0, 0.9, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.2, 0.1, 0.4, 0.3, 0.0, 0.0, 0.0, 0.0],
                     [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0], 
                     [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9, 0.0, 0.1, 0.0], 
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0], 
                     [0.4, 0.0, 0.0, 0.2, 0.0, 0.0, 0.0, 0.4, 0.0, 0.0], 
                     [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0], 
                     [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0],  
                     [0.0, 0.0, 0.8, 0.0, 0.1, 0.0, 0.0, 0.0, 0.1, 0.0]]

# List of Lambda values 
lambda_vals = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95]

# Initial opnions
node_opnins = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

# Bloabl value to set for running test runs 
TRAINING_ITERATIONS = 2

# Empty T-Step matrix to keep track of opinions 
p_t_steps=[]

# Empty list to store the p value after each  
overall_p_vals = []

# Iterate through each row of the matrix that represent each possible neighbor, 
# that the bad node's one edge could be connected to. 
for possible_neigh in range(len(proj_03_adj_ntwrk)):
    # Print table headrer in output to help'
    print("************************************************************")
    print(f"*               Running Short Test                        *")
    print("************************************************************")
    print(f"Tabel 1.{possible_neigh}.Short")
    result, p_t_steps = networkPropagandaModel(proj_03_adj_ntwrk, lambda_vals, node_opnins, TRAINING_ITERATIONS, possible_neigh, p_t_steps, plot_result=True, img_sav_pth_prefx="shrt")
    print("-------------------------------------------------------------")
    print(f" Node {possible_neigh} Directly influenced by 'fake node' test results")
    print("-------------------------------------------------------------")
    plotProagandaValOverTime(np.array(p_t_steps), possible_neigh, img_sav_pth_prefx="shrt")
    temp_lst = p_t_steps.copy()
    print(timestepsToPandaDF(result, temp_lst, save_table_path=f"./Deliverable02/Tables/ShortTermTableBadConnection{possible_neigh:02}"))
    overall_p_vals.append(temp_lst)
    p_t_steps.clear()
    print("-------------------------------------------------------------\n\n")  
plotAllProagandaValOverTime(np.array(overall_p_vals), possible_neigh, img_sav_pth_prefx="shrt")



TRAINING_ITERATIONS = 10
overall_p_vals.clear()
p_t_steps.clear()

for possible_neigh in range(len(proj_03_adj_ntwrk)):
    print("************************************************************")
    print(f"*               Running Medium Test                       *")
    print("************************************************************")    
    print(f"Tabel 1.{possible_neigh}.Medium")
    result, p_t_steps = networkPropagandaModel(proj_03_adj_ntwrk, lambda_vals, node_opnins, TRAINING_ITERATIONS, possible_neigh, p_t_steps, plot_result=True, img_sav_pth_prefx="medium")
    print("-------------------------------------------------------------")
    print(f" Node {possible_neigh} Directly influenced by 'fake node' test results")
    print("-------------------------------------------------------------")
    plotProagandaValOverTime(np.array(p_t_steps), possible_neigh, img_sav_pth_prefx="medium")
    temp_lst = p_t_steps.copy()
    print(timestepsToPandaDF(result, temp_lst, save_table_path=f"./Deliverable03/Tables/LongTermTableBadConnection{possible_neigh:02}"))
    overall_p_vals.append(temp_lst)
    p_t_steps.clear()
    print("-------------------------------------------------------------\n\n")  
plotAllProagandaValOverTime(np.array(overall_p_vals), possible_neigh, img_sav_pth_prefx="medium")



TRAINING_ITERATIONS = 100
overall_p_vals.clear()
p_t_steps.clear()

for possible_neigh in range(len(proj_03_adj_ntwrk)):
    print("************************************************************")
    print(f"*               Running Long Test                         *")
    print("************************************************************")    
    print(f"Tabel 1.{possible_neigh}.Long")
    result, p_t_steps = networkPropagandaModel(proj_03_adj_ntwrk, lambda_vals, node_opnins, TRAINING_ITERATIONS, possible_neigh, p_t_steps, plot_result=True, img_sav_pth_prefx="long")
    print("-------------------------------------------------------------")
    print(f" Node {possible_neigh} Directly influenced by 'fake node' test results")
    print("-------------------------------------------------------------")
    plotProagandaValOverTime(np.array(p_t_steps), possible_neigh, img_sav_pth_prefx="long")
    temp_lst = p_t_steps.copy()
    print(timestepsToPandaDF(result, temp_lst, save_table_path=f"./Deliverable03/Tables/LongTermTableBadConnection{possible_neigh:02}"))
    overall_p_vals.append(temp_lst)
    p_t_steps.clear()
    print("-------------------------------------------------------------\n\n")  
plotAllProagandaValOverTime(np.array(overall_p_vals), possible_neigh, img_sav_pth_prefx="long")