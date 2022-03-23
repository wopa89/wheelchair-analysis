from ohsome import OhsomeClient
from datetime import datetime
import geopandas as gpd
import pandas as pd
from configparser import ConfigParser
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
starttime  = config.get("time", "starttime")
endtime    = config.get("time", "endtime")
boundary   = config.get("boundary", "path_to_boundary")
filter_arg = config.get("filter", "filter_arg")
out_file   = config.get("output", "outfile")

# read boundary file
bpolys = gpd.read_file(boundary) # path to geojson with administrative boundary

# send request to OhsomeClient
response = client.contributions.geometry.post(bpolys=bpolys,
				      time="%s,%s" % (starttime, endtime),
                      filter=filter_arg,
                      showMetadata="yes",
                      properties="Metadata, tags",
                      clipGeometry="false")
                      
response_df = response.as_dataframe()
response_df.reset_index(inplace=True)
print("Total Changes: %i" % len(response_df))

# get all tagchanges
tagchange_df = response_df[response_df['@tagChange'] == True]

# filter data where osmId only 1 count
v = tagchange_df['@osmId'].value_counts()
value_df = tagchange_df[tagchange_df['@osmId'].isin(v.index[v.gt(1)])]
# fill all NaN values in column name with Null
value_df['name'] = value_df['name'].fillna('Null')

# get only relevant columns and sort by column osmId
name_df_unsorted = value_df[['@timestamp','@osmId', '@version', 'name']]
name_df = name_df_unsorted.sort_values(by=['@osmId', '@version'])

# compare rows with previous rows for to look for changes in osmID and name -> different objects needs to be identified and name change
name_df['changed_id'] = name_df['@osmId'].ne(name_df['@osmId'].shift().bfill()).astype(int)
name_df['changed'] = name_df['name'].ne(name_df['name'].shift().bfill()).astype(int)

# if change_id is 0 and changed is 1 then a tagChange on tag name occured
df = name_df[(name_df['changed_id'] == 0) & (name_df['changed'] == 1)]
# change_id (different object) needs to be identified otherwise name change would occure more often

# get year of timestamp
df['year'] = df['@timestamp'].dt.year
count_name = df['year'].value_counts()
name = count_name.sort_index()
name.rename('name', inplace=True)

# get all timestamps
tagchange_df['year'] = tagchange_df['@timestamp'].dt.year
count_all = tagchange_df['year'].value_counts()
all_s = count_all.sort_index()
all_s.rename('gesamt', inplace=True)

# merge series
final = pd.concat([all_s, name], axis=1)
final['name'] = final['name'].fillna(0)
final['gesamt'] = final['gesamt']-final['name']
final.reset_index(inplace=True)
final = final.rename(columns={'index' : 'year'})
print(final)

final.to_csv(out_file, index=False)
