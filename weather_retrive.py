
import mysql.connector
import pandas as pd

from mysql.connector import Error

try:
    # Connect to MySQL
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='Pia&Victor0935',
        database='krs_weather_db'
    )

    if conn.is_connected():
        query = "SELECT * FROM krs_weather_data"
        weather_data = pd.read_sql(query, conn)
        
    weather_data['year'] = weather_data['time_stamp'].dt.year
    weather_data['month'] = weather_data['time_stamp'].dt.month
    weather_data['day'] = weather_data['time_stamp'].dt.day
    weather_data['hour'] = weather_data['time_stamp'].dt.hour    
        
    weather_data.to_csv('weather_data.csv',index=False)
    
    weather_data.to_pickle('weather_data.pkl')
    

except Error as e:
    print(f"Error: {e}")

finally:
    if conn.is_connected():
        conn.close()

