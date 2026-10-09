from pathlib import Path

# The data source URL
SOURCE_URL = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=43.65&longitude=-79.38"
    "&hourly=temperature_2m,precipitation"
    "&past_days=7&forecast_days=0"
    "&timezone=America%2FToronto"
)

# Request timeout limit in seconds
TIMEOUT = 10

# Relative path for the output summary
OUTPUT_PATH = Path("data/processed/summary.json")