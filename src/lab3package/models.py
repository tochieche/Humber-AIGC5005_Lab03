class HourlyRecord:
    #Represents a single hourly weather record with validation and cleaning.

    def __init__(self, timestamp, temperature, precipitation):
        if timestamp is None:
            raise ValueError("Timestamp cannot be None.")
        if temperature is None or precipitation is None:
            raise ValueError("Temperature and precipitation cannot be None.")
        
        try:
            self.timestamp = str(timestamp)
            self.temperature = float(temperature)
            self.precipitation = float(precipitation)
        except (ValueError, TypeError) as e:
            raise ValueError(f"Invalid malformed data types: {e}")

    def __str__(self):
        #Returns a clean string representation of the record.
        return (
            f"HourlyRecord(time={self.timestamp}, "
            f"temp={self.temperature}°C, precip={self.precipitation}mm)"
        )