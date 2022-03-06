import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image
import sys, glob

print(glob.glob("./*.png"))
print(type(glob.glob("./*.png")))

for i in sys.path:
    print(i)

empytlst=[]

arry = np.array([[i for i in range(0, 10)], [j for j in range(0,10)]])

somplot = plt.matshow(arry)

empytlst.append('.\\Graph-TestDefault-000.png')

frames = []

for i in empytlst:
    new_frame = Image.open(i)
    frames.append(new_frame)


# Save into a GIF file that loops forever
    frames[0].save('./something.gif', format='GIF',
                  append_images=frames[1:],
                  save_all=True,
                  duration=300, loop=0)



    