"""
Plots fourier transforms for all CARIBIC flights.

"""

import itertools
import matplotlib.pyplot as pyplot
import os
import pandas as pd
import scipy
import scipy.signal
import numpy as np
import scipy.fftpack
from statistics import mean

def main():
    
    path = "C:/Users/alasd/OneDrive - University of Edinburgh/SHP/data/IAGOS-CARIBIC-FULL"
    data_files = os.listdir(path)
    
    df_list = []

    for file in data_files:
        
        with open(os.path.join(path,file)) as current_file:    
            
            df = pd.read_csv(current_file, sep = " ", header=74)
                 
        # Define  variables of interest
        xvariable = "UTC_time"
        yvariable = "CO_PC2"
        yvariable2 = "air_stag_temp_AC"
        yvariable3 = "O3_PC2"
        
        # Remove the "Package 1" flights as they have no O3/CO data
        if "CO_PC1" in df.columns:
            continue
    
        # Remove missing values. This leaves blank gaps in time.
        df = df[df[xvariable] > -9999]
        df = df[df[yvariable] > -9999]
        df = df[df[yvariable3] > -9999]   
        
        if df.size > 10000:    
            df_list.append(df)
                
    window_size = 9
    
    fftCO_list = []
    fftTemp_list = []
    fftO3_list = []
    
    for df in df_list:

        # Savistky-Golay filters
        df[yvariable] = scipy.signal.savgol_filter(df[yvariable], window_size, 2)
        df[yvariable2] = scipy.signal.savgol_filter(df[yvariable2], window_size, 2)    
        df[yvariable3] = scipy.signal.savgol_filter(df[yvariable3], window_size, 2)
        
        # Remove takeoff/landings
        df.drop(df.head(200).index, inplace=True)
        df.drop(df.tail(300).index, inplace=True)    

        # Subtract means, to get oscillations about 0.
        df[yvariable]  = df[yvariable] - df[yvariable].mean()
        df[yvariable2]  = df[yvariable2] - df[yvariable2].mean()
        df[yvariable3]  = df[yvariable3] - df[yvariable3].mean()
    
        # Compute (real) fast fourier transforms and append to lists.
        fftCO_list.append(np.fft.rfft(df[yvariable], n=100000))
        fftTemp_list.append(np.fft.rfft(df[yvariable2], n=100000))
        fftO3_list.append(np.fft.rfft(df[yvariable3], n=100000))
    
    fftCO_listplot = []
    
    n = len(df_list)
    
    for i in range(n-1):
    
        fftCO_listplot.append(np.fft.rfft(df_list[i][yvariable], n=100000))

          
    fftCO_avg = np.mean(fftCO_list, axis=0)
    fftTemp_avg = np.mean(fftTemp_list, axis=0)    
    fftO3_avg = np.mean(fftO3_list, axis=0)

    timestep = 10
    freq = np.fft.rfftfreq(100000, d=timestep)
    
    #pyplot.plot(freq, abs(fftTemp_avg), 'ro', markersize=2)
    #pyplot.plot(freq, abs(fftO3_avg), 'go', markersize=2) 
    
    for i in range(n-1):
        pyplot.plot(freq, abs(fftCO_listplot[i]), markersize=2)
       
    pyplot.title("Fourier transforms of CO time series, all CARIBIC flights")
    pyplot.ylabel("Amplitude (molar fraction, ppb)")
    pyplot.xlabel("Frequency [Hz] (log)")
    pyplot.xscale("log")
    pyplot.show()
    
    pyplot.plot(freq, abs(fftCO_avg), 'bo', markersize=2)
    pyplot.title("Average of all Fourier transforms of CO time series")
    pyplot.ylabel("Amplitude (molar fraction, ppb)")
    pyplot.xlabel("Frequency [Hz] (log)")
    pyplot.xscale("log")    
    pyplot.show()
    
main()
