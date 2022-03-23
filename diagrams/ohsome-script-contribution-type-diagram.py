from ohsome import OhsomeClient
from datetime import datetime
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import sys

def diagram(typ):
    # karlsruhe
    csv_path_ka  = "csv/karlsruhe-contribution-type-%s.csv" % (typ)
    
    fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
    fig.subplots_adjust(hspace=0.1)
    fig.set_figwidth(9)
    fig.set_figheight(5)
    
    df_contribution_type_ka = pd.read_csv(csv_path_ka)
    x1 = df_contribution_type_ka.time
    y1 = df_contribution_type_ka.creation
    x2 = df_contribution_type_ka.time
    y2 = df_contribution_type_ka.deletion
    x3 = df_contribution_type_ka.time
    y3 = df_contribution_type_ka.geometry_change
    x4 = df_contribution_type_ka.time
    y4 = df_contribution_type_ka.tag_change
    
    max_value = [y1.max(), y2.max(), y3.max(), y4.max()]
    
    ax = plt.gca()
    line1, = ax1.plot(x1, y1, '-', color='#2c7bb6', label='creation')
    line2, = ax1.plot(x2, y2, '-', color='#d7191c', label='deletion')
    line3, = ax1.plot(x3, y3, '-', color='#fdb863', label='geometry_change')
    line4, = ax1.plot(x4, y4, '-', color='#b2abd2', label='tag_change')
    ax1.legend(handles=[line1,line2,line3, line4])
    ax2.plot(x1, y1, '-', color='#2c7bb6', label='creation')
    ax2.plot(x2, y2, '-', color='#d7191c', label='deletion')
    ax2.plot(x3, y3, '-', color='#fdb863', label='geometry_change')
    ax2.plot(x4, y4, '-', color='#b2abd2', label='tag_change')
    
    ax1.set_ylim(55,max(max_value)+10)
    ax2.set_ylim((0, 55))
    
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.set_xticks(x1[::6])
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax2.xaxis.tick_bottom()
    ax2.set_xticks(x1[::6])
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_xticks(x1[::12])
    
    # break markers
    d = 0.5
    kwargs = dict(marker=[(-1,-d), (1,d)], markersize=12, linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0,1],[0,0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0,1],[1,1], transform=ax2.transAxes, **kwargs)
    
    csv_path_out = "diagramme/karlsruhe-contribution-type-%s.png" % (typ)
    fig.savefig(csv_path_out, dpi=fig.dpi)
    
    # magdeburg
    csv_path_md  = "csv/magdeburg-contribution-type-%s.csv" % (typ)
    
    fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
    fig.subplots_adjust(hspace=0.1)
    fig.set_figwidth(9)
    fig.set_figheight(5)
    
    df_contribution_type_md = pd.read_csv(csv_path_md)
    x1 = df_contribution_type_md.time
    y1 = df_contribution_type_md.creation
    x2 = df_contribution_type_md.time
    y2 = df_contribution_type_md.deletion
    x3 = df_contribution_type_md.time
    y3 = df_contribution_type_md.geometry_change
    x4 = df_contribution_type_md.time
    y4 = df_contribution_type_md.tag_change
    
    ax = plt.gca()
    line1, = ax1.plot(x1, y1, '-', color='#2c7bb6', label='creation')
    line2, = ax1.plot(x2, y2, '-', color='#d7191c', label='deletion')
    line3, = ax1.plot(x3, y3, '-', color='#fdb863', label='geometry_change')
    line4, = ax1.plot(x4, y4, '-', color='#b2abd2', label='tag_change')
    ax1.legend(handles=[line1,line2,line3, line4])
    ax2.plot(x1, y1, '-', color='#2c7bb6', label='creation')
    ax2.plot(x2, y2, '-', color='#d7191c', label='deletion')
    ax2.plot(x3, y3, '-', color='#fdb863', label='geometry_change')
    ax2.plot(x4, y4, '-', color='#b2abd2', label='tag_change')
    
    ax1.set_ylim(55,max(max_value)+10)
    ax2.set_ylim((0, 55))
    
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.tick_top()
    ax1.set_xticks(x1[::6])
    ax1.xaxis.grid(True)
    ax1.yaxis.grid(True)
    ax2.xaxis.tick_bottom()
    ax2.set_xticks(x1[::6])
    ax2.xaxis.grid(True)
    ax2.yaxis.grid(True)
    ax2.set_xticks(x1[::12])
    
    # break markers
    d = 0.5
    kwargs = dict(marker=[(-1,-d), (1,d)], markersize=12, linestyle="none", color='k', mec='k', mew=1, clip_on=False)
    ax1.plot([0,1],[0,0], transform=ax1.transAxes, **kwargs)
    ax2.plot([0,1],[1,1], transform=ax2.transAxes, **kwargs)
    
    csv_path_out = "diagramme/magdeburg-contribution-type-%s.png" % (typ)
    fig.savefig(csv_path_out, dpi=fig.dpi)
    
if __name__ == "__main__":
    diagram("stops")
    diagram("platforms")