import sys
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import pylab
import math
from scipy.interpolate import interp1d
# Specifying Times New Roman font and to force that withing plotting commands
tnr='Times New Roman'
params ={'mathtext.default':'regular'}
plt.rcParams.update(params)

#Importing Taustar data:
ObsID= sys.argv[1]
data = np.genfromtxt(ObsID+'_info.txt',skip_header=1)
wl = data[0:len(data),0]
data_val = data[0:len(data),4]
min_error = data[0:len(data),5]
max_error= data[0:len(data),6]
error = np.array([min_error, max_error])

#Defining constants

h = 4.1357E-18 #Plank's constant in KeV s
c = 2.998E8    #Speed of light in m/s
vinf = 2250E3 #in m/s
Rstar = 18.9*6.9599E8#in m
Msun= 1.98847E30 #in kg
#Defining function to compute wavelength in Angstrom
def wavelength(Energy):
    return (h*c*10**10)/Energy


#Importing Energy and Kappa values

contents = np.genfromtxt('kappaZ.txt')[3000:90000]
size = len(contents)
E = contents[0:size,0]
kappaZ = contents[0:size,1]


print(wavelength(E[0]))


#Calculating wavelength
wavelengths=[]
for i in range (len(E)):
    wavelengths.append(wavelength(E[i]))

f = interp1d(wavelengths, kappaZ)
k = f(wl)


#print(wavelengths[0])
Taustar =[]
steps = np.arange(1E-6, 4E-6,0.1E-6)
for i in range(len(k)):
    result=[]
    for j in steps:
        ts= (k[i]*j*0.1*Msun)/ (4*math.pi*Rstar*vinf*3.154E7)
        result.append(ts)
    Taustar.append(result)


#Making a model for chi squared
def model(data, model, max_error, min_error):
    result =0
    for i in range(len(model)):
        result += ((model[i]-data[i])/(min_error[i] if data[i]>model[i] else max_error[i] ))**2
    return result

#model(data_val,max_error,min_error)
#print(np.shape(Taustar))


#reduced_chis =[]
#vals =[]
chisquared =[]
models=[]
for j in range(len(Taustar[0])):
    mod=[]
    for i in range(len(Taustar)):
        mod.append(Taustar[i][j])
    models.append(mod)
    chisquared.append(model(data_val, mod, max_error,min_error))
reduced_chisquared =np.min(chisquared)/(len(data_val)-1)
vals = models[chisquared.index(np.min(chisquared))]




#R_delta_chi_square_1 = a[(np.abs((R_reduced_chi_square+1)*(len(R_o)-1)-chi_square)).argmin()]
#R_delta_chi_square_2 = a[(np.abs((R_reduced_chi_square+1)*(len(R_o)-1)-np.where(chi_square == chi_square[(np.abs((R_reduced_chi_square+1)*(len(R_o)-1)-chi_square)).argmin()], -1., chi_square))).argmin()]


mass_loss =[]

for i in range(len(k)):
    mass_loss.append(((vals[i]*4*math.pi*Rstar*vinf*3.154E7)/(k[i]*0.1))/Msun)
print(mass_loss)


#Plotting wavelength vs kappaZ
plt.figure(figsize = (10, 8))
plt.plot(wl, vals, 'k-')
plt.plot(wl, data_val, 'ro')
plt.errorbar(wl,data_val, error, ls='none',color='lightgrey',linewidth=0.5,capsize=1.5,capthick=1)

plt.xlabel('Wavelength($\AA$)', fontname=tnr, fontsize=23)
plt.ylabel('Taustar', fontname=tnr, fontsize=23)
plt.show()
