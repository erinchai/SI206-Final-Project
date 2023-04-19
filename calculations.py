import sqlite3
import os
import numpy as np

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

    #write this city's 8 week averages to file
    with open('aqi.txt',"a") as f:
        f.write(f"{weekly_avgs}\n")

    return weekly_avgs

def main():
    path = os.path.dirname(os.path.abspath(__file__))
    con = sqlite3.connect(path + '/' + 'api.db')
    cur = con.cursor()
    calc_wkly_avg_aqi(cur, con, "New+York")
    calc_wkly_avg_aqi(cur, con, "Honolulu")
main()
