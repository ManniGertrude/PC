import matplotlib.pyplot as plt
import scipy.optimize as opt
import scipy.odr as odr
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


Punkte = 10000
Maß = 0.5

phi = 2 * np.pi * np.random.rand(Punkte)
theta = np.arccos(2 * np.random.rand(Punkte) - 1)

x = np.sin(theta) * np.cos(phi)
y = np.sin(theta) * np.sin(phi)
z = np.cos(theta)

fig = plt.figure()
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})

for i in range(Punkte):
    if (x[i] < Maß and y[i] < Maß and x[i] > - Maß and y[i] > - Maß):
        ax.scatter(x[i], y[i], z[i], c='b', marker='.')
    else:
        ax.scatter(x[i], y[i], z[i], c='r', marker='.')





plt.savefig('PC\\Annika\\Kugel.pdf')
plt.show()
plt.cla()
# plt.hist(xWerte+yWerte+FxWerte+FyWerte, bins=100)
# plt.hist(FxWerte+FyWerte, bins=100)
# plt.savefig('PC\\Annika\\Kugelplot.pdf')
# plt.cla()










