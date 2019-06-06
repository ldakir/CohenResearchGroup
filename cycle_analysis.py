"""
README
The following script allows to look at taustar, Ro, and norm vs lambda for each observation.
Note: The norm for each line in each of the three new observations is ratioed to the norm from the cycle 1 observation

To use this script you must have the following files saved as indicated below:

1- ObsID_info.txt: has observations from the target cycle

2- parameters.txt: has observations from cycle 1

To run the script simple type the following command:
>python3 cycle_analysis.py  parameters.txt  arg ObsID_info.txt

arg could be norm, taustar or Ro
"""

"""NOTE TO SEFL : double check NORM"""

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

#Importing data
def get_data(file):
    contents = np.genfromtxt(file,skip_header=1)
    return contents

#Argument 1: Cycle_1 data
cycle1_data = get_data(sys.argv[1])
data_name= sys.argv[2]
size_cycle1 =len(cycle1_data)
cycle1_wavelength= cycle1_data[0:size_cycle1,0]


#Importing wavelength values
def get_wavelength(data):
    wavelength = data[0:len(data),0]
    return wavelength

#Importing Norm/Taustar/Ro values
def get_data_vals(data):
    data_val = []
    if data_name == 'norm':
        for j in range(len(data)):
            for i in range(len(cycle1_data)):
                if(get_wavelength(data)[j]== cycle1_wavelength[i]):
                    data_val.append(data[j,1]/cycle1_data[i,7])
        data_val =np.asarray(data_val)
        label= 'Norm'

    elif data_name == 'taustar':
        data_val = data[0:len(data),4]
        label= 'Taustar'

    elif data_name == 'Ro':
        data_val = data[0:len(data),7]
        label= 'Ro'

    return data_val,label


#Importing error values
def get_error(data):
    min_error =[]
    max_error=[]
    error = []
    if data_name == 'norm':
        for j in range(len(data)):
            for i in range(len(cycle1_data)):
                if(get_wavelength(data)[j]== cycle1_wavelength[i]):
                    min_error.append(data[j,2]/cycle1_data[i,7])
                    max_error.append(data[j,3]/cycle1_data[i,7])
        min_error =np.asarray(min_error)
        max_error =np.asarray(max_error)
        error = np.array([min_error, max_error])

    elif data_name == 'taustar':
        min_error = data[0:len(data),5]
        max_error= data[0:len(data),6]
        error = np.array([min_error, max_error])
    elif data_name == 'Ro':
        min_error = data[0:len(data),8]
        max_error= data[0:len(data),9]
        error = np.array([min_error, max_error])
    return error

#Making a model for chi squared
def model(data_name, data, max_error, min_error):
    if data_name =='norm' or data_name =='Ro':
    #Chi-squared model
        chisquared=[]
        steps = np.linspace(np.min(data), np.max(data), 1000)
        for m in steps:
            result = 0
            for d in range(0,len(data)):
                result += ((m-data[d])/(min_error[d] if data[d]>m else max_error[d] ))**2
            chisquared.append(result)
        model_val = steps[chisquared.index(np.min(chisquared))]
        reduced_chisquared= np.min(chisquared)/(len(data)-1)
        return model_val,reduced_chisquared

def plotting(file,color_plot, color_error):
    data = get_data(file)
    wavelength = get_wavelength(data)
    data_val,label = get_data_vals(data)
    error = get_error(data)
    model_val,reduced_chisquared = model(data_name,data_val,error[1], error[0])
    plt.figure(figsize = (10, 8))
    plt.plot(wavelength, data_val, color_plot)
    plt.xlabel('Wavelength($\AA$)', fontname=tnr, fontsize=23)
    plt.ylabel(label, fontname=tnr, fontsize=23)
    plt.errorbar(wavelength,data_val, error, ls='none',color=color_error,linewidth=0.5,capsize=1.5,capthick=1)
    plt.axhline(y=model_val, color='r', linestyle='-')
    plt.xticks(fontname=tnr, fontsize=19)
    plt.yticks(fontname=tnr, fontsize=19)
    plt.figtext(0.68,0.83, 'ObsID: '+ObsID, fontsize=19)
    plt.figtext(0.68,0.78, data_name+' = '+str(np.around(model_val, 3)), fontsize=19)
    plt.figtext(0.68,0.73, r'reduced $\chi^2$ = '+str(np.around(reduced_chisquared, 3)), fontsize=19)
    plt.savefig('wavelength_vs_'+data_name+ObsID)
    plt.show()



#Argument 3: Type of data
ObsID = sys.argv[3].split('_')[0]
plotting(sys.argv[3],'k.', 'lightgrey')


if(sys.argv[4]):
    ObsID= sys.argv[4].split('_')[0]
    plotting(sys.argv[4],'b.', 'lightblue')
if(sys.argv[5]):
    ObsID= sys.argv[5].split('_')[0]
    plotting(sys.argv[5],'g.', 'lightgreen')
