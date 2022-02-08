import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import inputdata


# Import variables
filename = inputdata.filename
ip_monoexp = inputdata.initial_parameters_monoexponential
ip_biexp = inputdata.initial_parameters_biexponential
mono_or_bi = inputdata.mono_or_bi



def monoexponential(t, y0, a, T1):
	"""
	Monoexponential function, to be used during curve fitting
	"""
	return y0*(1 - ((a*a)**0.5)*np.exp(-t/T1))



def biexponential(t, a, p, T1, T2, y0):
	"""
	Biexponential function, to be used during curve fitting
	"""
	return a*(p*np.exp(-t/T1) + (1 - p)*np.exp(-t/T2)) + y0



def readInputFile(filename):
	"""
	Code for reading and preprocessing input file
	"""
	data = []
	with open(filename, 'r') as file:
		temporary_data = file.readlines()
		for i in temporary_data:
			i = i.rstrip("\n") 
			i = i.split(" ")
			i = [float(j) for j in i]
			data.append(i)

	data = np.array(data)
	data = np.transpose(data)
	np.save("data", data)



def plot_initial_data():
	"""
	Plots the initial data for viewing and estimating initial variables for curve fitting.
	
	"""
	data = np.load('data.npy')

	time = data[0]
	signal = data[1:]

	for i in range(0, len(signal)):
		plt.plot(time, signal[i])

	plt.grid()
	plt.xscale('log')
	plt.show()





def curveFit(func):
	data = np.load('data.npy')

	time = data[0]
	signal = data[1:]

	T1_array = []
	x_axis = time

	if func == "mono":
		initial_parameters = ip_monoexp
		for index, item in enumerate(signal):
			y_axis = item
			popt, pcov = curve_fit(monoexponential, x_axis, y_axis, p0=initial_parameters)
			answer = np.array(monoexponential(x_axis, popt[0], popt[1], popt[2]))
			T1_array.append((1/popt[2]))
			initial_parameters = [popt[0], popt[1], popt[2]]
	elif func == "bi":
		initial_parameters = ip_biexp
		for index, item in enumerate(signal):
			y_axis = item
			popt, pcov = curve_fit(biexponential, x_axis, y_axis, p0=initial_parameters)
			answer = np.array(biexponential(x_axis, popt[0], popt[1], popt[2], popt[3], popt[4]))
			T1_array.append((1/popt[2]))
			initial_parameters = [popt[0], popt[1], popt[2], popt[3], popt[4]]
	else:
		print("There has been breaking changes to the code. Debug it.")

	q_array = np.array([(2*math.pi*(x+1)/(256*6.5/20))**2 for x in range(0, 128)])
	# Fullsizebox = 256
	# pixels per micrometre**2 = 6.5
	# magnification = 20
	T1_array = np.array(T1_array)

	plt.scatter(q_array, T1_array)
	plt.grid()
	plt.show()





readInputFile(filename)
plot_initial_data()
if mono_or_bi == "mono":
	curveFit("mono")
elif mono_or_bi == "bi":
	curveFit("bi")
else:
	print("There is some error with the curvefitting. Debug the code")