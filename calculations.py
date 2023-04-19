import sqlite3
import os
import numpy as np


def open_db(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(path+'/'+db_name)
    cur = con.cursor()
    return cur, con

def calc_wkly_avg_temp(cur,con, city):
    weekly_avgs = []
    #get city id that corresponds with the city string that was passed in
    cur.execute('SELECT id FROM master_city WHERE city=?',(city,))
    city_id = cur.fetchone()[0]
    #get date id that corresponds
    #full 8 weeks (omit last 3 days from 57-59):
    for first_day_of_week in range(0, 50, 7): 
        start = first_day_of_week
        end = first_day_of_week + 8
        cur.execute('SELECT temperature FROM temperature WHERE city_id = ? AND date_id > ? AND date_id < ?', (city_id, start, end))
        daily_temps = cur.fetchall()
        #turn daily temps list into a list of floats (not tuples anymore)
        temp_list = [x[0] for x in daily_temps]
        weekly_mean=np.mean(temp_list)
        #add weekly mean to list of weekly means
        weekly_avgs.append(int(weekly_mean))

    return weekly_avgs


def calc_wkly_avg_aqi(cur, con, city):
    weekly_avgs = []
    #get city id that corresponds with the city string that was passed in
    cur.execute('SELECT id FROM master_city WHERE city=?',(city,))
    city_id = cur.fetchone()[0]
    #get date id that corresponds
    #full 8 weeks (omit last 3 days from 57-59):
    for first_day_of_week in range(0, 50, 7): 
        start = first_day_of_week
        end = first_day_of_week + 8
        cur.execute('SELECT aqi FROM aqi_level2 WHERE city_id = ? AND date_id > ? AND date_id < ?', (city_id, start, end))
        daily_aqi = cur.fetchall()
        #turn daily temps list into a list of floats (not tuples anymore)
        aqi_list = [x[0] for x in daily_aqi]
        weekly_mean=np.mean(aqi_list)
        rounded_mean = int(np.round(weekly_mean))
        #add weekly mean to list of weekly means
        weekly_avgs.append(rounded_mean)

    return weekly_avgs

def calc_wkly_avg_humidity(cur,con,city):
    weekly_avgs = []
    #get city id that corresponds with the city string that was passed in
    cur.execute('SELECT id FROM master_city WHERE city=?',(city,))
    city_id = cur.fetchone()[0]
    #get date id that corresponds
    #full 8 weeks (omit last 3 days from 57-59):
    for first_day_of_week in range(0, 50, 7): 
        start = first_day_of_week
        end = first_day_of_week + 8
        cur.execute('SELECT humidity FROM Humidity_pct2 WHERE city_id = ? AND date_id > ? AND date_id < ?', (city_id, start, end))
        daily_temps = cur.fetchall()
        #turn daily temps list into a list of floats (not tuples anymore)
        temp_list = [x[0] for x in daily_temps]
        weekly_mean=int(np.mean(temp_list))
        #add weekly mean to list of weekly means
        weekly_avgs.append(weekly_mean)

    return weekly_avgs



def main(): 
    #connect to database
    cur, con = open_db('final.db')

    nyc_temp = calc_wkly_avg_temp(cur, con, "New+York")
    with open('temp.txt',"w") as f:
        f.write(f"Showing the average weekly temperatures for New York City from 1/1/23 - 2/28/23: {nyc_temp}\n")

    honolulu_temp =calc_wkly_avg_temp(cur, con, "Honolulu")
    with open('temp.txt',"a") as f:
        f.write(f"Showing the average weekly temperatures for New York City from 1/1/23 - 2/28/23: {honolulu_temp}\n")
    
    nyc_aqi = calc_wkly_avg_aqi(cur, con, "New+York")
    with open('aqi.txt',"w") as f:
        f.write(f"Showing the average weekly aqi for New York City from 1/1/23 - 2/28/23: {nyc_aqi}\n")

    honolulu_aqi = calc_wkly_avg_aqi(cur, con, "Honolulu")
    with open('aqi.txt',"a") as f:
        f.write(f"Showing the average weekly aqi for Honolulu from 1/1/23 - 2/28/23: {honolulu_aqi}\n")

    nyc_humidity = calc_wkly_avg_humidity(cur,con,"New+York")
    with open('humidity.txt',"w") as f:
        f.write(f"Showing the average weekly humidity percentage for New York City from 1/1/23 - 2/28/23: {nyc_humidity}\n")
    
    honolulu_humidity = calc_wkly_avg_humidity(cur,con,"Honolulu")
    with open('humidity.txt',"a") as f:
        f.write(f"Showing the average weekly humidity percentage for Honolulu from 1/1/23 - 2/28/23: {honolulu_humidity}\n")

main()



