"""
This script uses Plotly and Dash to show a CO density map for a week of CORE flights.

"""

# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import itertools
import os

"""
This first function reads in the data and creates a single Pandas dataframe.
This contains the data from all the flights, joined top to tail.
"""

def makedataframe():
    
    path = "C:/users/alasd/OneDrive - University of Edinburgh/SHP/data/IAGOS-CORE_1week"
    data_files = os.listdir(path)
    
    df_list = []

    for file in data_files:
        
        with open(os.path.join(path,file)) as current_file:   
            
            df_list.append(pd.read_csv(current_file, sep = " ", header=70))
            
    df = pd.concat(df_list[i] for i in range(len(df_list)))
        
    return df

# Initialise the Dash app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

def main():

    df = makedataframe()
    
    # Plot the CO density map, onto a MapBox map.
    fig = px.density_mapbox(df, lat="lat", lon="lon", z="CO_P1", range_color=[80,180], radius=10, center=dict(lat=0, lon=0), zoom=1, title = "CO density heatmap", height=800, mapbox_style="stamen-terrain")
    
    # Layout and extras
    app.layout = html.Div(children=[
        html.H1(children='My SHP - IAGOS Data'),
    
        html.Div(children=''' This is my app for analysing IAGOS data!.'''),
    
        dcc.Graph(id='example-graph', figure=fig)])
        
main()

if __name__ == '__main__':
    app.run_server(debug=True)