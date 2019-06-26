"""
README

To run the script simple type the following command:
python3 spectra_data.py ObsID


"""
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import math


# specifying Times New Roman font and to force that withing plotting commands
tnr='Times New Roman'
params ={'mathtext.default':'regular'}
plt.rcParams.update(params)


ObsID= sys.argv[1]
# Uploading data to be plotted
all_data=np.genfromtxt(ObsID+'_data.txt',skip_header=3)

# Finding the number of spectrum 1 or 2 data points
domain = 0
for i in range (0, int(np.size(all_data)/5)):
    if(str(all_data[i:i+1, 0:1]) != '[[nan]]'):
        domain = domain+1
    else:
        break



# defining variables of windprof/wgauss+pow data points
wavelength = all_data[(int)(domain/3):domain, 0:1]
data_binning = all_data[(int)(domain/3):domain, 1:2]
data = all_data[(int)(domain/3):domain, 2:3]+all_data[domain+(int)(domain/3)+1:domain*2+1, 2:3]
data_error = np.sqrt(np.square(all_data[(int)(domain/3):domain, 3:4])+np.square(all_data[domain+(int)(domain/3)+1:domain*2+1, 3:4]))

# Plotting the graph
# determining plot size and labeling the plot

plt.figure(figsize = (24, 7))

plt.xlabel('Wavelength ($\AA$)', fontname=tnr, fontsize=21)
plt.ylabel('normalized counts $(s^{-1}\AA^{-1})$', fontname=tnr, fontsize=21)
plt.xticks(fontname=tnr, fontsize=18)
plt.yticks(fontname=tnr, fontsize=18)

# plotting data points and their error bars and bin widths

plt.plot(wavelength, data, 'o', color='black', markersize= 0.4)
plt.xticks(np.arange(0, max(wavelength)+1, 5))
plt.errorbar(wavelength,data,xerr=data_binning, ls='none', color='black' ,linewidth=0.2,capsize=None,capthick=0.5)

#poisson error
photon_number=data*2*data_binning*67730 # 67730 is the exposure time
poisson_error=np.divide(np.sqrt(photon_number),(2*data_binning*67730))
plt.errorbar(wavelength,data,yerr=poisson_error, ls='none', color='black', linewidth=0.2,capsize=None,capthick=0.5)
plt.figtext(0.8,0.83, 'ObsID: '+ObsID, fontname=tnr, fontsize=21)
plt.figtext(0.8,0.78, 'Date: '+ '2000 Mar 28',fontname=tnr, fontsize=21)
plt.ylim(0,0.25)
plt.xlim(4,25.5)
plt.savefig(ObsID+'_data.png')
plt.show()
