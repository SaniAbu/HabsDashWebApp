import sqlite3
import pandas as pd
conn = sqlite3.connect('web_data.db')
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS runs")
c.execute('''CREATE TABLE IF NOT EXISTS runs (DasherID text, Date text, RunNo int, Pos int, Time text, pb int)''')
runs = pd.read_csv('csvs/rundata.csv')
runs.to_sql('runs', conn, if_exists='append', index=False)
c.execute('''SELECT * FROM runs''').fetchall()


c.execute("DROP TABLE IF EXISTS dashers")
c.execute('''CREATE TABLE IF NOT EXISTS dashers (DasherID text, House text, Year int, Streak int, TotalKm real)''')
dashers = pd.read_csv('csvs/dasherdata.csv')
dashers.to_sql('dashers', conn, if_exists='append', index=False)
c.execute('''SELECT * FROM dashers''').fetchall()

conn.commit()
conn.close()
