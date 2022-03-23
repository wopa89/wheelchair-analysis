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
                      properties="metadata, tags")
response_df = response.as_dataframe()
response_df.reset_index(inplace=True)

# lists for csv output
list_time = []
list_creation = []
list_deletion = []
list_geometry_change = []
list_tag_change = []

# get year number for range
start = starttime[2] + starttime[3]
end   = endtime[2] + endtime[3]

for y in range(int(start),int(end)):
    year = str(y)
    # check if year between 0-9 -> add 0
    if len(year) < 2:
        year = '0' + year
    for m in range(1, 13):
        month = str(m)
        # check if month between 1-9 -> add 0
        if len(month) < 2:
            month = '0' + month
        # get datetime
        time1_str = '%s/01/%s 00:00:00' % (month, year)
        time1 = datetime.strptime(time1_str, '%m/%d/%y %H:%M:%S')
        month2 = int(month) + 1
        if month2 <= 12:
            time2_str = '%s/01/%s 00:00:00' % (month2, year)
            time2 = datetime.strptime(time2_str, '%m/%d/%y %H:%M:%S')
            df = response_df[(response_df['@timestamp'] < time2) & (response_df['@timestamp'] >= time1)]
            df_creation = df[df['@creation']==True]
            df_deletion = df[df['@deletion']==True]
            df_geometry_change = df[df['@geometryChange']==True]
            df_tag_change = df[df['@tagChange']==True]
            list_creation.append(len(df_creation))
            list_deletion.append(len(df_deletion))
            list_geometry_change.append(len(df_geometry_change))
            list_tag_change.append(len(df_tag_change))
            list_time.append(month + '/' + year)
        else:
            #day = '31'
            month2 = '01'
            year2 = int(year) + 1
            time2_str = '%s/01/%s 00:00:00' % (month2, str(year2))
            time2 = datetime.strptime(time2_str, '%m/%d/%y %H:%M:%S')
            df = response_df[(response_df['@timestamp'] < time2) & (response_df['@timestamp'] >= time1)]
            df_creation = df[df['@creation']==True]
            df_deletion = df[df['@deletion']==True]
            df_geometry_change = df[df['@geometryChange']==True]
            df_tag_change = df[df['@tagChange']==True]
            list_creation.append(len(df_creation))
            list_deletion.append(len(df_deletion))
            list_geometry_change.append(len(df_geometry_change))
            list_tag_change.append(len(df_tag_change))
            if year2 < 22:
                list_time.append(month + '/' + str(year2))
            else:
                list_creation.append(len(df_creation))
                list_deletion.append(len(df_deletion))
                list_geometry_change.append(len(df_geometry_change))
                list_tag_change.append(len(df_tag_change))
                list_time.append('01/22')
                list_time.append('01/22')

df_result = pd.DataFrame({
    'time' : list_time,
    'creation' : list_creation,
    'deletion' : list_deletion,
    'geometry_change' : list_geometry_change,
    'tag_change' : list_tag_change
})
print(df_result)
df_result.to_csv(out_file, index=False)
