import math
import numpy as np
import plotly.plotly as py
import plotly
import plotly.graph_objs as go



#21661
Mdot_1 = 3.30E-06
min_error_1 = 1.06E-06
max_error_1 = 1.06E-06
error_average_1 = (min_error_1+max_error_1)/2

#20157
Mdot_2 = 2.77E-06
min_error_2 = 1.08E-06
max_error_2 =1.10E-06
error_average_2 = (min_error_2+max_error_2)/2

#21659
Mdot_3 = 2.53E-06
min_error_3 = 0.90E-06
max_error_3 = 0.97E-06
error_average_3 = (min_error_3+max_error_3)/2

#coefficents



def average(a):
    return (a[0]+a[1]+a[2])/3

def error_average(a):
    return math.sqrt((a[0])**2 + (a[1])**2 + (a[2])**2 )/3




print('Mass Loss using Windtab')
ml_tstar = []
ml_tstar.append(Mdot_1)
ml_tstar.append(Mdot_2)
ml_tstar.append(Mdot_3)

ml_tstar_min = []
ml_tstar_min.append(min_error_1)
ml_tstar_min.append(min_error_2)
ml_tstar_min.append(min_error_3)

ml_tstar_max = []
ml_tstar_max.append(max_error_1)
ml_tstar_max.append(max_error_2)
ml_tstar_max.append(max_error_3)


vinf = 2250E3*3.154E7 #in m/yr
Rstar = 18.9*6.9599E8#in m
Msun= 1.98847E30 #in kg

def m_loss(sigma_star):
    return (10*sigma_star*4*math.pi*Rstar*vinf)/Msun

def error(sstar_error):
    return (10*sstar_error*4*math.pi*Rstar*vinf)/Msun


contents = np.genfromtxt('sigma_star.txt', skip_header=1)
size = len(contents)
ObsIDs= contents[0:size,0]
sigma_star_all = contents[0:size,1]
min_error_all = contents[0:size,2]
sigma_star_all = contents[0:size,3]
ml_all =[]
ml_417 =[]
ml_415 =[]
ml_all_min =[]
ml_417_min =[]
ml_415_min =[]
ml_all_max =[]
ml_417_max =[]
ml_415_max =[]

for i in range (size):
        #print('ObsID'+ str(contents[i,0]))
        #print('From 0 to **')
        ml_all.append(m_loss(contents[i,1]))
        ml_all_min.append(error(contents[i,2]))
        ml_all_max.append(error(contents[i,3]))

        #print('From 4 to 17')
        ml_417.append(m_loss(contents[i,4]))

        ml_417_min.append(error(contents[i,5]))
        ml_417_max.append(error(contents[i,6]))

        #print('From 4 to 15')
        ml_415.append(m_loss(contents[i,7]))

        ml_415_min.append(error(contents[i,8]))
        ml_415_max.append(error(contents[i,9]))


print('MASS LOSS AVERAGE')
print('Using Taustar')
print(ml_tstar)
print(average(ml_tstar))
print(error_average(ml_tstar_min))
print(error_average(ml_tstar_max))

print('Using sigma star')
print('0-**')
print(ml_all)
print(average(ml_all))
print(error_average(ml_all_min))
print(error_average(ml_all_max))

print('4-17')
print(ml_417)
print(average(ml_417))
print(error_average(ml_417_min))
print(error_average(ml_417_max))


print('4-15')
print(ml_415)
print(average(ml_415))
print(error_average(ml_415_min))
print(error_average(ml_415_max))



print('Ro average')
print(average([1.57,1.51,1.66]))
print(error_average([0.20,0.19,0.16]))
print(error_average([0.22,0.20,0.17]))

averages=[]
averages.append(average(ml_tstar))
averages.append(average(ml_all))
averages.append(average(ml_417))
averages.append(average(ml_415))

er_averages_min=[]
er_averages_min.append(-1.5-error_average(ml_tstar_min)+average(ml_tstar))
er_averages_min.append(-0.9-error_average(ml_all_min)+average(ml_all))
er_averages_min.append(-1.1-error_average(ml_417_min)+average(ml_417))
er_averages_min.append(-1.2-error_average(ml_415_min)+average(ml_415))

er_averages=[]
er_averages.append(-1.8+error_average(ml_tstar_max)+average(ml_tstar))
er_averages.append(-1.8+error_average(ml_all_max)+average(ml_all))
er_averages.append(-1.8+error_average(ml_417_max)+average(ml_417))
er_averages.append(-1.8+error_average(ml_415_max)+average(ml_415))
y=list(range(0, 100, 10))


#Still not complete !
layout = go.Layout(yaxis=go.layout.YAxis(title='Type'),
                   xaxis=go.layout.XAxis(
                       range=[-4, 4],
                       tickvals=np.linspace(-3.8,3.8,58),
                       title='Mass Loss'),
                   barmode='overlay',
                   bargap=0.1)

data = [go.Bar(y=y,
               x=er_averages_min,
               orientation='h',
               showlegend=False,
               opacity=0.5,
               marker=dict(color='teal')
               ),
        go.Bar(y=y,
               x=er_averages,
               orientation='h',
               showlegend=False,
               opacity=0.5,
               marker=dict(color='teal')
               )]

#plotly.offline.plot(dict(data=data, layout=layout), filename='ml_pyramid')
