"""
README
The following script allows to analyze individual spectral lines from Chandra observations
To use this script you must have the following files saved as indicated below:

1- Model pow+windprof:
    linename_pow+windprof.txt

2- Model pow:
    linename_pow.txt

3- Information file:
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
#line_data=get_data(file+'_pow+windprof.txt')
#line_pow=get_data(file+'_pow.txt')
#line_windprof=get_data(file+'_windprof.txt')

line_data=get_data(file+'_pow+windprof.txt')
line_pow=get_data(file+'_pow.txt')

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

#Windprof/Hewind models
#For 11 data sets
wavelength = line_data[0]
data_binning = line_data[1]
data = [a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v in zip\
        (line_data[2],line_data[7],line_data[12],line_data[17],line_data[22],line_data[27],\
        line_data[32],line_data[37],line_data[42],line_data[47],line_data[52],line_data[57],\
        line_data[62],line_data[67],line_data[72],line_data[77],line_data[82],line_data[87],\
        line_data[92],line_data[97],line_data[102],line_data[107])]

data_error = np.sqrt(np.square(line_data[3])+np.square(line_data[8])+np.square(line_data[13])+np.square(line_data[18])+np.square(line_data[23])+np.square(line_data[28])+\
            np.square(line_data[33])+np.square(line_data[38])+np.square(line_data[43])+np.square(line_data[48])+np.square(line_data[53])+np.square(line_data[58])+\
            np.square(line_data[63])+np.square(line_data[68])+np.square(line_data[73])+np.square(line_data[78])+np.square(line_data[83])+np.square(line_data[88])+\
            np.square(line_data[93])+np.square(line_data[98])+np.square(line_data[103])+np.square(line_data[108]))\



model = [a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v in zip\
        (line_data[4],line_data[9],line_data[14],line_data[19],line_data[24],line_data[29],\
        line_data[34],line_data[39],line_data[44],line_data[49],line_data[54],line_data[59],\
        line_data[64],line_data[69],line_data[74],line_data[79],line_data[84],line_data[89],\
        line_data[94],line_data[99],line_data[104],line_data[109])]


#Windprof Histogram Modeling
hist_model= []
for x in model:
    hist_model.append(x)
    hist_model.append(x)


hist_boundary=[]
for i in range(len(model)):
    hist_boundary.append(wavelength[i]+data_binning[i])
    hist_boundary.append(wavelength[i]-data_binning[i])


#Powerlaw Histogram Modeling


data_binning_pow = line_pow[1]
data_pow = [a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v in zip\
        (line_pow[2],line_pow[7],line_pow[12],line_pow[17],line_pow[22],line_pow[27],\
        line_pow[32],line_pow[37],line_pow[42],line_pow[47],line_pow[52],line_pow[57],\
        line_pow[62],line_pow[67],line_pow[72],line_pow[77],line_pow[82],line_pow[87],\
        line_pow[92],line_pow[97],line_pow[102],line_pow[107])]

data_error_pow = np.sqrt(np.square(line_pow[3])+np.square(line_pow[8])+np.square(line_pow[13])+np.square(line_pow[18])+np.square(line_pow[23])+np.square(line_pow[28])+\
            np.square(line_pow[33])+np.square(line_pow[38])+np.square(line_pow[43])+np.square(line_pow[48])+np.square(line_pow[53])+np.square(line_pow[58])+\
            np.square(line_pow[63])+np.square(line_pow[68])+np.square(line_pow[73])+np.square(line_pow[78])+np.square(line_pow[83])+np.square(line_pow[88])+\
            np.square(line_pow[93])+np.square(line_pow[98])+np.square(line_pow[103])+np.square(line_pow[108]))\



model_pow = [a+b+c+d+e+f+g+h+i+j+k+l+m+n+o+p+q+r+s+t+u+v for a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v in zip\
        (line_pow[4],line_pow[9],line_pow[14],line_pow[19],line_pow[24],line_pow[29],\
        line_pow[34],line_pow[39],line_pow[44],line_pow[49],line_pow[54],line_pow[59],\
        line_pow[64],line_pow[69],line_pow[74],line_pow[79],line_pow[84],line_pow[89],\
        line_pow[94],line_pow[99],line_pow[104],line_pow[109])]


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
plt.xlabel('Wavelength ($\AA$)', fontname=tnr, fontsize=23)
plt.ylabel('normalized counts $(s^{-1}\AA^{-1})$', fontname=tnr, fontsize=23)
plt.xticks(fontname=tnr, fontsize=19)
plt.yticks(fontname=tnr, fontsize=19)


#Plotting data points and their error bars and bin widths
plt.plot(wavelength, data, 'o', color='black', markersize=4)
plt.errorbar(wavelength,data,xerr=data_binning, ls='none', color='black', linewidth=0.5,capsize=1.5,capthick=1)

#Poisson error
exposure_time= 46970+15510+18410+26860+29700+17720+19690+18090+43390+14950+27690+67730
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
plt.plot(hist_boundary, hist_model, color='lightcoral', markersize=1.5, linewidth=1.5)
plt.fill_between(hist_boundary,hist_model, hist_model_pow , color='lightgrey')

#Add text about model parameters, parameters depend on specific spectral line, must be changed for each spectral line
plt.figtext(0.64,0.83, 'ObsID: '+ObsID, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.773,r'$\lambda$ = '+str(line_wavelength)+'Å '+line_name, fontname=tnr, fontsize=19)
plt.figtext(0.64,0.716,'norm = '+ str('{:.2f}'.format(round(float(norm)*1E4, 2)))+'$_{'+str('{:.2f}'.format(round(-float(norm_lower_error)*1E4, 2)))+'}'+'^{+'+str('{:.2f}'.format(round(float(norm_upper_error)*1E4, 2)))+'}$'+r'$\times 10^{-4}$' , fontname=tnr, fontsize=19)
plt.figtext(0.64,0.659,r'$\tau_{\star}$ = '+ str('{:.2f}'.format(round(float(T_star), 2)))+'$_{'+str('{:.2f}'.format(round(-float(t_lower_error), 2)))+'}'+'^{+'+str('{:.2f}'.format(round(float(t_upper_error), 2)))+'}$', fontname=tnr, fontsize=19)
plt.figtext(0.64,0.602,r'$R_o$ = '+ str('{:.2f}'.format(round(float(Ro), 2)))+'$_{'+str('{:.2f}'.format(round(-float(Ro_lower_error), 2)))+'}'+'^{+'+str('{:.2f}'.format(round(float(Ro_upper_error), 2)))+'}$', fontname=tnr, fontsize=19)
if photon_num == 0:
    plt.figtext(0.64,0.545,r'$N_{MEG}$ = '+str(pho_num), fontname=tnr, fontsize=19)
else:
    plt.figtext(0.64,0.545,r'$N_{HEG}$ = '+str(pho_num), fontname=tnr, fontsize=19)
plt.figtext(0.64,0.488,r'$\chi^2$ = '+str(chi_squared), fontname=tnr, fontsize=19)

plt.savefig(file+'_'+line_tp+'_spectra.png')
plt.show()
