import requests
import json
import sqlite3
import os
import datetime
import numpy as np
import csv

# key1=184adb6b28bd4286ae9184147230804
# con = sqlite3.connect("irenehumidity.db")
# cur = con.cursor()

def open_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(path + '/' + db_name)
    cur = con.cursor()
    return cur, con

def get_humidity_data(con,cur):
    
    cur.execute('CREATE TABLE IF NOT EXISTS Humidity_pct2 (city_id INTEGER, date_id INTEGER, humidity INTEGER)')
    cur.execute("SELECT COUNT(0) FROM Humidity_pct2")
    count = int(cur.fetchone()[0])
    current = count + 1
    index = count//19 
    print(f'starting filling humidity table, there are currently {count} rows in the table')

    place_time = [("New+York","2023-01-01", "2023-01-19"),
              ("New+York", "2023-01-20", "2023-02-08"),
              ("New+York","2023-02-09", "2023-02-28"),
              ("Honolulu","2023-01-01", "2023-01-19"),
              ("Honolulu", "2023-01-20", "2023-02-08"),
              ("Honolulu","2023-02-09", "2023-02-28")]
    
    new_dict = {}
    humid_list = []
    date_list = []
    try:
        place, start, end = place_time[index]
        query=f'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=184adb6b28bd4286ae9184147230804&q={place}&format=json&date={start}&enddate={end}&includelocation=yes&tp=24&lang=eng'
        
        try:
            response = requests.get(query)
            data = json.loads(response.text)
            # print(data)
            content = data["data"]['weather']
            # date = content['date']
            # print(content)
            
        except:
            print(f'Error: {response.status_code}')
            return None
        
        # for weather in range(0,len(content),24):
        for weather in content:
            # print(weather)
            humidity = weather['hourly'][0]['humidity']
            # print(humidity)
            cur.execute("SELECT id FROM master_city WHERE city=?", (place,))
            city_id = cur.fetchone()[0]
            date = weather['date']
            cur.execute("SELECT id FROM master_date WHERE date=?", (date,))
            date_id = cur.fetchone()[0]
            # print(date_id)
            cur.execute("INSERT OR IGNORE INTO Humidity_pct2 (city_id, date_id, humidity) VALUES (?, ?, ?)", ( city_id, date_id, humidity))
            # cur.execute("INSERT OR IGNORE INTO Humidity_pct (id, humidity) VALUES (?, ?)", (current, humidity))

            
            current += 1
            con.commit()
    except:
        return None 
    
# get_humidity_data()

def fill_date_table(con,cur):
    id= 1
    first_day = datetime.datetime(2023,1,1)
    num_days = 59
    datelist = [(first_day + datetime.timedelta(days = x)).strftime("%Y-%m-%d")for x in range(59)]
    cur.execute('CREATE TABLE IF NOT EXISTS master_date (id INTEGER PRIMARY KEY, date TEXT)')
    for date in datelist:
        cur.execute("INSERT OR IGNORE INTO master_date (id, date) VALUES (?, ?)", (id, date))
        id += 1
        con.commit()

# fill_date_table()

def fill_city_table(con,cur):
    city_lst = [("New+York", "40.7128","74.0060"), ("Honolulu","21.3099", "157.8581")]
    id= 1
    for city, lat,long in city_lst:
        cur.execute('CREATE TABLE IF NOT EXISTS master_city (id INTEGER PRIMARY KEY, city TEXT, lat TEXT, long TEXT)')
        cur.execute("INSERT OR IGNORE INTO master_city (id, city, lat, long) VALUES (?, ?, ?, ?)", (id, city, lat, long))
        id += 1
        con.commit()
    
# fill_city_table()


def main():
     cur, con = open_db('final.db')
    #  fill_city_table(con,cur)
    #  fill_date_table(con,cur)
     get_humidity_data(con,cur)


main()
     



