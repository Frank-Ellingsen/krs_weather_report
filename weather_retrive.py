
import subprocess
import time
import pandas as pd
import mysql.connector
from mysql.connector import Error
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
from dotenv import load_dotenv
import os

# ✅ Load environment variables
load_dotenv()



# ✅ Debug: Check environment variables
db_user = os.getenv("KRS_DB_USER")
db_password = os.getenv("KRS_DB_PASSWORD")

print(f"🔍 Debug: DB User loaded: {db_user if db_user else '❌ Missing'}")
print(f"🔍 Debug: DB Password loaded: {'✅ Loaded' if db_password else '❌ Missing'}")

# ✅ Check MySQL service status before starting
print("\nChecking MySQL service status...")
service_status = subprocess.run(["sc", "query", "MySQL80"], capture_output=True, text=True)

if "RUNNING" in service_status.stdout:
    print("✅ MySQL service is already running.")
else:
    print("⚠️ MySQL service is not running. Attempting to start...")
    try:
        subprocess.run(["net", "start", "MySQL80"], shell=True, check=True)
        print("✅ MySQL service started successfully.")
    except subprocess.CalledProcessError as e:
        print(f"❌ Could not start MySQL service: {e}")
        print("➡ Please check if MySQL is installed and service name is correct (MySQL80).")
        raise SystemExit("Stopping script because MySQL service could not start.")

# ✅ Database connection details
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': db_user,
    'password': db_password,
    'database': 'krs_weather_db'
}

if conn.is_connected():
    query = "SELECT * FROM krs_weather_data"
    weather_data = pd.read_sql(query, conn)
        
    weather_data['year'] = weather_data['time_stamp'].dt.year
    weather_data['month'] = weather_data['time_stamp'].dt.month
    weather_data['day'] = weather_data['time_stamp'].dt.day
    weather_data['hour'] = weather_data['time_stamp'].dt.hour    
        
    weather_data.to_csv('weather_data.csv',index=False)
    
    weather_data.to_pickle('weather_data.pkl')
    

