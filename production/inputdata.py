# Configure all variables here!

filename = 'C:\\Users\\harno\\Desktop\\DDM-util\\inputfiles\\DDM_newest.dat'
# filename = 'ps1micron_0.1mgmlDDM_Nanoparticles_MaxNc500.dat'
"""
Filename for input data.
Either enter full path or relative path of the file (relative to main.py)
"""


fullSizeBox = 256
"""
Size of the sqaure image (in pixels) which was analyzed
"""

pixels_per_micrometre_squared = 6.5
"""
TODO
"""

magnification = 20
"""
TODO
"""


initial_parameters_monoexponential = [35, 0.5, 0.1]
"""
Set initial parameters for monoexponential curve fitting
The equation for monoexponential is: y0*(1 - ((a*a)**0.5)*np.exp(-t/T1))
The order of initial parameters should be: [y0, a, T1]. All numbers are necessary to enter
I cannot change the order, because of how the scipy.optimize.curve_fit works
The order matters!!!
"""

initial_parameters_biexponential = [] # [a, p, T1, T2, y0]
"""
Set initial parameters for biexponential curve fitting
The equation for monoexponential is: a*(p*np.exp(-t/T1) + (1 - p)*np.exp(-t/T2)) + y0
The order of initial parameters should be: [a, p, T1, T2, y0]. All numbers are necessary to enter
I cannot change the order, because of how the scipy.optimize.curve_fit works
The order matters!!!
"""

mono_or_bi = "mono"
"""
Set as "mono" (with quotes) for monoexponential curve fitting
Set as "bi" (with quotes) for biexponential curve fitting
Examples:
mono_or_bi = "mono"
mono_or_bi = "bi"
"""