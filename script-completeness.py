from ohsome import OhsomeClient
from datetime import datetime
from configparser import ConfigParser
import geopandas as gpd
import pandas as pd
import numpy as np
import os
import sys

# open OhsomeClient
client = OhsomeClient()
print(client.start_timestamp) # --> '2007-10-08T00:00:00Z'
print(client.end_timestamp) # --> '2021-01-23T03:00Z'

# open ConfigFile
path_to_config = sys.argv[1]
config = ConfigParser()
config.read(path_to_config)
# get Parameters
starttime      = config.get("time", "starttime")
endtime        = config.get("time", "endtime")
boundary       = config.get("boundary", "path_to_boundary")
filter_arg     = config.get("filter", "filter_arg")
out_all        = config.get("output", "outfile_all")
out_wheelchair = config.get("output", "outfile_wheelchair")

# read boundary file
bpolys = gpd.read_file(boundary) # path to geojson with administrative boundary

# send request to OhsomeClient -> this request is for last time
response = client.elements.geometry.post(bpolys=bpolys,
				      time=endtime,
                      filter=filter_arg,
                      properties="tags")
# read request as geodataframe
df_last = response.as_dataframe()

# get number of osm objects
last_gesamt = len(df_last)
# last anteil
last_anteil = last_gesamt / last_gesamt * 100
# wheelchair gesamt
if 'wheelchair' in df_last.columns:
    wheelchair = df_last.loc[df_last['wheelchair'].notnull()]
    gesamt_w = len(wheelchair)
    last_anteil_w = gesamt_w / last_gesamt * 100
else:
    last_anteil_w = 0
print("Jahr: 22, Monat: 01, Stationen: %.2f, Wheelchair: %.2f" % (last_anteil, last_anteil_w))

# lists for csv output
list_stations = []
list_wheelchair = []
list_time = []

# get year number for range
start = starttime[2] + starttime[3]
end   = endtime[2] + endtime[3]

#for y in range(9,22):
for y in range(int(start),int(end)):
    year = str(y)
    if len(year) < 2:
        year = '0' + year
    for m in range(1, 13):
        month = str(m)
        # check if month between 1-9 -> add 0
        if len(month) < 2:
            month = '0' + month
        #print("Jahr: %s, Month: %s" % (year, month))
        list_time.append(month + '/' + year)
        # get stand of time
        response = client.elements.geometry.post(bpolys=bpolys,
				      time="20%s-%s-01" % (year, month),
                      filter=filter_arg,
                      properties="tags")
        try:
            response_df = response.as_dataframe()
        except:
            anteil = 0
            anteil_w = 0
        else:
            # objekte
            gesamt = len(response_df)
            anteil = gesamt / last_gesamt * 100
            # wheelchair
            if 'wheelchair' in response_df.columns:
                wheelchair = response_df.loc[response_df['wheelchair'].notnull()]
                gesamt_w = len(wheelchair)
                anteil_w = gesamt_w / gesamt * 100
            else:
                anteil_w = 0
        # append to lists
        list_stations.append(anteil)
        list_wheelchair.append(anteil_w)
        print("Jahr: %s, Monat: %s, Stationen: %.2f, Wheelchair: %.2f" % (year, month, anteil, anteil_w))

list_stations.append(last_anteil)
list_wheelchair.append(last_anteil_w)
list_time.append('01/22')
        
df_stations = pd.DataFrame({
    'time' : list_time,
    'value': list_stations
})
print(df_stations)
df_stations.to_csv(out_all, index=False)

df_wheelchair = pd.DataFrame({
    'time' : list_time,
    'value': list_wheelchair
})
print(df_wheelchair)
df_wheelchair.to_csv(out_wheelchair, index=False)
