
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

# ✅ Output folder
OUTPUT_DIR = Path("docs")
OUTPUT_DIR.mkdir(exist_ok=True)

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

# ✅ Connect with retry logic and detailed diagnostics
conn = None
for attempt in range(3):
    try:
        print(f"\nAttempt {attempt+1}: Connecting to MySQL...")
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("✅ Connected to MySQL successfully.")
            break
    except Error as e:
        print(f"❌ Attempt {attempt+1} failed: {e}")
        if attempt == 2:
            print("\n➡ Final check:")
            print("   - Is MySQL service running? (Check with `sc query MySQL80`)")
            print("   - Are credentials correct in .env? (KRS_DB_USER, KRS_DB_PASSWORD)")
            print("   - Does database `krs_weather_db` exist?")
        time.sleep(5)
else:
    raise Exception("❌ Failed to connect after 3 attempts. Please verify service and credentials.")

# ✅ Fetch last 100 rows dynamically
try:
    cursor = conn.cursor()
    query = """
    SELECT id, location, time_stamp, temp_c, humidity, cond, wind_kph, pressure_mb
    FROM krs_weather_data
    ORDER BY id DESC LIMIT 100;
    """
    cursor.execute(query)
    rows = cursor.fetchall()

    df = pd.DataFrame(
        rows,
        columns=['id', 'location', 'time_stamp', 'temp_c', 'humidity', 'cond', 'wind_kph', 'pressure_mb']
    )
    df['time_stamp'] = pd.to_datetime(df['time_stamp'])
    df['wind_mps'] = df['wind_kph'] / 3.6

finally:
    if conn.is_connected():
        cursor.close()
        conn.close()
        print("\n✅ Connection closed (MySQL service remains running).")

# ✅ Save static CSV snapshot
csv_path = OUTPUT_DIR / "last_100_weather_records.csv"
df.to_csv(csv_path, index=False)
print(f"✅ Saved CSV snapshot to {csv_path}")


# ✅ Weather Icons Mapping (Case-Insensitive)

icons = {
    'sunny': '☀️',
    'clear': '☀️',
    'patchy rain nearby': '🌦️',
    'partly cloudy': '⛅',
    'mist': '🌫️',
    'cloudy': '☁️',
    'overcast': '🌥️',
    'light rain': '🌦️',
    'moderate rain': '🌧️',
    'heavy rain': '🌧️💦',
    'rain': '🌧️',
    'light snow': '🌨️',
    'snow': '❄️',
    'heavy snow': '❄️❄️',
    'thunderstorm': '⛈️',
    'fog': '🌫️',
    'windy': '🌬️',
    'sleet': '🌨️🌧️',
    'light sleet': '🌨️🌦️',
    'moderate sleet': '🌨️🌧️',
    'heavy sleet': '🌨️🌧️💦',
    'moderate or heavy sleet': '🌨️🌧️💦'
}




def get_icon(condition):
    """Return weather icon for given condition (case-insensitive)."""
    return icons.get(condition.lower(), '❓')  # Default icon for unknown conditions

# ✅ Latest record
latest = df.iloc[0]
weather_icon = get_icon(latest['cond'])

# ✅ Chart 1: Current Weather Summary
fig_current = go.Figure()
fig_current.add_trace(go.Indicator(
    mode="number",
    value=latest['temp_c'],
    title={"text": f"{weather_icon} {latest['cond']}<br><span style='font-size:0.8em;color:gray'>{latest['location']} | {latest['time_stamp']}</span>"},
    number={"suffix": "°C"}
))
fig_current.add_annotation(
    text=f"Humidity: {latest['humidity']}%<br>Pressure: {latest['pressure_mb']} mb<br>Wind: {latest['wind_mps']:.1f} m/s",
    x=0.5, y=-0.2, showarrow=False
)
fig_current.update_layout(title="Current Weather Summary", height=400)

current_html = OUTPUT_DIR / "current_weather.html"
fig_current.write_html(current_html)
print(f"✅ Saved current weather chart to {current_html}")

# ✅ Chart 2: Temperature Trend for Last 10 Records
fig_trend = px.line(
    df.sort_values('time_stamp'),
    x='time_stamp',
    y='temp_c',
    title='Temperature Trend',
    markers=True
)
fig_trend.update_traces(line_color='orange')

trend_html = OUTPUT_DIR / "temperature_trend.html"
fig_trend.write_html(trend_html)
print(f"✅ Saved temperature trend chart to {trend_html}")
