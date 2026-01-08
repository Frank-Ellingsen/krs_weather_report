# Activate virtual environment
$env:Path = ".\.venv\Scripts;" + $env:Path

# Run the weather script
python weather_snapshot.py

# Add updated files
git add docs/*.html
git add docs/*.csv

# Commit (ignore errors if nothing changed)
git commit -m "Auto-update $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>$null

# Push to GitHub
git push origin main
