# -*- coding: utf-8 -*-
"""
Created on Tue Nov  2 14:35:08 2021

@author: rcboot
"""
import scipy as s
from scipy import optimize as opp
import numpy as np
import pandas as pd
import cv2
import argparse as ar1
import pandas as pd
import math as m
from pathlib import Path
import os

# Open the file with the binary images and define height of the images
path = Path(__file__) / 'This is where you write your path name to indicate where the time series images are stored'
os.chdir(str(path))
tasp = cv2.imread("ImageExample.jpg", cv2.IMREAD_UNCHANGED)
image_height = tasp.shape[0] #this is where the script defines the heght of the images

#Define middle of each aspiration channel

middle_y = [102,318,551,791,1038,1280,1524,1764] #Values for the x-coordinates of the middles of the 8 aspiration channels are filled in here

 
#Naming funtion to call all the images

def Naming(base_name, sv, fv, digits):

    full_name = []
    zero = str(0)
    total_zero = ""
    for i in range(sv, fv+1):
        if (i<10):
            add_zeros = digits-1
            for j in range(add_zeros):
                total_zero = total_zero + zero
        if (i>= 10 and i<100):
            add_zeros = digits-2
            for j in range(add_zeros):
                total_zero = total_zero + zero
        if (i>= 100 and i<1000):
            add_zeros = digits-3
            for j in range(add_zeros):
                total_zero = total_zero + zero
        if (i>= 1000 and i<10000):
            add_zeros = digits-4
            for j in range(add_zeros):
                total_zero = total_zero + zero
        full_name.append(base_name+total_zero+str(i)+".jpg")
        total_zero = ""
    return full_name

basename = "Binary" #depends on how the user named the images 
digits = 4
start_value = 0
end_value = 60
name_array = Naming(basename, start_value, end_value, digits)

#Function to measure aspiration in single image

def Aspiration(filename, channel_length):
    image = cv2.imread(filename)
    extension = []
    for i in range(len(middle_y)):
        for j in range(channel_length):
            data1, data2, data3 = image[j,middle_y[i]]
            
            if(data1<=10):
                extension.append(channel_length - j)
                break
            if j == channel_length-1:
                extension.append(None)
    return extension

#Funtion to measure aspiration in time series

def Displacement(namearray, channel_length):
    
    creep_serie1 = []
    creep_serie2 = []
    creep_serie3 = []
    creep_serie4 = []
    creep_serie5 = []
    creep_serie6 = []
    creep_serie7 = []
    creep_serie8 = []
    frame_index = []
    
    for i in range(0,len(namearray)):
        data = Aspiration(namearray[i], channel_length)
        creep_serie1.append(data[0])
        creep_serie2.append(data[1])
        creep_serie3.append(data[2])
        creep_serie4.append(data[3])
        creep_serie5.append(data[4])
        creep_serie6.append(data[5])
        creep_serie7.append(data[6])
        creep_serie8.append(data[7])
        frame_index.append(i)
        
    return creep_serie1, creep_serie2, creep_serie3, creep_serie4, creep_serie5, creep_serie6,creep_serie7,creep_serie8, frame_index

#Collect data

Database = pd.DataFrame()
time_steps = 4.61 # second per frame, depends on camera
channel_length = image_height #pixels
distance_to_pixel_ratio = 1.3 # microns per pixel, depends on used objective
creep_data = Displacement(name_array, channel_length)

Database["Serial number"] = creep_data[8] #frame_index
Database["Time Step (secs)"] = Database["Serial number"]*time_steps
Database["Creep1 (pixels)"] = creep_data[0] 
Database["Creep1 ($\mu$m)"] = Database["Creep1 (pixels)"]*distance_to_pixel_ratio
Database["Creep2 (pixels)"] = creep_data[1] 
Database["Creep2 ($\mu$m)"] = Database["Creep2 (pixels)"]*distance_to_pixel_ratio
Database["Creep3 (pixels)"] = creep_data[2] 
Database["Creep3 ($\mu$m)"] = Database["Creep3 (pixels)"]*distance_to_pixel_ratio
Database["Creep4 (pixels)"] = creep_data[3] 
Database["Creep4 ($\mu$m)"] = Database["Creep4 (pixels)"]*distance_to_pixel_ratio
Database["Creep5 (pixels)"] = creep_data[4] 
Database["Creep5 ($\mu$m)"] = Database["Creep5 (pixels)"]*distance_to_pixel_ratio
Database["Creep6 (pixels)"] = creep_data[5] 
Database["Creep6 ($\mu$m)"] = Database["Creep6 (pixels)"]*distance_to_pixel_ratio
Database["Creep7 (pixels)"] = creep_data[6] 
Database["Creep7 ($\mu$m)"] = Database["Creep7 (pixels)"]*distance_to_pixel_ratio
Database["Creep8 (pixels)"] = creep_data[7] 
Database["Creep8 ($\mu$m)"] = Database["Creep8 (pixels)"]*distance_to_pixel_ratio

#Export data to excel file

file_name = 'CreepDataAllChannels.xlsx'
Database.to_excel(file_name)
