"""
README
The following script allows to analyze individual spectral lines from Chandra observations
To use this script you must have the following files saved as indicated below:

1- Model pow+windprof:
    linename_pow+windprof.txt

2- Model pow:
    linename_pow.txt

3- Model windprof
    linename_windprof.txt

4- Line information file:
    linename_info.txt

The information file has the following form:
line_wavelength
line_name
T_star
R_o
chi_squared
pho_num
norm

Here is an example for NeX_info.txt:
12.134
Ne X
$2.92^{+0.55}_{-0.49}$
$1.02$
41.20
184
$2.70_{-0.22}^{+0.24}\times 10^{-4}$

To run the script simple type the following command:
>python3 line_spectra.py linename
"""


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


# Uploading files with data to be plotted
file = sys.argv[1]
line_data=np.genfromtxt(file+'_pow+windprof.txt', skip_header=3)
line_pow=np.genfromtxt(file+'_pow.txt',skip_header=3)
line_windprof=np.genfromtxt(file+'_windprof.txt',skip_header=3)


# Defining parameters specific to each spectral line
NeX= open(file+'_info.txt', "r") #Reading data file
info = NeX.read().splitlines() #Reading lines in the file
line_wavelength = info[0]
line_name = info[1]
T_star = info[2]
R_o = info[3]
chi_squared = info[4]
pho_num = info[5]
norm = info[6]

# Finding the number of spectrum 1 or 2 data points
domain_MEG = 0
for i in range (0, int(np.size(line_data)/5)):
    if(str(line_data[i:i+1, 0:1]) != '[[nan]]'):
        domain_MEG = domain_MEG+1
    else:
        break

domain_HEG = 0
for i in range (domain_MEG*2+2,len(line_data)):
    if(str(line_data[i:i+1, 0:1]) != '[[nan]]'):
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

wavelength = line_data[min_range:max_range, 0:1]
data_binning = line_data[min_range:max_range, 1:2]
data = line_data[min_range:max_range, 2:3]+line_data[max_range+1:max_range+domain+1, 2:3]
data_error = np.sqrt(np.square(line_data[min_range:max_range, 3:4])+np.square(line_data[max_range+1:max_range+domain+1, 3:4]))
model = line_data[min_range:max_range, 4:5]+line_data[max_range+1:max_range+domain+1,4:5]


# Defining variables of pow model
model_pow = line_pow[min_range:max_range, 4:5]+line_pow[max_range+1:max_range*2+1, 4:5]
hist_boundary_pow = np.sort(np.append(line_pow[min_range:max_range, 0:1]-line_pow[min_range:max_range, 1:2],line_pow[min_range:max_range, 0:1]+line_pow[min_range:max_range, 1:2]))[::-1]
hist_model_pow = []
for x in range(0, domain):
    model_set = float(model_pow[x])
    hist_model_pow.append(model_set)
    hist_model_pow.append(model_set)


# Defining variables of windprof/wgauss model
model_windprof = line_windprof[min_range:max_range, 4:5]+(np.max(line_data[min_range:max_range, 4:5])-np.max(line_windprof[min_range:max_range, 4:5]))+line_windprof[max_range+1:max_range*2+1, 4:5]+(np.max(line_data[max_range+1:max_range*2+1, 4:5])-np.max(line_windprof[max_range+1:max_range*2+1, 4:5]))
hist_boundary_windprof = np.sort(np.append(line_windprof[min_range:max_range, 0:1]-line_windprof[min_range:max_range, 1:2],line_windprof[min_range:max_range, 0:1]+line_windprof[min_range:max_range, 1:2]))[::-1]
hist_model_windprof = []
for x in range(0, domain):
    model_set = float(model_windprof[x])
    hist_model_windprof.append(model_set)
    hist_model_windprof.append(model_set)


#Plotting the graph
#Determining plot size and labeling the plot

plt.figure(figsize = (10, 8))
plt.xlabel('Wavelength($\AA$)', fontname=tnr, fontsize=23)
plt.ylabel('normalized counts $(s^{-1}\AA^{-1})$', fontname=tnr, fontsize=23)
plt.xticks(fontname=tnr, fontsize=19)
plt.yticks(fontname=tnr, fontsize=19)


#Plotting data points and their error bars and bin widths
plt.plot(wavelength, data, 'o', color='black', markersize=4)
plt.errorbar(wavelength,data,xerr=data_binning, ls='none', color='black', linewidth=0.5,capsize=1.5,capthick=1)

#Poisson error
photon_number=data*2*data_binning*67730 # 67730 is the exposure time
poisson_error=np.divide(np.sqrt(photon_number),(2*data_binning*67730))
plt.errorbar(wavelength,data,yerr=poisson_error, ls='none', color='black', linewidth=0.5,capsize=1.5,capthick=1)
plt.ylim(bottom=0.00)


#Creating histogram for pow model
plt.plot(hist_boundary_pow, hist_model_pow, color='lightcoral',linestyle='dashed', markersize=1.5, linewidth=1.5)


#Creating histogram for windprof/wgauss model
plt.plot(hist_boundary_windprof, hist_model_windprof, color='lightcoral', markersize=1.5, linewidth=1.5)
plt.fill_between(hist_boundary_windprof,hist_model_windprof, hist_model_pow , color='lightgrey')

#Add text about model parameters, parameters depend on specific spectral line, must be changed for each spectral line

plt.figtext(0.64,0.83,r'$\lambda$ = '+line_wavelength+'$\AA$ '+line_name, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.775,r'$\tau_{\star}$ = '+T_star, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.72,r'$R_o$ = '+R_o, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.665,r'$\chi^2$ = '+chi_squared, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.61,'N = '+pho_num, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.555,'norm = '+norm, fontname=tnr, fontsize=19)
plt.savefig(file+'_'+line_tp+'_spectra.png')
plt.show()
