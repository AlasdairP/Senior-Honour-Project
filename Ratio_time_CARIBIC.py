"""
This script plots the O3/CO ratio against time,
flight by flight, for all CARIBIC flights.

"""

import itertools
import matplotlib.pyplot as pyplot
import os
import pandas as pd
import numpy as np
import scipy.signal
from matplotlib_scalebar.scalebar import ScaleBar


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
        yvariable2 = "O3_PC2"
        yvariable3 = "baro_alt_AC"
        yvariable4 = "air_stag_temp_AC"
    
        df = df[df[xvariable] > -9999]
        df = df[df[yvariable] > -9999]
        df = df[df[yvariable2] > -9999]
        df = df[df[yvariable3] > -9999]
        df = df[df[yvariable4] > -9999]
        
        df.drop(df.head(200).index, inplace=True)
        df.drop(df.tail(300).index, inplace=True)
            
        ratio = df["O3_PC2"]/df["CO_PC2"]
            
        if df.size < 10:
            continue     
        
        window_size = 9 
        
        df[yvariable] = scipy.signal.savgol_filter(df[yvariable], window_size, 2)
        df[yvariable2] = scipy.signal.savgol_filter(df[yvariable2], window_size, 2)    
        df[yvariable3] = scipy.signal.savgol_filter(df[yvariable3], window_size, 2)
        
        fig, ax1 = pyplot.subplots()
        
        ax1.set_xlabel("Time (seconds since start of day)" + "\n" + 
                        departure  + arrival + depart_time)
        ax1.set_ylabel("O3/CO ratio")
        
        ax1.plot(df[xvariable], ratio, 'bo', markersize=2, label="ratio")
        
        #ax2 = ax1.twinx()
        #ax2.set_ylabel("Latitude (degrees), Altitude (km)")
        
        #ax2.plot(df[xvariable], df[yvariable3]/1000, 'ro', markersize=2, label="altitude")
        #ax2.plot(df[xvariable], df["lat"], 'yo', markersize=2, label="latitude")                
        pyplot.title("O3/CO ratio against time")

        scalebar = ScaleBar(240, location='center left')
        fig.gca().add_artist(scalebar)
        
        fig.legend(loc='upper right')
        fig.tight_layout()
        pyplot.show()
        
main()

