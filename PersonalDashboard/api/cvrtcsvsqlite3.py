#Etc/UTC,IDK,GMT,-2208988800,0,2

import pandas as pd
import sqlite3

#df = pd.read_csv("assets/databases/time_zone.csv")
df = pd.read_csv("/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/time_zone.csv")


cols_to_drop = ['country_code', 'abbreviation', 'time_start', 'gmt_offset', 'dst']

df_filtered = df.drop(columns=cols_to_drop)

conn = sqlite3.connect("/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/cities.sqlite3")

df_filtered.to_sql('zone_name', conn, if_exists="replace", index=False)
conn.close()
print("Done")