import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

import inputdata


# Import variables
filename = inputdata.filename

fullSizeBox = inputdata.fullSizeBox
pixels_per_mm_sq = inputdata.pixels_per_micrometre_squared
magnification = inputdata.magnification

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
			# answer = np.array(monoexponential(x_axis, popt[0], popt[1], popt[2]))
			T1_array.append((1/popt[2]))
			initial_parameters = [popt[0], popt[1], popt[2]]
	elif func == "bi":
		initial_parameters = ip_biexp
		for index, item in enumerate(signal):
			y_axis = item
			popt, pcov = curve_fit(biexponential, x_axis, y_axis, p0=initial_parameters)
			# answer = np.array(biexponential(x_axis, popt[0], popt[1], popt[2], popt[3], popt[4]))
			T1_array.append((1/popt[2]))
			initial_parameters = [popt[0], popt[1], popt[2], popt[3], popt[4]]
	else:
		print("There has been breaking changes to the code. Debug it.")

	q_array = np.array([(2*math.pi*(x+1)/(fullSizeBox*pixels_per_mm_sq/magnification))**2 for x in range(0, 128)])
	"""
	q_array is actually q squared.
	"""
	T1_array = np.array(T1_array)

	np.save('q_array', q_array)
	np.save('T1_array', T1_array)

	plt.scatter(q_array, T1_array)
	plt.grid()
	plt.show()




if mono_or_bi == "mono":
	curveFit("mono")
elif mono_or_bi == "bi":
	curveFit("bi")
else:
	print("There is some error with the curvefitting. Debug the code")