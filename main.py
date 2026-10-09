import sys
import requests
from lab3package import WeatherDataSource, ReportBuilder
from lab3package.config import OUTPUT_PATH, SOURCE_URL

def main():
    try:
        source = WeatherDataSource(SOURCE_URL)
        records = source.fetch()
    except requests.RequestException as err:
        sys.exit(f"Error: Download failed from source API. {err}")

    if not records:
        sys.exit("Error: No valid records retrieved.")

    reporter = ReportBuilder(records)
    summary = reporter.write(OUTPUT_PATH)

    print(f"Read {len(records)} weather records from source API.")
    print(
        f"Hottest day was {summary['hottest_day']} with a high of "
        f"{summary['hottest_day_max_temp_c']}°C."
    )
    print(f"Summary written to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()