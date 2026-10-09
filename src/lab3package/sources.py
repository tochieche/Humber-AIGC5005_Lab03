import requests
from .config import SOURCE_URL, TIMEOUT
from .models import HourlyRecord

class WeatherDataSource:
   #Fetches weather data from the API and parses it into HourlyRecord objects.

    def __init__(self, url=SOURCE_URL, timeout=TIMEOUT):
        self.url = url
        self.timeout = timeout

    def fetch(self):
        #Downloads data and returns a list of valid HourlyRecord instances.
        response = requests.get(self.url, timeout=self.timeout)
        response.raise_for_status()
        payload = response.json()

        hourly = payload.get("hourly", {})
        timestamps = hourly.get("time", [])
        temperatures = hourly.get("temperature_2m", [])
        precipitations = hourly.get("precipitation", [])

        records = []
        for ts, temp, precip in zip(timestamps, temperatures, precipitations):
            if ts is None or temp is None or precip is None:
                continue
            try:
                record = HourlyRecord(ts, temp, precip)
                records.append(record)
            except ValueError:
                continue

        return records