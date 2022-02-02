# -*- coding: utf-8 -*-
r"""
Elation Sports Technologies LLC
1 Feb 2022

DIY EMT Conduit Telescoping Pole
Photoresistor Extension Sensing Calibration Script

"""

import matplotlib.pyplot as plt
import numpy as np
import time,csv
import matplotlib.cm as cm

plt.close('all')

currTimeString = time.strftime('%d%b%Y_%I%M%p')

#Replace this string with the local address where your data is saved.
data_path = r'C:\Users\(local_username)\Desktop'
folder_path = data_path

plot_alpha = 0.4

data_file_name = r'Photoresistor Calibration Data.csv'
data_file_path = data_path + '\\' + data_file_name

start_row = 1
raw_data = []

with open(data_file_path, 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for row in spamreader:
        raw_data.append(row)

raw_data_2 = []
for i in range(start_row,len(raw_data)):
    row_curr = raw_data[i]
    temp_list = []
    for  j in range(0,5):    
        temp_list.append(float(row_curr[j]))
    
    raw_data_2.append(temp_list)

raw_data_2 = np.array(raw_data_2)

#Idenify the different sets of angle data
angles = np.unique(raw_data_2[:,2])
num_angles = len(angles)

#Idenify the different sets of length data
lengths = np.unique(raw_data_2[:,0])

#Plot the data
slopes_1_list = []
slopes_2_list = []

fig,ax = plt.subplots()
plt.grid(True,alpha=plot_alpha)
plt.xlabel('Reading')
plt.ylabel('Extension Length [inch]')
plt.title('Net LDR Readings w.r.t. Extension Length\nVarying Theta')
    
e_temp = raw_data_2[1:,0] #Extension length values
t_temp = raw_data_2[1:,2] #Theta values
s1_temp = raw_data_2[1:,3] #LDR #1 values
s2_temp = raw_data_2[1:,4] #LDR #2 values

#Force the linear fit to pass through zero
#https://stackoverflow.com/questions/46164012/how-to-use-numpy-polyfit-to-force-scatter-points-linear-fit-pass-through-zero
m1 = np.linalg.lstsq(e_temp.reshape(-1,1), s1_temp, rcond=None)[0][0]
m2 = np.linalg.lstsq(e_temp.reshape(-1,1), s2_temp, rcond=None)[0][0]

slopes_1_list.append(m1)
slopes_2_list.append(m2)

ext_data_fit = np.array([0,max(e_temp)])
LDR_data_fit_1 = ext_data_fit * m1
LDR_data_fit_2 = ext_data_fit * m2

plt.plot(s1_temp,e_temp,'-o',color='tab:blue',markersize=3,label='LDR #1 Data')
plt.plot(s2_temp,e_temp,'-o',color='tab:orange',markersize=3,label='LDR #2 Data')

#Plot the average of the LDR1 and LDR2 readings, and fit that to a
#linear function.
sensor_avgs = 0.5 * (s1_temp + s2_temp)
plt.plot(sensor_avgs,e_temp,'-o',color='tab:green',markersize=3,label='Average')

#Force the linear fit to pass through zero
#https://stackoverflow.com/questions/46164012/how-to-use-numpy-polyfit-to-force-scatter-points-linear-fit-pass-through-zero
avg_diff_slope = np.linalg.lstsq(e_temp.reshape(-1,1), sensor_avgs, rcond=None)[0][0]

#Also do the fit without imposing any pass-through-zero restriction
coeffs_1 = np.polyfit(s1_temp,e_temp,1)
coeffs_2 = np.polyfit(s2_temp,e_temp,1)
coeffs_3 = np.polyfit(sensor_avgs,e_temp,1)

x_many = np.linspace(sensor_avgs[0],sensor_avgs[-1],100)
y_many = coeffs_3[0] * x_many + coeffs_3[1]

plt.plot(x_many,y_many,'--',color='tab:green',markersize=3,label='Linear Fit')

plt.legend()
plt.savefig(folder_path + '\\' + 'LDR_Readings_wrt_Extension' + '.png', dpi=200)

print()
print('Linear fit coefficients:')
print('Slope: ' + str(coeffs_3[0]))
print('Y-Int: ' + str(coeffs_3[1]))

#Write the calibration data to a CSV file.
with open(folder_path + '\\' + 'Calibration Fit Parameters' + '.csv', 'w', newline='') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=',')
    spamwriter.writerow(['Slope'] + [coeffs_3[0]])
    spamwriter.writerow(['Y_Int'] + [coeffs_3[1]])






