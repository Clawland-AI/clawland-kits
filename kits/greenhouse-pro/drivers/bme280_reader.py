class BME280Reader:
    def __init__(self, sensor):
        self.sensor = sensor

    def read(self):
        temperature, pressure, humidity = self.sensor.read_compensated_data()
        return {
            "air_temperature_c": round(temperature / 100, 2),
            "pressure_hpa": round(pressure / 25600, 2),
            "relative_humidity_pct": round(humidity / 1024, 2),
        }

