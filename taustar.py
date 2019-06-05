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
data1 = get_data(sys.argv[1])
data1_name= sys.argv[1].split('_')[0]
size_data = len(data1)

#Storing data
taustar_1 = data1[0:size_data,1]
min_error_1 = data1[0:size_data,2]
max_error_1= data1[0:size_data,3]
error_1 = np.array([min_error_1, max_error_1])

data2 = get_data(sys.argv[2])
data2_name=sys.argv[2].split('_')[0]
size_data2 = len(data2)
taustar_2 = data2[0:size_data2,1]
min_error_2 = data2[0:size_data2,2]
max_error_2= data2[0:size_data2,3]
error_2 = np.array([min_error_2, max_error_2])


#Plotting Wavelength vs Taustar with errorbars
plt.figure(figsize = (10, 8))
plt.plot(taustar_1, taustar_2, 'ko')
plt.xlabel(data1_name+ ' '+r'$ \tau_{\star}$', fontname=tnr, fontsize=23)
plt.ylabel(data2_name+' '+r'$ \tau_{\star}$', fontname=tnr, fontsize=23)
plt.errorbar(taustar_1, taustar_2, yerr= error_2, ls='none',color='lightgrey',linewidth=0.5,capsize=1.5,capthick=1)
plt.errorbar(taustar_1, taustar_2, xerr= error_1, ls='none',color='lightgrey',linewidth=0.5,capsize=1.5,capthick=1)

x =[0,1,2,3,4]
y =[0,1,2,3,4]
plt.plot(x,y,'r-')
plt.xticks(fontname=tnr, fontsize=19)
plt.yticks(fontname=tnr, fontsize=19)
plt.savefig('Taustar'+data1_name+'vs'+data2_name)
plt.show()
