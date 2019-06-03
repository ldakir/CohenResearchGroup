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
taustar_old = data[0:size_data,1]
min_error_old = data[0:size_data,2]
max_error_old= data[0:size_data,3]
error_old = np.array([min_error_old, max_error_old])
taustar_new = data[0:size_data,4]
min_error_new = data[0:size_data,5]
max_error_new= data[0:size_data,6]
error_new = np.array([min_error_new, max_error_new])

#Plotting Wavelength vs Taustar with errorbars
plt.figure(figsize = (10, 8))
plt.plot(taustar_old, taustar_new, 'ko')
plt.xlabel(r'$\tau_{\star}$', fontname=tnr, fontsize=23)
plt.ylabel(r'$\tau_{\star}$', fontname=tnr, fontsize=23)
plt.errorbar(taustar_old, taustar_new, yerr= error_new, ls='none',color='red',linewidth=0.5,capsize=1.5,capthick=1)
plt.errorbar(taustar_old, taustar_new, xerr= error_old, ls='none',color='blue',linewidth=0.5,capsize=1.5,capthick=1)

x =[0,1,2,3,4]
y =[0,1,2,3,4]
plt.plot(x,y,'g-')
plt.xticks(fontname=tnr, fontsize=19)
plt.yticks(fontname=tnr, fontsize=19)
plt.show()
