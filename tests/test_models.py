import unittest
from lab3package.models import HourlyRecord
from lab3package.aggregations import (
    DailyTemperatureAggregation,
    ConditionCountAggregation,
)


class TestHourlyRecord(unittest.TestCase):
    # Test cases for HourlyRecord data cleaning and validation.

    def test_valid_record_creation(self):
        # Test that a valid record initializes correctly with correct types.
        record = HourlyRecord("2026-10-01T12:00", 22.5, 0.0)
        self.assertEqual(record.timestamp, "2026-10-01T12:00")
        self.assertEqual(record.temperature, 22.5)
        self.assertEqual(record.precipitation, 0.0)

    def test_invalid_temperature_raises_error(self):
        # Test that malformed non-numeric values raise a ValueError during creation.
        with self.assertRaises(ValueError):
            HourlyRecord("2026-10-01T12:00", "not-a-number", 0.0)

    def test_string_representation(self):
        # Test that the __str__ method formats correctly.
        record = HourlyRecord("2026-10-01T14:00", 18.0, 0.5)
        self.assertIn("18.0°C", str(record))
        self.assertIn("0.5mm", str(record))


class TestAggregationsWithHandmadeRecords(unittest.TestCase):
    # Test aggregations using hand-made records and no network dependency.

    def setUp(self):
        # Create a list of hand-made HourlyRecord objects for testing.
        self.handmade_records = [
            HourlyRecord("2026-10-01T08:00", -2.5, 0.0),   # Freezing Dry
            HourlyRecord("2026-10-01T12:00", 10.0, 1.2),   # Precipitation
            HourlyRecord("2026-10-02T12:00", 25.0, 0.0),   # Warm Dry
        ]

    def test_daily_temperature_aggregation(self):
        # Test that DailyTemperatureAggregation computes correct min/max/avg.
        agg = DailyTemperatureAggregation()
        result = agg.compute(self.handmade_records)

        # Verify date keys exist
        self.assertIn("2026-10-01", result)
        self.assertIn("2026-10-02", result)

        # Check calculated metrics for 2026-10-01 (-2.5 and 10.0)
        self.assertEqual(result["2026-10-01"]["min_temp_c"], -2.5)
        self.assertEqual(result["2026-10-01"]["max_temp_c"], 10.0)
        self.assertEqual(result["2026-10-01"]["total_precip_mm"], 1.2)

    def test_condition_count_aggregation(self):
        # Test that ConditionCountAggregation counts categories properly.
        agg = ConditionCountAggregation()
        result = agg.compute(self.handmade_records)

        # Expecting 1 Freezing Dry, 1 Precipitation, 1 Warm Dry
        self.assertEqual(result.get("Freezing Dry", 0), 1)
        self.assertEqual(result.get("Precipitation", 0), 1)
        self.assertEqual(result.get("Warm Dry", 0), 1)


if __name__ == "__main__":
    unittest.main()