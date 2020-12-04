"""
This script plots the O3/CO ration against latitude.
Uses all CARIBIC flights.

"""

import matplotlib.pyplot as pyplot
import os
import pandas as pd
import numpy as np
import scipy.signal

def main():
    
    path = "C:/Users/alasd/OneDrive - University of Edinburgh/SHP/data/IAGOS-CARIBIC-FULL"
    data_files = os.listdir(path)
    
    df_list = []

    for file in data_files:
        
        with open(os.path.join(path,file)) as current_file:    
            
            df = pd.read_csv(current_file, sep = " ", header=74)
                 
        time = "UTC_time"
        altitude = "baro_alt_AC"
        
        df = df[df[time] > -9999]
        df = df[df["lat"] > -9999]
        
        if "CO_PC1" in df.columns:
            continue
            
        if "CO_PC2" in df.columns:

            df = df[df["CO_PC2"] > -9999]
            df = df[df["O3_PC2"] > -9999]
            
            df.drop(df.head(200).index, inplace=True)
            df.drop(df.tail(300).index, inplace=True) 
        
            df_list.append(df)
        
        if df.size < 10:
            continue  
        
    dff = pd.concat(df_list[i] for i in range(len(df_list)))
    
    window_size = 9 
        
    dff["O3_PC2"] = scipy.signal.savgol_filter(dff["O3_PC2"], window_size, 2)
    dff["CO_PC2"] = scipy.signal.savgol_filter(dff["CO_PC2"], window_size, 2)    


    ratio = dff["O3_PC2"]/dff["CO_PC2"]

    pyplot.plot(dff["lat"], ratio, 'bo', markersize=0.1)
    pyplot.title("O3/CO ratio against latitude")
    pyplot.xlabel("Latitude")
    pyplot.ylabel("O3/CO ratio")
    pyplot.show()
        
main()
