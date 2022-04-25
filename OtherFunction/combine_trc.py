# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 15:24:41 2022

It just a little test that try to combine two .trc file

@author: Hsin Yang
"""
import os
import numpy as np
import pandas as pd
from pandas import DataFrame

# setting data folder
path = r'D:\NTSU\TenLab\ComputerMouse\data'
path = path +'\\'
file_list = os.listdir(path)
Mouse_1_list = []
mouse_list = []

# to find each file have specific name
for i in file_list:
    if os.path.splitext(i)[1] == ".trc":
        if i.find('Mouse 3') != -1:
            Mouse_1_list.append(i)
        elif i.find('mouse') != -1:
            mouse_list.append(i)

# to seperate trial name and name of marker set 
Mouse_1_list_split = []
for i in Mouse_1_list:
    Mouse_1_list_split.append(i.split('-'))
mouse_list_split =[]
for i in mouse_list:
    mouse_list_split.append(i.split('-'))

# combine two data set
for i in range(np.shape(Mouse_1_list_split)[0]):
    for ii in range(np.shape(mouse_list_split)[0]):
        if Mouse_1_list_split[i][0] == mouse_list_split[ii][0]:
            print(Mouse_1_list_split[i])
            print(mouse_list_split[ii])
            print(i)
            # create data path
            FourMarkerSet_data_path = path + '-'.join(Mouse_1_list_split[i])
            mouse_data_path = path + '-'.join(mouse_list_split[ii])
            # read .trc data set
            FourMarkerSet_data = pd.read_csv(FourMarkerSet_data_path, sep = '	', skiprows=3)
            mouse_data = pd.read_csv(mouse_data_path, sep = '	', skiprows=3)
            # delect last columns from Mouse data
            mouse_data = mouse_data.drop(mouse_data.columns[-1], axis=1)
            # combine two data set
            combine_data = pd.concat([mouse_data, FourMarkerSet_data.iloc[:, 2:13]]
                                     , axis=1, ignore_index=True)
            # combine two columns name
            columns_name = mouse_data.columns.append(FourMarkerSet_data.columns[2:13])
            # add columns name to dataframe
            combine_data.columns = columns_name
            # writing data to excel
            file_name = path + Mouse_1_list_split[i][0] + '_combine.xlsx'
            DataFrame(combine_data).to_excel(file_name, sheet_name='Sheet1', index=False, header=True)
