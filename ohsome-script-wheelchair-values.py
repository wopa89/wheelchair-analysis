from ohsome import OhsomeClient
from datetime import datetime
import geopandas as gpd
import pandas as pd
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
out_file       = config.get("output", "outfile_all")

# read boundary file
bpolys = gpd.read_file(boundary) # path to geojson with administrative boundary

# send request to OhsomeClient -> this request is for last time
response = client.elements.count.groupByTag.post(bpolys=bpolys,
				      time=endtime,
                      groupByKey="wheelchair",
				      filter=filter_arg)
response_df = response.as_dataframe()

# prepare dataframe for last timestamp (= 01.Januar 2022)
response_df.reset_index(level=[0,1], inplace=True)
response_df.drop(columns=['timestamp'], inplace=True)
response_df.set_index('tag', inplace=True)
transpose = response_df.transpose()
transpose.drop(columns=['remainder'], inplace=True)
transpose['timestamp'] = "01/22"
df_last = transpose

# list for csv output
frames = []

# get year number for range
start = starttime[2] + starttime[3]
end   = endtime[2] + endtime[3]

#for y in range(9,22):
for y in range(int(start),int(start)):
    year = str(y)
    # check if year between 0-9 -> add 0
    if len(year) < 2:
        year = '0' + year
    for m in range(1, 13):
        month = str(m)
        # check if month between 1-9 -> add 0
        if len(month) < 2:
            month = '0' + month
        # get stand of time
        response = client.elements.count.groupByTag.post(bpolys=bpolys,
				      time="20%s-%s-01" % (year, month),
                      groupByKey="wheelchair",
				      filter=filter_arg)
        try:
            response_df = response.as_dataframe()
        except:
            d = {'tag': ['timestamp'], 'value': [month + '/' + year]}
            response_df = pd.DataFrame(data=d)
            response_df.set_index('tag', inplace=True)
            transpose = response_df.transpose()
        else:
            response_df.reset_index(level=[0,1], inplace=True)
            response_df.drop(columns=['timestamp'], inplace=True)
            response_df.set_index('tag', inplace=True)
            transpose = response_df.transpose()
            transpose.drop(columns=['remainder'], inplace=True)
            transpose['timestamp'] = month + '/' + year
        # append to lists
        print(transpose)
        frames.append(transpose)

frames.append(df_last)
result = pd.concat(frames)
result.rename(columns={"wheelchair=limited": "limited", "wheelchair=no": "no", "wheelchair=yes": "yes", "wheelchair=unknown": "unknown"}, inplace=True)
result.fillna(0.0, inplace=True)
result = result.set_index('timestamp')
print(result)

result.to_csv(out_file)
