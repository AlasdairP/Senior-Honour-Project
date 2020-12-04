"""
This script plots the CO, O3, Temperature and Latitude against time
for all CARIBIC "package 2" flights 
"""

import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import scipy.signal

def main():
    
    path = "C:/Users/alasd/OneDrive - University of Edinburgh/SHP/data/IAGOS-CARIBIC-FULL"
    data_files = os.listdir(path)

    for i, file in enumerate(data_files):
        
        with open(os.path.join(path,file)) as current_file:
            
            all_lines = current_file.readlines()
            departure = all_lines[60]
            depart_time = all_lines[62]
            arrival = all_lines[63]   
        
        with open(os.path.join(path,file)) as current_file:    

            df = pd.read_csv(current_file, sep = " ", header=74)

        if "CO_PC1" in df.columns:
            continue
                
        xvariable = "UTC_time"
        yvariable = "CO_PC2"
        yvariable2 = "air_stag_temp_AC"
        yvariable3 = "O3_PC2"
        yvariable4 = "lat"
    
        df = df[df[xvariable] > -9999]
        df = df[df[yvariable] > -9999]
        df = df[df[yvariable3] > -9999]  
        df = df[df[yvariable4] > -9999]  
        
        if df.size < 10:
            continue    
                
        window_size = 9  
        
        df[yvariable] = scipy.signal.savgol_filter(df[yvariable], window_size, 2)
        df[yvariable2] = scipy.signal.savgol_filter(df[yvariable2], window_size, 2)    
        df[yvariable3] = scipy.signal.savgol_filter(df[yvariable3], window_size, 2)
        df.drop(df.head(200).index, inplace=True)
        df.drop(df.tail(300).index, inplace=True)    
        """
        df[yvariable]  = (df[yvariable] - df[yvariable].mean())/df[yvariable].mean()
        df[yvariable2]  = (df[yvariable2] - df[yvariable2].mean())/df[yvariable2].mean()
        df[yvariable3]  = (df[yvariable3] - df[yvariable3].mean())/df[yvariable3].mean()
        """    
        fig, ax1 = plt.subplots()
        ax1.set_xlabel("Time (seconds since start of day)" + "\n" + 
            departure  + arrival + depart_time)
        ax1.set_ylabel("CO, O3 (molar fraction, ppb), Stagnation Temp (K)")
            
        ax1.plot(df[xvariable], df[yvariable], 'bo', markersize=2, label="CO")
        ax1.plot(df[xvariable], df[yvariable2], 'ro', markersize=2, label="T")
        ax1.plot(df[xvariable], df[yvariable3], 'go', markersize=2, label="O3")
        ax1.legend()
        
        ax2 = ax1.twinx()
        
        ax2.plot(df[xvariable], df[yvariable4], 'yo', markersize=2, label="Lat")
        ax2.set_ylabel("Latitude (degrees)")
        ax2.legend()
        
        plt.title("CO, O3, temperature and latitude time series, CARIBIC")
        fig.tight_layout()
        plt.show()
        
main()

