# -*- coding: utf-8 -*-
"""
Created on Wed Feb 23 12:51:32 2022

@author: Hsin Yang

This is using Delsys EMG sensor to be a template. If someone want to use it, you must modify the filter parameter that suit for you experiment.

This function will return two different smoothing data for user. 
One is calculate by Root Mean Square, another one is calculate by lowpass filter which means linear envelop analysis.
The user can choose which one is suitable for your experiment design.
"""
import pandas as pd
import numpy as np
from scipy import signal
from pandas import DataFrame

def EMG_processing(cvs_file_list):
    
    '''
    This function uses the Delsys data format as a template
    
    This function will calculate 
    1. Bandpass filter
    2. Rectify data
    3. Lowpass filter or Root mean square

    Parameters
    ----------
    cvs_file_list : str
        data path    

    Returns
    -------
    bandpass_filtered_data : ndarray
        The filtered data.
    rms_data : ndarray
        The smoothed data, smoothing method used Root mean square
    lowpass_filtered_data : ndarray
        Linear envelop analysis, smoothing method used lowpass filter

    '''
    
    data = pd.read_csv(cvs_file_list,encoding='UTF-8')
    # to define data time
    data_time = data.iloc[:,0]
    Fs = 1/(data_time[2]-data_time[1]) # sampling frequency
    data = pd.DataFrame(data)
    # --------need to change column name or using column number-------------
    # to choose the surface Electromyography chennel for analysis
    EMG_data = data.iloc[:, np.arange(1,112,8)]
    # bandpass filter use in signal
    bandpass_sos = signal.butter(2, [20, 450],  btype='bandpass', fs=Fs, output='sos')
    
    bandpass_filtered_data = np.zeros(np.shape(EMG_data))
    for i in range(np.shape(EMG_data)[1]):
        # print(i)
        # using dual filter to processing data to avoid time delay
        bandpass_filtered = signal.sosfiltfilt(bandpass_sos, EMG_data.iloc[:,i])
        bandpass_filtered_data[:, i] = bandpass_filtered 
        
    # -------Data smoothing. Compute RMS
    # The user should change window length and overlap length that suit for your experiment design
    # window width = window length(second)//time period(second)
    window_width = int(0.04265/(1/np.floor(Fs))) #width of the window for computing RMS
    # caculate absolute value
    bandpass_filtered_data = abs(bandpass_filtered_data)
    rms_data = np.zeros(np.shape(bandpass_filtered_data))
    for i in range(np.shape(rms_data)[1]):
        for ii in range(np.shape(rms_data)[0]-window_width):
            data_location = ii+(window_width/2)
            rms_data[int(data_location), i] = (np.sum(bandpass_filtered_data[ii:ii+window_width, i])
                               /window_width)
    # ------linear envelop analysis-----------                          
    # ------lowpass filter parameter that the user must modify for your experiment        
    lowpass_sos = signal.butter(2, 2.5, btype='low', fs=Fs, output='sos')        
    lowpass_filtered_data = np.zeros(np.shape(bandpass_filtered_data))
    for i in range(np.shape(rms_data)[1]):
        lowpass_filtered = signal.sosfiltfilt(lowpass_sos, bandpass_filtered_data[:,i])
        lowpass_filtered_data[:, i] = lowpass_filtered
    # add columns name to data frame
    rms_data = pd.DataFrame(rms_data, columns=EMG_data.columns)
    lowpass_filtered_data = pd.DataFrame(lowpass_filtered_data, columns=EMG_data.columns)
    # insert time data in the DataFrame
    lowpass_filtered_data.insert(0, 'time', data_time)
    rms_data.insert(0, 'time', data_time)    
    return bandpass_filtered_data, rms_data, lowpass_filtered_data
