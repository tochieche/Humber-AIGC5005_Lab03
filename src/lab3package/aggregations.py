from abc import ABC, abstractmethod
from collections import Counter, defaultdict
from typing import Any

class Aggregation(ABC):
    # Base class for all weather aggregations.

    @abstractmethod
    def compute(self, records) -> Any:
        # Compute and return aggregation results.
        pass


class DailyTemperatureAggregation(Aggregation):
    # Computes daily min, max, average temperatures and total precipitation.

    def compute(self, records) -> dict[str, dict[str, float | int]]:
        grouped = defaultdict(list)
        for rec in records:
            date_str = rec.timestamp.split("T")[0]
            grouped[date_str].append(rec)

        return {
            date: {
                "min_temp_c": round(min(r.temperature for r in day_recs), 1),
                "max_temp_c": round(max(r.temperature for r in day_recs), 1),
                "avg_temp_c": round(
                    sum(r.temperature for r in day_recs) / len(day_recs), 1
                ),
                "total_precip_mm": round(sum(r.precipitation for r in day_recs), 1),
                "readings": len(day_recs),
            }
            for date, day_recs in grouped.items()
        }


class ConditionCountAggregation(Aggregation):
    # Classifies hourly readings into weather condition categories and counts frequencies.

    def compute(self, records) -> dict[str, int]:
        conditions = []
        for rec in records:
            if rec.precipitation > 0.0:
                conditions.append("Precipitation")
            elif rec.temperature < 0.0:
                conditions.append("Freezing Dry")
            elif rec.temperature < 15.0:
                conditions.append("Cool Dry")
            else:
                conditions.append("Warm Dry")
        return dict(Counter(conditions))


class RecentReadingsAggregation(Aggregation):
    # Retrieves the recent hourly readings up to a given count.

    def __init__(self, count=5):
        self.count = count

    def compute(self, records) -> list[dict[str, Any]]:
        recent = records[-self.count:] if len(records) >= self.count else records
        return [
            {
                "timestamp": r.timestamp,
                "temperature_c": r.temperature,
                "precipitation_mm": r.precipitation,
            }
            for r in recent
        ]