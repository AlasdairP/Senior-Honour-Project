"""
This script identifies tropopause crossings,
and then plots the height of each tropopause crossing against its latitude,
which theoretically produces a plot of the variation of tropopause height with latitude. 

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
        
          
        if "CO_PC2" in df.columns:

            df = df[df["CO_PC2"] > -9999]
            df = df[df["O3_PC2"] > -9999]
            
            df.drop(df.head(300).index, inplace=True)
            df.drop(df.tail(400).index, inplace=True) 
        
            df_list.append(df)
        
        if df.size < 10:
            continue  
        
    dff = pd.concat(df_list[i] for i in range(len(df_list))) 

    window_size = 9 
        
    dff["O3_PC2"] = scipy.signal.savgol_filter(dff["O3_PC2"], window_size, 2)
    dff["CO_PC2"] = scipy.signal.savgol_filter(dff["CO_PC2"], window_size, 2)
     
    ratio2 = dff["O3_PC2"]/dff["CO_PC2"]
    
    # Define tropospheric ratio threshold level
    
    df2 = pd.concat([ratio2, dff["lat"], dff[altitude]], axis=1)
    ratio_list = df2[0].values.tolist()
    lat_list = df2["lat"].values.tolist()
    alt_list = df2[altitude].values.tolist()
    
    # Find tropopause crossings
    
    crossing_latitudes = []
    crossing_altitudes = []
    
    trop_threshold = 0.8
    interval=10
    diff_threshold = 1.0
    bins=100
        
    big_difference_list = []
    difference_list = []
    
    for i, ratio in enumerate(ratio_list):
        
        if i < (len(ratio_list) - interval):

            if ratio < trop_threshold:
                
                if ratio_list[i+interval] > trop_threshold:
                
                    difference1 = abs(ratio_list[i+interval] - ratio_list[i])
                    difference_list.append(difference1)
                
                    if difference1 > diff_threshold:
                    
                        big_difference_list.append(difference1)
                    
                        crossing_latitudes.append(lat_list[int(i+(interval/2))])
                        crossing_altitudes.append(alt_list[int(i+(interval/2))])
                        
                elif ratio_list[i-interval] > trop_threshold:
                    
                    difference2 = abs(ratio_list[i-interval] - ratio_list[i])
                    difference_list.append(difference2)
                
                    if difference2 > diff_threshold:
                    
                        big_difference_list.append(difference2)
                    
                        crossing_latitudes.append(lat_list[int(i-(interval/2))])
                        crossing_altitudes.append(alt_list[int(i-(interval/2))])
    
    pyplot.hist(difference_list, bins, color='orange')
    pyplot.plot([diff_threshold,diff_threshold],[0,1000], 
        color = 'blue', linewidth=1, linestyle='dashed')
    pyplot.title("Histogram of the " + str(interval*10) + "s interval differences")
    pyplot.xlabel("Difference (absolute value)")
    pyplot.ylabel("Counts (log)")
    pyplot.yscale("log")
    pyplot.text(10,1000, "Difference threshold: " + str(diff_threshold))
    pyplot.show()
    
    #pyplot.hist(crossing_latitudes, bins, color='orange')
    pyplot.plot(crossing_latitudes, crossing_altitudes, 'bo', markersize=3)
    pyplot.title("Altitude against latitude for tropopause crossings")
    pyplot.xlabel("Latitude")
    pyplot.ylabel("Altitude")
    pyplot.ylim([7500, 13500])
    pyplot.xlim([-60, 90])
    pyplot.text(-20, 8000, "Tropopause threshold: " + str(trop_threshold) + "\n" + 
        "Interval: " + str(interval*10) + "s" + "\n" + 
        "Difference threshold: " + str(diff_threshold))
    pyplot.show()
        
main()

