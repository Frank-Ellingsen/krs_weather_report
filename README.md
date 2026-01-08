# KRS Weather Static Snapshot

This project generates **static weather snapshots** from a local MySQL database and publishes them to GitHub as HTML and CSV files.
The script pulls the **latest 10 weather records**, creates **Plotly visualizations**, and exports them to the `docs/` folder for GitHub Pages hosting.

The project is designed to run **automatically every hour** using Windows Task Scheduler, producing a continuously updated static weather dashboard.

---

## 🚀 Features

- Connects to a local MySQL database (`krs_weather_db`)
- Fetches the latest 10 weather observations
- Generates:
  - `current_weather.html` — summary indicator dashboard
  - `temperature_trend.html` — temperature trend line chart
  - `last_10_weather_records.csv` — static data snapshot
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
│ ├── last_10_weather_records.csv
│ ├── current_weather.html
│ └── temperature_trend.html
│
└── .env
