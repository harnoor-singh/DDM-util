import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit 


# Change the filename here
filename = '../inputfiles/DDM_newest.dat'
# filename = '../inputfiles/ps1micron_0.1mgmlDDM_Nanoparticles_MaxNc500.dat'



data = []

# Code for reading input data file
with open(filename, 'r') as file:
	temporary_data = file.readlines()
	for i in temporary_data:
		i = i.rstrip("\n") 
		i = i.split(" ")
		i = [float(j) for j in i]
		data.append(i)



data = np.array(data)
data_two = np.transpose(data)

np.save("data", data_two)

time = data_two[0]
signal = data_two[1:]



for i in range(0, len(signal)):
	plt.plot(time, signal[i])

plt.grid()
plt.xscale('log')
plt.show()
