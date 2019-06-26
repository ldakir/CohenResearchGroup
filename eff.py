"""
README

To run the script simple type the following command:
python3 eff.py


"""

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
    contents = np.genfromtxt(file,skip_header=3)
    return contents



data = get_data('640_eff.txt')


# Finding the number of spectrum 1 or 2 data points
domain_MEG = 0
for i in range (0, int(np.size(data)/5)):
    if(str(data[i:i+1, 0:1]) != '[[nan]]'):
        domain_MEG = domain_MEG+1
    else:
        break

domain_HEG = 0
for i in range (domain_MEG*2+2,len(data)):
    if(str(data[i:i+1, 0:1]) != '[[nan]]'):
        domain_HEG = domain_HEG+1
    else:
        break


#Choosing MEG or HEG
#If you want MEG type 0 else type 1
line_type = 0


#Defining variables of windprof/wgauss+pow data points
if line_type == 0:
    min_range = 0
    max_range = domain_MEG
    domain = domain_MEG
    line_tp = 'MEG'
else:
    min_range= domain_MEG*2+2
    max_range = domain_HEG+min_range
    domain = domain_HEG
    line_tp = 'HEG'




ObsID= '640'
wavelength = data[min_range:max_range, 0]
data_binning = data[min_range:max_range, 1]
data_val = data[min_range:max_range, 2]
data_error =np.square(data[min_range:max_range, 3])
model = data[min_range:max_range, 4]/0.08065

data2 = get_data('21661_eff.txt')
ObsID_2= '21661'
wavelength_2 = data2[min_range:max_range, 0]
data_binning_2 = data2[min_range:max_range, 1]
data_val_2 = data2[min_range:max_range, 2]
data_error_2 =np.square(data2[min_range:max_range, 3])
model_2 = data2[min_range:max_range, 4]/0.08065

data3 = get_data('21659_eff.txt')
ObsID_3= '21659'
wavelength_3 = data3[min_range:max_range, 0]
data_binning_3 = data3[min_range:max_range, 1]
data_val_3 = data3[min_range:max_range, 2]
data_error_3 =np.square(data3[min_range:max_range, 3])
model_3 = data3[min_range:max_range, 4]/0.08065

data4 = get_data('20157_eff.txt')
ObsID_4= '20157'
wavelength_4 = data4[min_range:max_range, 0]
data_binning_4 = data4[min_range:max_range, 1]
data_val_4 = data4[min_range:max_range, 2]
data_error_4 =np.square(data4[min_range:max_range, 3])
model_4 = data4[min_range:max_range, 4]/0.08065


# Plotting the graph
# determining plot size and labeling the plot

plt.figure(figsize = (24, 7))
plt.xlabel('Wavelength ($\AA$)', fontname=tnr, fontsize=21)
plt.ylabel('Effective Area ($cm^{2}$)', fontname=tnr, fontsize=21)
plt.xticks(fontname=tnr, fontsize=18)
plt.yticks(fontname=tnr, fontsize=18)
plt.xticks(np.arange(0, max(wavelength)+1, 5))
plt.plot(wavelength, model, '-', color='mediumblue', markersize= 0.4, label = '640')
plt.plot(wavelength_2, model_2, '-', color='r', markersize= 0.4, label = '21661')
plt.plot(wavelength_3, model_3, '-', color='g', markersize= 0.4, label = '21659')
plt.plot(wavelength_4, model_4, '-', color='k', markersize= 0.4, label = '20157')
plt.figtext(0.8,0.83, 'ObsID: 640',color ='mediumblue' ,fontname=tnr, fontsize=21)
plt.figtext(0.8,0.78,'ObsID: 21661',color='r', fontname=tnr, fontsize=21)
plt.figtext(0.8,0.73,'ObsID: 20157',color='k', fontname=tnr, fontsize=21)
plt.figtext(0.8,0.68,'ObsID: 21659',color='g', fontname=tnr, fontsize=21)
plt.xlim(4,25.5)
plt.savefig('eff_data.png')
plt.show()
