# -*- coding: utf-8 -*-
r"""
Elation Sports Technologies LLC
1 Feb 2022

Telescoping Couplings - Sensing Pole Project
Photoresistor Method Demo Data Processing

"""

import csv,time
import matplotlib.pyplot as plt
import serial, io, datetime
from serial import Serial
import numpy as np
from matplotlib import animation
import matplotlib.cm as cm

def is_integer(n):
    try:
        float(n)
    except ValueError:
        return False
    else:
        return float(n).is_integer()

plot_alpha = 0.25

animation_folder = r'C:\Users\(local_username)\Desktop'

#Read in the calibration data
calib_folder = r'C:\Users\(local_username)\Desktop'
calib_file = calib_folder + '\\' + 'Calibration Fit Parameters.csv'
calib_data = []
calib_dict = {}
with open(calib_file) as csvfile:
        reader = csv.reader(csvfile,delimiter=',')
        for row in reader:
            calib_data.append(row)

for i in range(0,len(calib_data)):
    if calib_data[i][0] == 'Slope':
        calib_dict['A'] = float(calib_data[i][1])
    if calib_data[i][0] == 'Y_Int':
        calib_dict['B'] = float(calib_data[i][1])
            
#https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-numpy-scipy
#x is the data you want to take the rolling average for.
#w is the size of the window to take the average
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w

rolling_avg_window = 3
plot_individual_files_boolean = True

timestr = time.strftime("%d%b%Y_%H%M%p")
folder_path = r'C:\Users\(local_username)\Desktop'
file_type = '.csv'

file_names_to_process = []

#Pole extension
file_names_to_process.append('Log_19Dec2021_1444PM')

file_labels = []
output_suffix = 'parsed'
data_all = []

for k in range(0,len(file_names_to_process)):
    
    file_name_to_process = file_names_to_process[k]

    file_path_to_process = folder_path + '\\' + file_name_to_process + file_type
    file_path_output= folder_path + '\\' + file_name_to_process + '_' + output_suffix + file_type
    
    print('Reading data from file: ' + file_name_to_process + file_type)
    
    raw_data = []
    
    with open(file_path_to_process) as csvfile:
            reader = csv.reader(csvfile,delimiter=',')
            for row in reader:
                raw_data.append(row)
    
    raw_data_2 = []
    start_row_index = 30 #Can set to 0 to collect from the beginning of the data
    
    time_data = []
    data_stream_1 = []
    data_stream_2 = []
    
    for i in range(start_row_index, len(raw_data)):
        
        temp_list = raw_data[i][0].split(',')
        temp_list_2 = []
        
        time_data.append(float(temp_list[0]))
        
        data_stream_1.append(float(temp_list[1]))
        data_stream_2.append(float(temp_list[2]))
        
        temp_list_2.append(time_data[-1])
        temp_list_2.append(data_stream_1[-1])
        temp_list_2.append(data_stream_2[-1])
        
        raw_data_2.append(temp_list_2)
    
    raw_data_2 = np.array(raw_data_2)
    data_stream_1 = np.array(data_stream_1)
    data_stream_2 = np.array(data_stream_2)
    
    time_data = np.array(time_data)
    time_data = time_data - time_data[0]
    
    avg_data = 0.5 * (data_stream_1 + data_stream_2)
    
    fig,ax = plt.subplots()
    x_label_string = 'Time [sec]'
    y_label_string = 'Data'
    
    plt.grid(True,alpha=plot_alpha)
    plt.xlabel(x_label_string)
    plt.ylabel(y_label_string)
    
    plt.plot(time_data,data_stream_1,'-',color='tab:blue',label='Sensor 1')
    plt.plot(time_data,data_stream_2,'-',color='tab:orange',label='Sensor 2')
    plt.plot(time_data,avg_data,'--',color='tab:green',label='Average')
    
    plt.legend()
    
    plotTitle = file_name_to_process + file_type + '\n' + 'Raw Data'
    plt.title(plotTitle)
    
    plt.savefig(animation_folder + '\\' + file_name_to_process + '_RawData' + '.png', dpi=200)
    
    def calc_distance(A,B,s1,s2):
        avg_curr = (s1+s2) * 0.5
        dist_solved = A * avg_curr + B
        return dist_solved
    
    dist_list = []
    for i in range(0,len(avg_data)):
        dist_solved_curr = calc_distance(calib_dict['A'],calib_dict['B'],data_stream_1[i],data_stream_2[i])
        dist_list.append(dist_solved_curr)
        
    fig,ax = plt.subplots()
    x_label_string = 'Time [sec]'
    y_label_string = 'Extension [inch]'
    plt.grid(True,alpha=plot_alpha)
    plt.xlabel(x_label_string)
    plt.ylabel(y_label_string)
    
    plt.plot(time_data,dist_list,'-',color='tab:blue')
    
    plt.legend()
    
    plotTitle = file_name_to_process + file_type + '\n' + 'Extension Data'
    plt.title(plotTitle)
    
    plt.savefig(animation_folder + '\\' + file_name_to_process + '_ExtensionData' + '.png', dpi=200)
    
    animation_folder = r'C:\Users\(local_username)\Desktop'
    
    #Linear map function
    #https://stackoverflow.com/questions/1969240/mapping-a-range-of-values-to-another
    def linear_map(value, leftMin, leftMax, rightMin, rightMax):
        # Figure out how 'wide' each range is
        leftSpan = leftMax - leftMin
        rightSpan = rightMax - rightMin
    
        # Convert the left range into a 0-1 range (float)
        valueScaled = float(value - leftMin) / float(leftSpan)
    
        # Convert the 0-1 range into a value in the right range.
        return rightMin + (valueScaled * rightSpan)
    
    #Have the line change color as the extension distance changes.
    val_min = min(dist_list)
    val_max = max(dist_list)
    color_val_min = 0
    color_val_max = 1
    color_vals = []
    for i in range(0,len(dist_list)):
        val_curr = dist_list[i]
        color_vals.append(linear_map(val_curr,val_min,val_max,color_val_min,color_val_max))
    
    color_vals = np.array(color_vals)
    colors = cm.rainbow(color_vals)
    
    plt.show()
    def update3(i):
        bar_plot_object[0].set_height(dist_list[i])
        bar_plot_object[0].set_color(colors[i])
        time_string_curr = format(time_data[i], '.2f')
        ann2.set_text('t = ' + time_string_curr + ' sec')
        
        return bar_plot_object
    
    fig2,ax2 = plt.subplots()
    fig2.set_size_inches(1.75, 7)
    
    ax2.set_ylim(0,max(dist_list)+1)
    plt.xticks([], [])
    
    plt.title('Extension [inch]')
    
    ln2, = plt.plot([], [], 'b-', lw=3, markersize=3)
    pos = 0
    val = 0
    width = 0.3
    bar_plot_object = plt.bar(pos,val)
    ann2 = plt.annotate('test', xy=(-.3,2), color = 'k', bbox=dict(boxstyle="square", alpha=1, facecolor='w'))
    
    print()
    print('Creating animation in a Figure...')
    
    #Interval is the delay between frames in msec. It is an integer.
    ani = animation.FuncAnimation(fig2, update3, frames=len(dist_list), interval=1)
    
    print('Saving animation as a gif...')
    gif_fps = int(len(dist_list)/max(time_data))
    ani.save(animation_folder + '\\' + file_name_to_process + '_' + 'animation' + '.gif',writer='pillow',fps=gif_fps)
    print('Gif saved!')
    
    print()
    print('Saving MP4...')
    
    #You will need to download FFmpeg to get the animation script to work correctly.
    #It can be downloaded for free from its original website: https://www.ffmpeg.org/
    #Change the Windows address below to lead to the downloaded ffmpeg.exe file on your computer.
    plt.rcParams['animation.ffmpeg_path'] = r'C:\Users\(local_username)\Desktop\FFmpeg\bin\ffmpeg.exe'
    
    writervideo = animation.FFMpegWriter(fps=gif_fps) 
    ani.save(animation_folder + '\\' + file_name_to_process + '_' + 'animation' + '.mp4', writer=writervideo)
    print('MP4 saved!')
    

    
    
    