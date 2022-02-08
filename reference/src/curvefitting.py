import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit 



data = np.load('data.npy')

time = data[0]
signal = data[1:]



def biexponential(t, a, p, T1, T2, y0):
	return a*(p*np.exp(-t/T1) + (1 - p)*np.exp(-t/T2)) + y0

def monoexponential(t, y0, a, T1):
	return y0*(1 - ((a*a)**0.5)*np.exp(-t/T1))


initial_parameters = [35, 0.5, 0.1]

some_array = []
x_axis = time


for index, item in enumerate(signal):
	y_axis = item
	popt, pcov = curve_fit(monoexponential, x_axis, y_axis, p0=initial_parameters)
	answer = np.array(monoexponential(x_axis, popt[0], popt[1], popt[2]))
	some_array.append((1/popt[2]))
	initial_parameters = [popt[0], popt[1], popt[2]]

q_array = np.array([(2*math.pi*(x+1)/(256*6.5/20))**2 for x in range(0, 128)])
some_array = np.array(some_array)

plt.scatter(q_array, some_array)
plt.grid()
plt.show()