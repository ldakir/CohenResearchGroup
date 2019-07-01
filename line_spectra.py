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

4- Information file:
    ObsID_info.txt

The information file has the following information:
line_wavelength
line_name
T_star
R_o
chi_squared
pho_num
norm


To run the script simple type the following command:
>python3 line_spectra.py linename ObsID
"""


# Importing libraries
import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import math
from io import StringIO


# Specifying Times New Roman font and to force that withing plotting commands
tnr='Times New Roman'
params ={'mathtext.default':'regular'}
plt.rcParams.update(params)


# Uploading files with data to be plotted

tnr='Times New Roman'
params ={'mathtext.default':'regular'}
#pow+windprof
def get_data(file):
    NeX= open(file, "r") #Reading data file
    contents = NeX.readlines() #Reading lines in the file
    data = [] #Initializing data array

    for x in contents:
        lines = x.split() #Splitting lines
        #data_val.append(lines[])
        data.append(lines)
    data = data[3:] #Removing the first three line

    data_vals = [] #Storing the data values for channel 1
    models = [] #Storing the model for channel 1
    wavelengths =[] #Storing the wavelength
    bin_widths = []
    error_bars =[]

    channels =[]
    for i in range(len(data)):
        if(data[i][0] != "NO"):
            wavelengths.append(float(data[i][0])) #wavelength values
            models.append(float(data[i][4])) #model values
            data_vals.append(float(data[i][2])) #data values
            bin_widths.append(float(data[i][1]))
            error_bars.append(float(data[i][3]))
        else:

            channels.append(wavelengths)
            channels.append(bin_widths)
            channels.append(data_vals)
            channels.append(error_bars)
            channels.append(models)
            data_vals = [] #Storing the data values for channel 1
            models = [] #Storing the model for channel 1
            wavelengths =[] #Storing the wavelength
            bin_widths = []
            error_bars =[]
            continue
        channels.append(wavelengths)
        channels.append(bin_widths)
        channels.append(data_vals)
        channels.append(error_bars)
        channels.append(models)
    return channels


file = sys.argv[1]
line_data=get_data(file+'_pow+windprof.txt')
line_pow=get_data(file+'_pow.txt')
line_windprof=get_data(file+'_windprof.txt')



ObsID = sys.argv[2]
# Defining parameters specific to each spectral line
info = np.genfromtxt(ObsID+'_info.txt', skip_header=1)

NeX= open(ObsID+'_info.txt', "r") #Reading data file
contents = NeX.readlines() #Reading lines in the file
name_info = [] #Initializing data array

for x in contents:
    lines = x.split() #Splitting lines
    #data_val.append(lines[])
    name_info.append(lines)
name_info = name_info[1:] #Removing the first three line

for i in range(len(info)):
    if file== name_info[i][12]:
        line_wavelength = info[i,0]
        norm = info[i,1]
        norm_lower_error= info[i,2]
        norm_upper_error = info[i,3]
        T_star = info[i,4]
        t_lower_error = info[i,5]
        t_upper_error = info[i,6]
        Ro = info[i,7]
        Ro_lower_error = info[i,8]
        Ro_upper_error = info[i,9]
        chi_squared = info[i,10]
        pho_num = info[i,11]
        line_name = name_info[i][13]+ ' '+ name_info[i][14]


v_terminal= 2250

#defining shifted wavelengths
shifted_wavelengths = [float(line_wavelength)*(1+v_terminal/(3*(10**5))), float(line_wavelength)*(1-v_terminal/(3*(10**5)))]


#Choosing MEG or HEG
#If you want MEG type 0 else type 1
line_type = 0

# If the fit is based on just MEG type 0, if the fit is based on MEG+HEG type 1
photon_num = 0

#Defining variables of windprof/wgauss+pow data points
if line_type == 0:
    line_tp = 'MEG'
else:
    line_tp = 'HEG'


wavelength = line_data[0]
data_binning = line_data[1]
data = [a+b+c+d+e+f for a,b,c,d,e,f in zip(line_data[2],line_data[7],line_data[12],line_data[17],line_data[22],line_data[27])]
data_error = np.sqrt(np.square(line_data[3])+np.square(line_data[8])+np.square(line_data[13])+np.square(line_data[18])+np.square(line_data[23])+np.square(line_data[28]))
model = [a+b+c+d+e+f for a,b,c,d,e,f in zip(line_data[4],line_data[9],line_data[14],line_data[19],line_data[24],line_data[29])]

#Windprof Histogram Modeling
data_binning_windprof = line_windprof[1]
data_windprof = [a+b+c+d+e+f for a,b,c,d,e,f in zip(line_windprof[2],line_windprof[7],line_windprof[12],line_windprof[17],line_windprof[22],line_windprof[27])]
data_error_windprof = np.sqrt(np.square(line_windprof[3])+np.square(line_windprof[8])+np.square(line_windprof[13])+np.square(line_windprof[18])+np.square(line_windprof[23])+np.square(line_windprof[28]))
model_windprof = [a+b+c+d+e+f for a,b,c,d,e,f in zip(line_windprof[4],line_windprof[9],line_windprof[14],line_windprof[19],line_windprof[24],line_windprof[29])]


model_raised = model_windprof+(np.max(model)-np.max(model_windprof))
hist_model_windprof = []
for x in model_raised:
    hist_model_windprof.append(x)
    hist_model_windprof.append(x)


hist_boundary_windprof =[]
for i in range(len(model)):
    hist_boundary_windprof.append(wavelength[i]+data_binning_windprof[i])
    hist_boundary_windprof.append(wavelength[i]-data_binning_windprof[i])


#Powerlaw Histogram Modeling
data_binning_pow = line_pow[1]
data_pow = [a+b+c+d+e+f for a,b,c,d,e,f in zip(line_pow[2],line_pow[7],line_pow[12],line_pow[17],line_pow[22],line_pow[27])]
data_error_pow = np.sqrt(np.square(line_pow[3])+np.square(line_pow[8])+np.square(line_pow[13])+np.square(line_pow[18])+np.square(line_pow[23])+np.square(line_pow[28]))
model_pow = [a+b+c+d+e+f for a,b,c,d,e,f in zip(line_pow[4],line_pow[9],line_pow[14],line_pow[19],line_pow[24],line_pow[29])]



hist_model_pow = []
for x in model_pow:
    hist_model_pow.append(x)
    hist_model_pow.append(x)


hist_boundary_pow =[]
for i in range(len(model)):
    hist_boundary_pow.append(wavelength[i]+data_binning_pow[i])
    hist_boundary_pow.append(wavelength[i]-data_binning_pow[i])


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
exposure_time= 67730
photon_number= [i*2*j*exposure_time for i,j in zip(data,data_binning)]
poisson_error=np.divide(np.sqrt(photon_number),([2*i*exposure_time for i in data_binning]))
plt.errorbar(wavelength,data,yerr=poisson_error, ls='none', color='black', linewidth=0.5,capsize=1.5,capthick=1)
plt.ylim(bottom=0.00)


#Creating histogram for pow model
plt.plot(hist_boundary_pow, hist_model_pow, color='lightcoral',linestyle='dashed', markersize=1.5, linewidth=1.5)


# drawing vertical lins to indicate rest wavelengths
plt.vlines(float(line_wavelength), ymin=0, ymax = 1, color='grey', linestyle='--', linewidth = 1.3)
plt.vlines(shifted_wavelengths, ymin=0, ymax = 1, color='grey', linestyle=':', linewidth = 1.)

#Creating histogram for windprof/wgauss model
plt.plot(hist_boundary_windprof, hist_model_windprof, color='lightcoral', markersize=1.5, linewidth=1.5)
plt.fill_between(hist_boundary_windprof,hist_model_windprof, hist_model_pow , color='lightgrey')

#Add text about model parameters, parameters depend on specific spectral line, must be changed for each spectral line
plt.figtext(0.64,0.83, 'ObsID: '+ObsID, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.773,r'$\lambda$ = '+str(line_wavelength)+'Å '+line_name, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.716,'norm = '+ str('{:.2f}'.format(round(float(norm)*1E5, 2)))+'$_{'+str('{:.2f}'.format(round(-float(norm_lower_error)*1E5, 2)))+'}'+'^{+'+str('{:.2f}'.format(round(float(norm_upper_error)*1E5, 2)))+'}$' , fontname=tnr, fontsize=19)
plt.figtext(0.64,0.659,r'$\tau_{\star}$ = '+ str('{:.2f}'.format(round(float(T_star), 2)))+'$_{'+str('{:.2f}'.format(round(-float(t_lower_error), 2)))+'}'+'^{+'+str('{:.2f}'.format(round(float(t_upper_error), 2)))+'}$', fontname=tnr, fontsize=19)
plt.figtext(0.64,0.602,r'$R_o$ = '+ str('{:.2f}'.format(round(float(Ro), 2)))+'$_{'+str('{:.2f}'.format(round(-float(Ro_lower_error), 2)))+'}'+'^{+'+str('{:.2f}'.format(round(float(Ro_upper_error), 2)))+'}$', fontname=tnr, fontsize=19)
if photon_num == 0:
    plt.figtext(0.64,0.545,r'$N_{MEG}$ = '+str(pho_num), fontname=tnr, fontsize=19)
else:
    plt.figtext(0.64,0.545,r'$N_{MEG+HEG}$ = '+str(pho_num), fontname=tnr, fontsize=19)
plt.figtext(0.64,0.488,r'$\chi^2$ = '+str(chi_squared), fontname=tnr, fontsize=19)

plt.savefig(file+'_'+line_tp+'_spectra.png')
plt.show()
