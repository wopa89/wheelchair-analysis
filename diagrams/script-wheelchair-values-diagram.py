import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import os
import sys

def diagram(typ):
    csv_path_ka  = "csv/karlsruhe-%s-wheelchair-values.csv" % (typ)
    csv_path_md  = "csv/magdeburg-%s-wheelchair-values.csv" % (typ)
    
    # karlsruhe
    fig = plt.figure(tight_layout=True, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
    
    wheelchair_ka = pd.read_csv(csv_path_ka)
    x1 = wheelchair_ka.timestamp
    y1 = wheelchair_ka.yes
    x2 = wheelchair_ka.timestamp
    y2 = wheelchair_ka.no
    x3 = wheelchair_ka.timestamp
    y3 = wheelchair_ka.limited
    
    ax = plt.gca()
    line1, = ax.plot(x1, y1, '-', color='#2c7bb6', label='yes')
    line2, = ax.plot(x2, y2, '-', color='#d7191c', label='no')
    line3, = ax.plot(x3, y3, '-', color='#fdae61', label='limited')
    ax.legend(handles=[line1,line2,line3])
    #ax.set_ylim(0, 105)
    ax.set_ylabel('Anzahl values', fontsize=14)
    ax.set_xlabel('Zeit in Monaten', labelpad=10, fontsize=14)
    ax.set_xticks(x1[::6])
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.set_xticks(x1[::12])
    fig.align_labels()
    
    csv_path_out = "diagramme/%s-ka-wheelchair-values.png" % (typ)
    fig.savefig(csv_path_out, dpi=fig.dpi)
    
    # magdeburg
    fig = plt.figure(tight_layout=True, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
    
    wheelchair_md = pd.read_csv(csv_path_md)
    x1 = wheelchair_md.timestamp
    y1 = wheelchair_md.yes
    x2 = wheelchair_md.timestamp
    y2 = wheelchair_md.no
    x3 = wheelchair_md.timestamp
    y3 = wheelchair_md.limited

    ax = plt.gca()
    line1, = ax.plot(x1, y1, '-', color='#2c7bb6', label='yes')
    line2, = ax.plot(x2, y2, '-', color='#d7191c', label='no')
    line3, = ax.plot(x3, y3, '-', color='#fdae61', label='limited')
    ax.legend(handles=[line1,line2,line3])
    #ax.set_ylim(0, 105)
    ax.set_ylabel('Anzahl values', fontsize=14)
    ax.set_xlabel('Zeit in Monaten', labelpad=10, fontsize=14)
    ax.set_xticks(x1[::6])
    ax.xaxis.grid(True)
    ax.yaxis.grid(True)
    ax.set_xticks(x1[::12])
    fig.align_labels()
    
    csv_path_out = "diagramme/%s-md-wheelchair-values.png" % (typ)
    fig.savefig(csv_path_out, dpi=fig.dpi)

if __name__ == "__main__":
    diagram("stop_position")
    diagram("platform")