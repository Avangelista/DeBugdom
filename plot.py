# Bugdom_Level_Plot.py
# Rory 2020
# Plots items, fences etc. from a Bugdom level

from sys import argv
import matplotlib.pyplot as plt
from glob import glob
from os import path

# fences
for file in glob("FnNb/*"):
    if path.splitext(file)[1] != '':
        continue
        
    x = []
    y = []
    with open(file, "rb") as f:
        data = f.read(8)
        while data:
            x += [data[2] * 256 + data[3]]
            y += [data[6] * 256 + data[7]]
            data = f.read(8)

    plt.plot(x, y, 'b-')

# items
with open('Itms/1000', "rb") as f:
    data = f.read(12)
    while data:
        x = data[0] * 256 + data[1]
        y = data[2] * 256 + data[3]
        # plt.plot(x, y, 'bo')
        plt.text(x, y, str(data[5]), fontsize=8)
        # plt.text(x, y, str(data[5]) + ',' + str(data[6]) + ',' + str(data[7]), fontsize=8)
        data = f.read(12)

# flip plot
ax = plt.gca()
ax.set_ylim(ax.get_ylim()[::-1])

# show plot
plt.show()
