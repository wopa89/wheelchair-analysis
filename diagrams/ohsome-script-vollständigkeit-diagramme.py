from ohsome import OhsomeClient
from datetime import datetime
from functools import reduce
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import sys

def diagram(typ):
    # stations
    csv_path_ka  = "csv/karlsruhe-%s.csv" % (typ)
    csv_path_md  = "csv/magdeburg-%s.csv" % (typ)
    
    fig = plt.figure(tight_layout=True, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
    
    df_stations_ka = pd.read_csv(csv_path_ka)
    df_stations_md = pd.read_csv(csv_path_md)
    x1 = df_stations_ka.time
    y1 = df_stations_ka.value
    x2 = df_stations_md.time
    y2 = df_stations_md.value
    
    ax = plt.gca()
    line1, = ax.plot(x1, y1, '-', color='blue', label='Karlsruhe')
    line2, = ax.plot(x2, y2, '-', color='red', label='Magdeburg')
    ax.legend(handles=[line1,line2])
    ax.set_ylim(0, 105)
    ax.set_ylabel('Objektvollständigkeit in %', fontsize=14)
    ax.set_xlabel('Zeit in Monaten', labelpad=10, fontsize=14)
    ax.set_xticks(x1[::6])
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.set_xticks(x1[::12])
    fig.align_labels()
    
    csv_path_out = "diagramme/%s.png" % (typ)
    fig.savefig(csv_path_out, dpi=fig.dpi)
    
    # wheelchair
    csv_path_ka  = "csv/karlsruhe-%s-tags.csv" % (typ)
    csv_path_md  = "csv/magdeburg-%s-tags.csv" % (typ)
    
    fig = plt.figure(tight_layout=True, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
    
    df_wheelchair_ka = pd.read_csv(csv_path_ka)
    df_wheelchair_md = pd.read_csv(csv_path_md)
    x1 = df_wheelchair_ka.time
    y1 = df_wheelchair_ka.value
    x2 = df_wheelchair_md.time
    y2 = df_wheelchair_md.value
    
    ax = plt.gca()
    line1, = ax.plot(x1, y1, '-', color='blue', label='Karlsruhe')
    line2, = ax.plot(x2, y2, '-', color='red', label='Magdeburg')
    ax.legend(handles=[line1,line2])
    ax.set_ylim(0, 105)
    ax.set_ylabel('Attributvollständigkeit in %', fontsize=14)
    ax.set_xlabel('Zeit in Monaten', labelpad=10, fontsize=14)
    ax.set_xticks(x1[::6])
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.set_xticks(x1[::12])
    fig.align_labels()
    
    csv_path_out = "diagramme/%s-tags.png" % (typ)
    fig.savefig(csv_path_out, dpi=fig.dpi)
    
if __name__ == "__main__":
    diagram("stop_position")
    diagram("platform")