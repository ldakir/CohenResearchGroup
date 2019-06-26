#Short script to calculate the limits on Ro

import sys

Uo= float(sys.argv[1])
lower = float(sys.argv[2])
upper = float(sys.argv[3])

Ro = 1/Uo
min = 1/(Uo+upper)-1/Uo
max = 1/(Uo+lower)-1/Uo

print('%.2f' %Ro +'('+'%.2f' %min +' +'+'%.2f' %max+')')
