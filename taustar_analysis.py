# Importing libraries
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import math

# Specifying Times New Roman font and to force that withing plotting commands
tnr='Times New Roman'
params ={'mathtext.default':'regular'}
plt.rcParams.update(params)

#Function to import data
def get_data(file):
    contents = np.genfromtxt(file,skip_header=1)
    return contents

#Importing data
data = get_data(sys.argv[1])
size_data = len(data)

#Storing data
wavelength = data[0:size_data,0]
taustar = data[0:size_data,1]
min_error = data[0:size_data,2]
max_error= data[0:size_data,3]

error = np.array([min_error, max_error])

#Plotting Wavelength vs Taustar with errorbars
plt.figure(figsize = (10, 8))
plt.plot(wavelength, taustar, 'k.')
plt.xlabel('Wavelength($\AA$)', fontname=tnr, fontsize=23)
plt.ylabel(r'$\tau_{\star}$', fontname=tnr, fontsize=23)
plt.errorbar(wavelength,taustar, error, ls='none',color='red')
plt.xticks(fontname=tnr, fontsize=19)
plt.yticks(fontname=tnr, fontsize=19)
plt.show()
