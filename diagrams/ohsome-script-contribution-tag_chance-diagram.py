from ohsome import OhsomeClient
from datetime import datetime
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import sys

def diagram(area):
    csv_path_w = "csv/%s-contribution-tag_change.csv" % (area)
    csv_path_n = "csv/%s-contribution-tag_change_name.csv" % (area)
    
    df_w = pd.read_csv(csv_path_w)
    df_n = pd.read_csv(csv_path_n)
    x = df_w.year
    y1 = df_w.wheelchair
    y2 = df_n.name
    
    max_w = y1.max()
    max_n = y2.max()
    
    if max_w > max_n:
        max_all = max_w
    else:
        max_all = max_n
    
    if max_all > 100:
        #fig = plt.figure(tight_layout=True, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
        # create subplots with outliers
        fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
        fig.subplots_adjust(hspace=0.1)
        fig.set_figwidth(8)
        fig.set_figheight(5)
    
        ax1.bar(x-0.1, y1, color="b", width=0.2)
        ax1.bar(x+0.1, y2, color="r", width=0.2)
        ax2.bar(x-0.1, y1, color="b", width=0.2)
        ax2.bar(x+0.1, y2, color="r", width=0.2)
        ax1.legend(labels=['Änderungen an Tag wheelchair', 'Änderungen an Tag Haltestellen-Name'])
    
        # set outliers above 85 until max
        ax1.set_ylim(105,max_all+10)
        ax2.set_ylim((0, 105))
    
        ax1.spines['bottom'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        ax1.xaxis.tick_top()
        ax1.set_xticks(x)
    
        # break markers
        d = 0.5
        kwargs = dict(marker=[(-1,-d), (1,d)], markersize=12, linestyle="none", color='k', mec='k', mew=1, clip_on=False)
        ax1.plot([0,1],[0,0], transform=ax1.transAxes, **kwargs)
        ax2.plot([0,1],[1,1], transform=ax2.transAxes, **kwargs)
    
        csv_path_out = "diagramme/%s-contribution-tag_change_name.png" % (area)
        fig.savefig(csv_path_out, dpi=fig.dpi)
    else:
        fig = plt.figure(tight_layout=True, figsize=(8, 5), dpi=100, facecolor='w', edgecolor='k')
        
        ax = plt.gca()
        ax.bar(x-0.1, y1, color="b", width=0.2)
        ax.bar(x+0.1, y2, color="r", width=0.2)
        ax.legend(labels=['Änderungen an Tag wheelchair', 'Änderungen an Tag Haltestellen-Name'])
        ax.set_xticks(x)
    
        csv_path_out = "diagramme/%s-contribution-tag_change_name.png" % (area)
        fig.savefig(csv_path_out, dpi=fig.dpi)

if __name__ == "__main__":
    diagram("karlsruhe")
    diagram("magdeburg")
