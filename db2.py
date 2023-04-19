import sqlite3
import json
import os
import datetime
import requests
from datetime import date, timedelta
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def get_city_temps(lat, long):
    temp_data = {}
    api_key = '7cc1d749d4b9f64be87f15ea8cd27ec8'
    start_date = datetime.datetime(2023, 1, 1)
    # Loop over each week (can only get 7 days of data at once)
    for i in range(0, 63, 7):
        # Calculate the start and end dates for the current request
        start = start_date + datetime.timedelta(days=i)
        end = min(start_date + datetime.timedelta(days=6+i), datetime.datetime(2023, 2, 28))

        # Format the start and end dates for the API request
        start_unix = str(int(start.timestamp()))
        end_unix = str(int(end.timestamp()))

        # Make the API request for the temperature data
        
        url = f'https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={long}&type=hour&start={start_unix}&cnt={end_unix}&units=imperial&appid={api_key}'

        #store whole week's data 
        resp  = requests.get(url)
    # print(response.text)
        data = json.loads(resp.text)
    # print(data) 
        if 'list' in data:
            #loop through each day
            #if on last loop 
            if end_unix == '1677560400': 
                for day in range(0, 49, 24): 
                    index = day
                #grab all 24 temps for that day 
                    for hour in range(24):
                        hourly_temps = []
                        hourly_temps.append(float(data['list'][index]['main']['temp']))
                        index += 1
                    #find the avg temp of the day and store it 
                    daily_temp = sum(hourly_temps)/len(hourly_temps) 
                    temp_data[start.strftime('%Y-%m-%d')] = daily_temp
                    #increment date to next day 
                    start = start + datetime.timedelta(days=1)
            #normal loop with all 7 days of data to be grabbed 
            else: 
                for day in range(0, 168, 24): 
                    index = day
                    #grab all 24 temps for that day 
                    for hour in range(24):
                        hourly_temps = []
                        hourly_temps.append(float(data['list'][index]['main']['temp']))
                        index += 1
                    #find the avg temp of the day and store it 
                    daily_temp = sum(hourly_temps)/len(hourly_temps) 
                    temp_data[start.strftime('%Y-%m-%d')] = daily_temp
                    #increment date to next day 
                    start = start + datetime.timedelta(days=1)

    #print(temp_data)
    return temp_data

def open_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn

def fill_date_table(cur, con):
    id= 1
    first_day = datetime.datetime(2023,1,1)
    num_days = 59
    datelist = [(first_day + datetime.timedelta(days = x)).strftime("%Y-%m-%d")for x in range(59)]
    cur.execute('CREATE TABLE IF NOT EXISTS master_date (id INTEGER PRIMARY KEY, date TEXT)')
    for date in datelist:
        cur.execute("INSERT OR IGNORE INTO master_date (id, date) VALUES (?, ?)", (id, date))
        id += 1
        con.commit()

def fill_city_table(cur, con):
    city_lst = [("New+York", "40.7128","74.0060"), ("Honolulu","21.3099", "157.8581")]
    id= 1
    for city, lat,long in city_lst:
        cur.execute('CREATE TABLE IF NOT EXISTS master_city (id INTEGER PRIMARY KEY, city TEXT, lat TEXT, long TEXT)')
        cur.execute("INSERT OR IGNORE INTO master_city (id, city, lat, long) VALUES (?, ?, ?, ?)", (id, city, lat, long))
        id += 1
        con.commit()


def make_weather_table(data, cur, conn, start):
    city = 'New+York'
    if start + 25 < 119:
        for i in range(start,start + 25):
            row  = data[i]
            if i > 58:
                city = 'Honolulu'
            cur.execute('SELECT id FROM master_city WHERE city=?',(city,))
            city_id = cur.fetchone()[0]
            temperature = float(row[1])
            date = row[0]
            cur.execute('SELECT id FROM master_date WHERE date =?', (date,))
            date_id = cur.fetchone()[0]
            cur.execute('''INSERT INTO temperature (temperature, city_id, date_id)
                            VALUES (?,?,?)''', (temperature,city_id, date_id))
            conn.commit()
            
    else: 
        for i in range(start, 118):
            row = data[i]
            city = 'Honolulu'
            cur.execute('SELECT id FROM master_city WHERE city=?',(city,))
            city_id = cur.fetchone()[0]
            temperature = float(row[1])
            date = row[0]
            cur.execute('SELECT id FROM master_date WHERE date =?', (date,))
            date_id = cur.fetchone()[0]
            cur.execute('''INSERT INTO temperature (temperature, city_id, date_id)
                            VALUES (?,?,?)''', (temperature,city_id, date_id))
            conn.commit()



def main():
    #get 2 dictionaries of date and temp for each city
    honolulu = get_city_temps(21.315603, -157.858093)
    nyc = get_city_temps(40.71278, -74.00611)

    print('Finished creating JSONS')
    #turn jsons into one giant list (used in creating database)
    weather_lst = list(nyc.items())
    weather2_lst = list(honolulu.items())
    weather_lst.extend(weather2_lst)
  
    cur, conn = open_db('final.db')
    fill_date_table(cur, conn)
    fill_city_table(cur, conn)
    # cur.execute("DROP TABLE temperature")
   # check current row in database in main (ROW_NUMBER)
   
    cur.execute('''CREATE TABLE IF NOT EXISTS temperature (temperature REAL, city_id INTEGER, date_id INTEGER)''')
    cur.execute('''SELECT COUNT(*) FROM temperature''')


    ct = cur.fetchall()
    ct = (ct[0])
    ct = ct[0]

   #to check you can delete database and see if rows are populating 
    new_start = 0 
    if ct < 118: 
        if ct == 0: 
            print("adding lines 1-25")
        elif ct == 25:
            new_start = 25
            print("adding lines 25-50")
        elif ct == 50:
            new_start = 50
            print("adding lines 50-75")
        elif ct == 75: 
            new_start = 75
            print("adding lines 75-100")
        elif ct == 100: 
            new_start = 100
            print("adding lines 100-118")

        make_weather_table(weather_lst, cur, conn, new_start)


if __name__ == "__main__":
    main()