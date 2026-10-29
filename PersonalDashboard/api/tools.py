'''

import pandas as pd
import sqlite3

#df = pd.read_csv("assets/databases/time_zone.csv")
df = pd.read_csv("/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/time_zone.csv")


cols_to_drop = ['country_code', 'abbreviation', 'time_start', 'gmt_offset', 'dst']

df_filtered = df.drop(columns=cols_to_drop)

conn = sqlite3.connect("/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/cities.sqlite3")

df_filtered.to_sql('zone_name', conn, if_exists="replace", index=False)
conn.close()
print("Done")'''

import json
import sqlite3

with open('/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/timezones.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

conn = sqlite3.connect('/home/matthew/Desktop/PersonalDashboardVersions/PersonalDashboard/assets/databases/timezones.sqlite3')
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS timezones (
        id         TEXT PRIMARY KEY,
        baseOffset TEXT NOT NULL
    )
''')

cur.executemany(
    'INSERT OR REPLACE INTO timezones (id, baseOffset) VALUES (?, ?)',
    [(row["id"], row['baseOffset']) for row in data]
)

conn.commit()
conn.close()
print(f"Inserted {len(data)} rows into timezones.sqlite3")