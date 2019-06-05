"""
README
The following script allows to look at taustar, Ro, and norm vs lambda for each observation.
Note: The norm for each line in each of the three new observations is ratioed to the norm from the cycle 1 observation

To use this script you must have the following files saved as indicated below:

1- ObsID_info.txt: has observations from the target cycle

2- parameters.txt: has observations from cycle 1

To run the script simple type the following command:
>python3 cycle_analysis.py ObsID_info.txt parameters.txt arg

arg could be norm, taustar or Ro 
"""

#python3 taustar_analysis.py datafile.txt cycle1.txt
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
cycle = sys.argv[1].split('_')[0]
cycle1_data = get_data(sys.argv[2])
size_data = len(data)
size_cycle1 =len(cycle1_data)
data_name= sys.argv[3]
if data_name == 'norm':
    wavelength = data[0:size_data,0]
    cycle1_wavelength = cycle1_data[0:size_cycle1,0]
    data_type =[]
    min_error =[]
    max_error=[]
    for j in range(len(data)):
        for i in range(len(cycle1_data)):
            if(wavelength[j]== cycle1_wavelength[i]):

                data_type.append(data[j,1]/cycle1_data[i,7])

                min_error.append(data[j,2]/cycle1_data[i,7])
                max_error.append(data[j,3]/cycle1_data[i,7])

    #data_type = data[0:size_data,2]/cycle1_data[0:size_data,2]
    #min_error = data[0:size_data,3]/cycle1_data[0:size_data,3]
    #max_error= data[0:size_data,4]/cycle1_data[0:size_data,4]
    data_type =np.asarray(data_type)
    min_error =np.asarray(min_error)
    max_error =np.asarray(max_error)
    error = np.array([min_error, max_error])
    label= 'Norm '+ cycle +'/640'
elif data_name == 'taustar':
    wavelength = data[0:size_data,0]
    data_type = data[0:size_data,4]
    #print(wavelength)
    #print(data_type)
    min_error = data[0:size_data,5]
    max_error= data[0:size_data,6]
    error = np.array([min_error, max_error])
    label=r'$\tau_{\star}$'

elif data_name == 'Ro':
    wavelength = data[0:size_data,0]
    data_type = data[0:size_data,7]
    min_error = data[0:size_data,8]
    max_error= data[0:size_data,9]
    error = np.array([min_error, max_error])
    label =r'$R_o$'


#Plotting Wavelength vs Taustar with errorbars

plt.figure(figsize = (10, 8))
plt.plot(wavelength, data_type, 'k.')
plt.xlabel('Wavelength($\AA$)', fontname=tnr, fontsize=23)
plt.ylabel(label, fontname=tnr, fontsize=23)
plt.errorbar(wavelength,data_type, error, ls='none',color='red',linewidth=0.5,capsize=1.5,capthick=1)
plt.xticks(fontname=tnr, fontsize=19)
plt.yticks(fontname=tnr, fontsize=19)
plt.savefig('wavelength_vs_'+data_name +'_' +cycle)
plt.show()
