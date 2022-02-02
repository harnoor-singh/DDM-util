import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import inputdata

# Import variables
filename = inputdata.filename

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


readInputFile(filename)
plot_initial_data()