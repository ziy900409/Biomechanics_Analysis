"""
Created on Sun Apr 24 12:53:32 2022
Batch process all files under a specific folder
It can be used to different type of file, please change line 23, 30 as needed
@author: Hsin Yang, 20220424
"""
import os
# using a recursive loop to traverse each folder
# and find the file extension has .csv
def Read_File(x, y, subfolder='None'):
    '''
    This function will return file path
    
    Parameters
    ----------
    x : str
        file path
    y : str
        file type
        example: ".csv"
    subfolder : boolean
    
    Returns
    -------
    csv_file_list : list
    '''
    
    # if subfolder = True, the function will run with subfolder
    folder_path = x
    data_type = y
    csv_file_list = []
    
    if subfolder:
        file_list_1 = []
        for dirPath, dirNames, fileNames in os.walk(x):
            # file_list = os.walk(folder_name)
            file_list_1.append(dirPath)
        # need to change here [1:]
        for ii in file_list_1[1:]:
            file_list = os.listdir(ii)
            for iii in file_list:
                if os.path.splitext(iii)[1] == data_type:
                    file_list_name = ii + '\\' + iii
                    csv_file_list.append(file_list_name)
    else:
        folder_list = os.listdir(x)                
        for i in folder_list:
            if os.path.splitext(i)[1] == data_type:
                file_list_name = folder_path + "\\" + i
                csv_file_list.append(file_list_name)                
        
    return csv_file_list
