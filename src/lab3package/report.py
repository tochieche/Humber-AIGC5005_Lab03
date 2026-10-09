import json
from .config import SOURCE_URL, OUTPUT_PATH
from .aggregations import (
    DailyTemperatureAggregation,
    ConditionCountAggregation,
    RecentReadingsAggregation,
)

class ReportBuilder:
    # Builds the complete summary dictionary and writes it to JSON.

    def __init__(self, records):
        self.records = records

    def build(self):
        # Polymorphic execution across aggregation objects
        daily_stats = DailyTemperatureAggregation().compute(self.records)
        condition_counts = ConditionCountAggregation().compute(self.records)
        recent_readings = RecentReadingsAggregation(count=5).compute(self.records)

        hottest_day = max(
            daily_stats, key=lambda d: daily_stats[d]["max_temp_c"]
        )

        return {
            "source_url": SOURCE_URL,
            "records_processed": len(self.records),
            "hottest_day": hottest_day,
            "hottest_day_max_temp_c": daily_stats[hottest_day]["max_temp_c"],
            "daily_breakdown": daily_stats,
            "condition_counts": condition_counts,
            "recent_readings": recent_readings,
        }

    def write(self, path=OUTPUT_PATH):
        summary = self.build()
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(summary, f, indent=2)
        return summary