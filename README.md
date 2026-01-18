# 🌦 KRS Weather Report

## Business Case

Understanding weather patterns is essential for planning, operations, and risk management.
This project analyzes and visualizes historical weather data for the Kristiansand (KRS) area
to identify trends and seasonal patterns.

## Data

- Source: Weather API / historical weather dataset
- Granularity: Daily measurements
- Metrics include temperature, precipitation, and wind conditions

## Tools & Technologies

- Python
- API data ingestion
- Pandas
- Matplotlib / Seaborn
- (Optional) Power BI / dashboarding tools

## What I Did

- Retrieved weather data programmatically using an API
- Cleaned and transformed time-series data
- Aggregated metrics to analyze trends over time
- Built visualizations to communicate seasonal and long-term patterns

## Key Insights

- Clear seasonal temperature trends across the year
- Periods of increased precipitation identified
- Long-term patterns useful for planning and forecasting

## Why This Project Matters

This project demonstrates my ability to:

- Work with external APIs
- Handle time-series data
- Turn raw data into clear, interpretable insights

## Next Improvements

- Add automated data refresh
- Create an interactive dashboard
- Extend analysis with anomaly detection or forecasting

# KRS Weather Static Snapshot

This project generates **static weather snapshots** from a local MySQL database and publishes them to GitHub as HTML and CSV files.
The script pulls the **weather records**, creates **Plotly visualizations**, and exports them to the `docs/` folder for GitHub Pages hosting.

The project is designed to run **automatically every hour** using Windows Task Scheduler, producing a continuously updated static weather dashboard.

---

## 🚀 Features

- Connects to a local MySQL database (`krs_weather_db`)
- Fetches weather observations
- Generates:
  - `current_weather.html` — summary indicator dashboard
  - `temperature_trend.html` — temperature trend line chart
  - `weather_records.csv` — static data snapshot
- Outputs files to:
  - `docs/` for GitHub Pages
  - `output/` for local storage
- Supports environment variables via `.env`
- Can be automated with Windows Task Scheduler

---

## 📂 Project Structure

krs-weather-static/
│
├── weather_snapshot.py # Main script
├── requirements.txt # Python dependencies
├── README.md # Project documentation
├── .gitignore # Git ignore rules
│
├── docs/ # GitHub Pages output (committed)
│ ├── index.html
│ ├── current_weather.html
│ └── temperature_trend.html
│
├── output/ # Local output (ignored by git)
│ ├── weather_records.csv
│ ├── current_weather.html
│ └── temperature_trend.html
│
└── .env
