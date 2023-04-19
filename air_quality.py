import requests
import json
import sqlite3
import os
import datetime
import numpy as np
import csv
import math

con = sqlite3.connect("final.db")
cur = con.cursor()


api_key1 = "2e539c9834404d3a8aec91261c1a2411"
api_key2 = "19e9845d47024ab6a9ee367d1833e7d7"
api_key3 = "a025d8a2b51f44f386bb80a3f571df53"

def open_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(path + '/' + db_name)
    cur = con.cursor()
    return cur, con

#gets the api index from 01-01- 02-28

def get_aqi_data(cur, con):
    
    cur.execute('CREATE TABLE IF NOT EXISTS aqi_level2 (city_id INTEGER, date_id INTEGER, aqi INTEGER)')
    cur.execute("SELECT COUNT(*) FROM aqi_level2")
    count = int(cur.fetchone()[0])
    current = count + 20
    index = current//21 
    print(f'starting filling aqi table, there are currently {count} rows in the table, inserting index {index}')

    place_time = [("40.7128","74.0060","2023-01-01", "2023-01-21"),
              ("40.7128","74.0060", "2023-01-22", "2023-02-11"),
              ("40.7128", "74.0060","2023-02-12", "2023-02-28"),
              ("21.3099", "157.8581", "2023-01-01", "2023-01-21"),
              ("21.3099", "157.8581", "2023-01-22", "2023-02-11"),
              ("21.3099", "157.8581","2023-02-12", "2023-02-28")]
    
    new_dict = {}
    aqi_list = []
    date_list = []
    try:
        lat, long, start, end = place_time[index]
    except:
        return None
    query = f'https://api.weatherbit.io/v2.0/history/airquality?lat={lat}&lon=-{long}&start_date={start}&end_date={end}&tz=local&key=2e539c9834404d3a8aec91261c1a2411'
    try:
        response = requests.get(query)
        data = json.loads(response.text)
        content = data["data"]
        
    except:
        print(f'failed on {query}')
        return None
    for i in range(0,len(content),24):
        info = content[i]
        aqi_level = int(info["aqi"])
        cur.execute("SELECT id FROM master_city WHERE lat=? AND long=?", (lat,long))
        city_id = cur.fetchone()[0]
        date = info['timestamp_local'].split('T')[0]
        cur.execute("SELECT id FROM master_date WHERE date=?", (date,))
        date_id = cur.fetchone()[0]
        cur.execute("INSERT OR IGNORE INTO aqi_level2 (city_id, date_id, aqi) VALUES (?, ?,?)", ( city_id, date_id, aqi_level))

        current += 1
        con.commit()



def date_table(cur, con, row):
    first_day = datetime.datetime(2023,1,1)
    num_days = 59
    datelist = [(first_day + datetime.timedelta(days = x)).strftime("%Y-%m-%d")for x in range(59)]
    if row + 25 < 60: 
        for i in range(row, row + 25):
            k = i + 1
            date = datelist[i]
            cur.execute("INSERT OR IGNORE INTO master_date (id, date) VALUES (?, ?)", (k, date))
            con.commit()
    else: 
        for i in range(row, 59):
            k = i + 1
            date = datelist[i]
            cur.execute("INSERT OR IGNORE INTO master_date (id, date) VALUES (?, ?)", (k, date))
            con.commit()
    


def city_table(cur, con):
    city_lst = [("New+York", "40.7128","74.0060"), ("Honolulu","21.3099", "157.8581")]
    id= 1
    for city, lat,long in city_lst:
        cur.execute('CREATE TABLE IF NOT EXISTS master_city (id INTEGER PRIMARY KEY, city TEXT, lat TEXT, long TEXT)')
        cur.execute("INSERT OR IGNORE INTO master_city (id, city, lat, long) VALUES (?, ?, ?, ?)", (id, city, lat, long))
        id += 1
        con.commit()

def main():
    cur, con = open_db('final.db')

    cur.execute('CREATE TABLE IF NOT EXISTS master_date (id INTEGER PRIMARY KEY, date TEXT)')
    cur.execute('''SELECT COUNT(*) FROM master_date''')
    row= cur.fetchall()
    row= (row[0])
    row= row[0]

   #to check you can delete database and see if rows are populating 
    if row < 60: 
        if row== 0: 
            print("adding lines 1-25")
        elif row== 25:
            print("adding lines 25-50")
        elif row== 50:
            print("adding lines 50-59")
    date_table(cur, con, row)
    city_table(cur, con)
    get_aqi_data(cur, con) 
main()
    













