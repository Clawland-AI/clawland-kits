class SCD41Reader:
    def __init__(self, sensor):
        self.sensor = sensor

    def read(self):
        co2, temperature, humidity = self.sensor.measure()
        return {
            "co2_ppm": int(co2),
            "co2_temperature_c": round(float(temperature), 2),
            "co2_humidity_pct": round(float(humidity), 2),
        }

