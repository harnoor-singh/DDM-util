import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.widgets as mwidgets
from scipy.optimize import curve_fit
from scipy.stats import linregress


q_array = np.load('q_array.npy')
T1_array = np.load('T1_array.npy')

data = []
for i in range(len(q_array)):
	data.append([q_array[i], T1_array[i]])

fig, ax = plt.subplots()
ax.scatter(q_array, T1_array)

def onselect(eclick, erelease):
	x1, y1 = eclick.xdata, eclick.ydata
	x2, y2 = erelease.xdata, erelease.ydata
	slope_points = []
	for item in data:
		item = list(item)
		if item[0] >= x1 and item[0] <= x2 and item[1] >= y1 and item[1] <= y2:
			slope_points.append(item)
	ans = linregress([i[0] for i in slope_points], [i[1] for i in slope_points])
	print(ans)

props = dict(facecolor='lightsteelblue', alpha=0.5)
rect = mwidgets.RectangleSelector(ax, onselect, interactive=True, props=props)
plt.grid()
plt.show()

