# -*- coding: utf-8 -*-
"""
Created on Thu Jan 19 22:44:15 2023
error: ValueError: could not broadcast input array from shape (4132,12) into shape (4144,12)
bug 原因: header資訊與data資訊不重合的問題
@author: Hsin Yang. 2023.01.20
"""

def read_c3d(path):
    """
    Parameters
    ----------
    path : str
        kep in c3d data path.
    Returns
    -------
    motion_information : dict
        Contains: frame rate, first frame, last frame, size(number of infrared markers).
    motion_data : DataFrame
        data strcuture like .trc file.
    analog_information : dict
        Contains: frame rate, first frame, last frame, size(number of analog channel).
    FP_data : DataFrame
        data structure like .anc file.
    
    example:
        motion_information, motion_data, analog_information, FP_data = read_c3d(Your_Path)
    
    Author: Hsin Yang. 2023.01.20
    """
    # import library
    import ezc3d
    import numpy as np
    import pandas as pd    
    # 1. read c3d file
    c = ezc3d.c3d(path)
    # 數據的基本資訊，使用dict儲存
    # 1.1 information of motion data
    motion_information = c['header']['points']
    # 1.2 information of analog data
    analog_information = c['header']['analogs']
    # 2. convert c3d motion data to DataFrame format
    ## 2.1 create column's name of motion data
    motion_axis = ['x', 'y', 'z']
    motion_markers = []
    for marker_name in c['parameters']['POINT']['LABELS']['value']:
        for axis in motion_axis:
            name = marker_name + '_' + axis
            motion_markers.append(name)
    ## 2.2 create x, y, z matrix to store motion data
    # motion_data = pd.DataFrame(np.zeros([c['header']['points']['last_frame']+1, # last frame + 1
    #                                      len(c['parameters']['POINT']['LABELS']['value'])*3]), # marker * 3
    #                            columns=motion_markers) 
    motion_data = pd.DataFrame(np.zeros([np.shape(c['data']['points'])[-1], # last frame + 1
                                         len(c['parameters']['POINT']['LABELS']['value'])*3]), # marker * 3
                               columns=motion_markers) 
    ## 2.3 key in data into matrix
    for i in range(len(c['parameters']['POINT']['LABELS']['value'])):
        # print(1*i*3, 1*i*3+3)
        # transpose matrix to key in data
        motion_data.iloc[:, 1*i*3:1*i*3+3] = np.transpose(c['data']['points'][:3, i, :])
    ## 2.4 insert time frame
    ### 2.4.1 create time frame
    motion_time = np.linspace(
                                0, # start
                              ((c['header']['points']['last_frame'])/c['header']['points']['frame_rate']), # stop = last_frame/frame_rate
                              num = (np.shape(c['data']['points'])[-1]) # num = last_frame
                              )
    ### 2.4.2 insert time frame to motion data
    motion_data.insert(0, 'Frame', motion_time)
    # 3. convert c3d analog data to DataFrame format
    #    force plate data (FP = force plate)
    ## 3.1 create force plate channel name
    FP_channel = c['parameters']['ANALOG']['LABELS']['value']
    ## 3.2 create a matrix to store force plate data
    FP_data = pd.DataFrame(np.zeros([np.shape(c['data']['analogs'])[-1], # last frame + 1
                                         len(FP_channel)]), 
                               columns=FP_channel)
    FP_data.iloc[:, :] = np.transpose(c['data']['analogs'][0, :, :])
    ## 3.3 insert time frame
    ### 3.3.1 create time frame
    FP_time = np.linspace(
                                0, # start
                              ((c['header']['analogs']['last_frame'])/c['header']['analogs']['frame_rate']), # stop = last_frame/frame_rate
                              num = (np.shape(c['data']['analogs'])[-1]) # num = last_frame
                              )
    FP_data.insert(0, 'Frame', FP_time)
    # synchronize data (optional)
    return motion_information, motion_data, analog_information, FP_data

motion_information, motion_data, analog_information, FP_data = read_c3d(r'C:/Users/hsin.yh.yang/Downloads/D0005.c3d')