import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import sys, glob

# print(glob.glob("./*.png"))
# print(type(glob.glob("./*.png")))

# for i in sys.path:
#     print(i)


# somplot = plt.matshow(arry)

# empytlst.append('.\\Graph-TestDefault-000.png')

# frames = []

# for i in empytlst:
#     new_frame = Image.open(i)
#     frames.append(new_frame)


# # Save into a GIF file that loops forever
#     frames[0].save('./something.gif', format='GIF',
#                   append_images=frames[1:],
#                   save_all=True,
#                   duration=300, loop=0)



    






# arry = np.array([[i for i in range(0, 5)], [j for j in range(0,5)],  [j for j in range(0,5)],  [j for j in range(0,5)],  [j for j in range(0,5)]])
# np.random.shuffle(arry)

# indx_col = 0
# indx_row = 0 

# sub_arry_lst = []
# # Iterate through local neighbors and build list
# for row in range(indx_col-1, indx_col+2):
#     for col in range(indx_row-1, indx_row+2):
#         # If a invalid 'residence address' (out side of the city limits) set to "N/A"
            
#         try:
#             if col == -1:
#                 sub_arry_lst.append("N/A")
#                 print(f"\t\tIndex:({row}, {col}) is out of bounds.")
#             elif row == -1:
#                 sub_arry_lst.append("N/A")
#             else:
#                 sub_arry_lst.append(str(arry[row][col]))
#         except IndexError:
#             print(f"\t\tIndex:({row}, {col}) is out of bounds.")
#             sub_arry_lst.append("N/A")


# print(sub_arry_lst)


# local_neighborhood = np.array(sub_arry_lst).reshape(3, 3)
# print(local_neighborhood)



# sumArray = np.zeros((5, 5))

# print(sumArray)

# print(np.where(sumArray == 0))


# x = [(1, 2), (2,3), (3, 4), (4, 5)]
x_0 = [i for i in range(0, 10) ]
x_1 = [1, 3, 4, 6, 2, 3, 4, 6, 4, 4]
y_0 = [i for i in range(0, 20, 2)]
y_1 = [2, 3, 4, 3, 2, 1, 23, 4, 3, 2]

plt.plot(x_0, y_0)
plt.plot(x_1, y_1)
# overallPlot.plot(y)
plt.show()