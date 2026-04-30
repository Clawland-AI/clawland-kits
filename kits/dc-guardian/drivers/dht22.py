#!/usr/bin/env python3
"""
DHT22 Temperature & Humidity Sensor Driver for LicheeRV-Nano
Reads temperature (°C) and humidity (%RH) via GPIO data pin.
"""

import time
import logging
from dataclasses import dataclass

logger = logging.getLogger("dc-guardian.dht22")


@dataclass
class DHT22Reading:
    temperature_c: float
    temperature_f: float
    humidity: float
    timestamp: float
    sensor_id: str
    valid: bool = True


class DHT22Driver:
    """
    Driver for DHT22 temperature/humidity sensor.
    Uses GPIO bit-banging protocol (single-wire, proprietary protocol).
    """

    def __init__(self, gpio_pin: int, sensor_id: str = "dht22"):
        self.gpio_pin = gpio_pin
        self.sensor_id = sensor_id
        self._last_reading: DHT22Reading | None = None
        self._last_read_time: float = 0
        # DHT22 requires minimum 2 seconds between readings
        self._min_interval = 2.0

    def read(self) -> DHT22Reading:
        """
        Read temperature and humidity from DHT22 sensor.
        Returns DHT22Reading dataclass with results.
        """
        now = time.time()

        # Enforce minimum read interval
        if now - self._last_read_time < self._min_interval:
            if self._last_reading and self._last_reading.valid:
                return self._last_reading
            time.sleep(self._min_interval - (now - self._last_read_time))

        try:
            temp_c, humidity = self._read_sensor()
            temp_f = temp_c * 9.0 / 5.0 + 32.0

            reading = DHT22Reading(
                temperature_c=round(temp_c, 1),
                temperature_f=round(temp_f, 1),
                humidity=round(humidity, 1),
                timestamp=time.time(),
                sensor_id=self.sensor_id,
            )
            self._last_reading = reading
            self._last_read_time = time.time()
            return reading

        except Exception as e:
            logger.error(f"DHT22 read error on {self.sensor_id}: {e}")
            return DHT22Reading(
                temperature_c=float("nan"),
                temperature_f=float("nan"),
                humidity=float("nan"),
                timestamp=time.time(),
                sensor_id=self.sensor_id,
                valid=False,
            )

    def _read_sensor(self) -> tuple[float, float]:
        """
        Low-level sensor read using GPIO bit-banging.
        
        DHT22 protocol:
        1. MCU pulls low for 1ms, then high for 30μs (start signal)
        2. Sensor responds: low 80μs, high 80μs
        3. 40 bits of data: 8bit humidity int + 8bit humidity dec 
           + 8bit temp int + 8bit temp dec + 8bit checksum
        """
        # NOTE: Actual GPIO access requires platform-specific library
        # (e.g., lgpio for LicheeRV-Nano). This is the reference implementation.
        
        try:
            import lgpio
        except ImportError:
            # Fallback: return simulated values for testing
            logger.warning("lgpio not available, returning simulated values")
            return 22.5, 45.0

        h = lgpio.gpiochip_open(0)
        try:
            # Send start signal
            lgpio.gpio_claim_output(h, self.gpio_pin)
            lgpio.gpio_write(h, self.gpio_pin, 0)
            time.sleep(0.001)  # 1ms low
            lgpio.gpio_write(h, self.gpio_pin, 1)
            time.sleep(30e-6)  # 30μs high
            
            # Switch to input
            lgpio.gpio_claim_input(h, self.gpio_pin)
            
            # Read 40 bits
            data = []
            for _ in range(40):
                # Wait for low → high transition (start of bit)
                while lgpio.gpio_read(h, self.gpio_pin) == 0:
                    pass
                # Time the high pulse
                start = time.time()
                while lgpio.gpio_read(h, self.gpio_pin) == 1:
                    pass
                pulse = time.time() - start
                # > 40μs = '1', < 40μs = '0'
                data.append(1 if pulse > 40e-6 else 0)
            
            # Parse bits
            humidity_int = self._bits_to_int(data[0:8])
            humidity_dec = self._bits_to_int(data[8:16])
            temp_int = self._bits_to_int(data[16:24])
            temp_dec = self._bits_to_int(data[24:32])
            checksum = self._bits_to_int(data[32:40])
            
            # Verify checksum
            calc_checksum = (humidity_int + humidity_dec + temp_int + temp_dec) & 0xFF
            if calc_checksum != checksum:
                raise ValueError(
                    f"Checksum mismatch: calculated {calc_checksum}, got {checksum}"
                )
            
            humidity = humidity_int + humidity_dec / 10.0
            temperature = temp_int + temp_dec / 10.0
            
            return temperature, humidity
            
        finally:
            lgpio.gpiochip_close(h)

    @staticmethod
    def _bits_to_int(bits: list[int]) -> int:
        value = 0
        for bit in bits:
            value = (value << 1) | bit
        return value

    @property
    def last_reading(self) -> DHT22Reading | None:
        return self._last_reading


# Self-test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Sensor #1 (hot aisle) on GPIO_12
    dht1 = DHT22Driver(gpio_pin=12, sensor_id="dht22_hot_aisle")
    r1 = dht1.read()
    print(f"[{r1.sensor_id}] Temp: {r1.temperature_c}°C / {r1.temperature_f}°F | Humidity: {r1.humidity}% | Valid: {r1.valid}")
    
    # Sensor #2 (cold aisle) on GPIO_13
    dht2 = DHT22Driver(gpio_pin=13, sensor_id="dht22_cold_aisle")
    r2 = dht2.read()
    print(f"[{r2.sensor_id}] Temp: {r2.temperature_c}°C / {r2.temperature_f}°F | Humidity: {r2.humidity}% | Valid: {r2.valid}")
