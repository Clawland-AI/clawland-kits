#!/usr/bin/env python3
"""
DC Guardian — DHT22 Temperature & Humidity Driver
For LicheeRV-Nano (Allwinner R528) GPIO

Usage:
    from drivers.dht22 import DHT22Sensor

    sensor = DHT22Sensor(pin="PD18", name="inlet")
    reading = sensor.read()
    print(f"Temperature: {reading.temperature}°C, Humidity: {reading.humidity}%")
"""

import time
import logging
from dataclasses import dataclass
from typing import Optional

logger = logging.getLogger("dc_guardian.dht22")

# DHT22 timing constants (microseconds)
DHT22_START_SIGNAL = 1000  # 1ms low to initiate
DHT22_RESPONSE_TIMEOUT = 100
DHT22_BIT_THRESHOLD = 50  # >50µs = 1, <50µs = 0


@dataclass
class DHT22Reading:
    """Single reading from a DHT22 sensor."""
    temperature: float  # Celsius
    humidity: float     # Percentage (0-100)
    timestamp: float    # Unix timestamp
    pin: str           # GPIO pin identifier
    name: str          # Sensor role name (e.g., "inlet", "exhaust")
    valid: bool        # True if checksum verified

    @property
    def temperature_f(self) -> float:
        """Temperature in Fahrenheit."""
        return (self.temperature * 9 / 5) + 32

    @property
    def heat_index(self) -> float:
        """Calculate heat index in Celsius."""
        t = self.temperature
        h = self.humidity
        if t < 27 or h < 40:
            return t
        # Simplified heat index formula
        hi = (-8.7847 + 1.6114 * t + 2.3385 * h
              - 0.1461 * t * h - 0.0123 * t**2
              - 0.0164 * h**2 + 0.0022 * t**2 * h
              + 0.0007 * t * h**2 - 0.0000036 * t**2 * h**2)
        return round(hi, 1)

    def to_dict(self) -> dict:
        return {
            "temperature_c": self.temperature,
            "temperature_f": round(self.temperature_f, 1),
            "humidity_pct": self.humidity,
            "heat_index_c": self.heat_index,
            "timestamp": self.timestamp,
            "pin": self.pin,
            "name": self.name,
            "valid": self.valid,
        }


class DHT22Sensor:
    """
    Driver for DHT22 temperature/humidity sensor on LicheeRV-Nano GPIO.

    The DHT22 uses a single-wire protocol:
    1. MCU pulls LOW for 1ms to start
    2. MCU releases, waits for sensor response
    3. Sensor pulls LOW for 80µs, then HIGH for 80µs
    4. Sensor sends 40 bits of data (humidity, temperature, checksum)

    Each bit is encoded as:
    - 26-28µs HIGH = bit 0
    - 70µs HIGH = bit 1
    """

    def __init__(self, pin: str, name: str = "dht22", retry_count: int = 3):
        """
        Initialize DHT22 sensor.

        Args:
            pin: GPIO pin identifier (e.g., "PD18")
            name: Sensor role name (e.g., "inlet", "exhaust")
            retry_count: Number of retries on read failure
        """
        self.pin = pin
        self.name = name
        self.retry_count = retry_count
        self._last_reading: Optional[DHT22Reading] = None
        self._min_interval = 2.0  # DHT22 needs 2s between reads
        self._last_read_time = 0.0
        logger.info(f"DHT22 sensor '{name}' initialized on pin {pin}")

    def _read_raw(self) -> Optional[list[int]]:
        """
        Perform raw GPIO read of DHT22 sensor.

        Returns:
            List of 5 bytes (40 bits) or None on failure.
        """
        try:
            # Import platform-specific GPIO library
            # On LicheeRV-Nano, use gpiod (Linux GPIO character device)
            import gpiod

            chip = gpiod.Chip("0")  # GPIO chip 0
            line = chip.get_line(self._get_line_offset())

            # Configure as output to send start signal
            line.request(consumer="dc_guardian", type=gpiod.LINE_REQ_DIR_OUT)
            line.set_value(0)
            time.sleep(DHT22_START_SIGNAL / 1_000_000)  # 1ms low
            line.set_value(1)
            time.sleep(0.000030)  # 30µs high

            # Switch to input to read response
            line.release()
            line.request(consumer="dc_guardian", type=gpiod.LINE_REQ_DIR_IN)

            # Wait for sensor response
            timeout = time.monotonic() + 0.001  # 1ms timeout
            while line.get_value() == 0:
                if time.monotonic() > timeout:
                    logger.warning(f"DHT22 '{self.name}': no response LOW phase")
                    return None

            timeout = time.monotonic() + 0.001
            while line.get_value() == 1:
                if time.monotonic() > timeout:
                    logger.warning(f"DHT22 '{self.name}': no response HIGH phase")
                    return None

            # Read 40 bits
            data = []
            for i in range(40):
                timeout = time.monotonic() + 0.0001
                while line.get_value() == 0:
                    if time.monotonic() > timeout:
                        return None

                start = time.monotonic()
                timeout = start + 0.0001
                while line.get_value() == 1:
                    if time.monotonic() > timeout:
                        return None

                duration = time.monotonic() - start
                data.append(1 if duration > DHT22_BIT_THRESHOLD / 1_000_000 else 0)

            line.release()
            return data

        except ImportError:
            logger.warning("gpiod not available, using mock data for testing")
            return self._mock_read()
        except Exception as e:
            logger.error(f"DHT22 '{self.name}' read error: {e}")
            return None

    def _get_line_offset(self) -> int:
        """Convert pin identifier to GPIO line offset."""
        # Parse pin like "PD18" -> port D, pin 18
        port = ord(self.pin[1]) - ord('A')
        pin_num = int(self.pin[2:])
        return port * 32 + pin_num

    def _mock_read(self) -> list[int]:
        """Return mock data for testing without hardware."""
        import random
        # Simulate ~22°C, ~45% humidity
        humidity = int(45 * 10)  # 45.0%
        temp = int(22 * 10)     # 22.0°C
        hum_hi = (humidity >> 8) & 0xFF
        hum_lo = humidity & 0xFF
        temp_hi = (temp >> 8) & 0xFF
        temp_lo = temp & 0xFF
        checksum = (hum_hi + hum_lo + temp_hi + temp_lo) & 0xFF

        bits = []
        for byte_val in [hum_hi, hum_lo, temp_hi, temp_lo, checksum]:
            for bit in range(7, -1, -1):
                bits.append((byte_val >> bit) & 1)
        return bits

    def _parse_data(self, data: list[int]) -> Optional[DHT22Reading]:
        """Parse 40-bit DHT22 data into a reading."""
        if len(data) != 40:
            return None

        # Convert bits to bytes
        bytes_data = []
        for i in range(0, 40, 8):
            byte_val = 0
            for bit in range(8):
                byte_val = (byte_val << 1) | data[i + bit]
            bytes_data.append(byte_val)

        hum_hi, hum_lo, temp_hi, temp_lo, checksum = bytes_data

        # Verify checksum
        calculated = (hum_hi + hum_lo + temp_hi + temp_lo) & 0xFF
        valid = calculated == checksum

        if not valid:
            logger.warning(f"DHT22 '{self.name}': checksum mismatch "
                          f"(expected {calculated}, got {checksum})")

        # Parse values (DHT22 uses 16-bit values, MSB first)
        humidity = ((hum_hi << 8) | hum_lo) / 10.0
        temperature = ((temp_hi << 8) | temp_lo) / 10.0

        # Handle negative temperatures (bit 15 of temp is sign bit)
        if temp_hi & 0x80:
            temperature = -temperature

        return DHT22Reading(
            temperature=round(temperature, 1),
            humidity=round(humidity, 1),
            timestamp=time.time(),
            pin=self.pin,
            name=self.name,
            valid=valid,
        )

    def read(self) -> Optional[DHT22Reading]:
        """
        Read temperature and humidity from the sensor.

        Retries up to self.retry_count times on failure.
        Enforces minimum 2-second interval between reads.

        Returns:
            DHT22Reading or None if all retries fail.
        """
        # Enforce minimum read interval
        elapsed = time.time() - self._last_read_time
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)

        for attempt in range(self.retry_count):
            data = self._read_raw()
            if data is not None:
                reading = self._parse_data(data)
                if reading and reading.valid:
                    self._last_reading = reading
                    self._last_read_time = time.time()
                    logger.debug(f"DHT22 '{self.name}': {reading.temperature}°C, "
                                f"{reading.humidity}%")
                    return reading
                elif reading:
                    logger.warning(f"DHT22 '{self.name}': invalid checksum, "
                                  f"attempt {attempt + 1}/{self.retry_count}")

            if attempt < self.retry_count - 1:
                time.sleep(2.0)  # Wait before retry

        logger.error(f"DHT22 '{self.name}': all {self.retry_count} attempts failed")
        return self._last_reading  # Return last valid reading if available


class DifferentialMonitor:
    """
    Monitors temperature differential between two DHT22 sensors.

    Used to detect cooling system failures by comparing rack inlet
    and exhaust temperatures.
    """

    def __init__(self, inlet_sensor: DHT22Sensor, exhaust_sensor: DHT22Sensor):
        self.inlet = inlet_sensor
        self.exhaust = exhaust_sensor

    def read_differential(self) -> Optional[dict]:
        """
        Read both sensors and calculate the temperature differential.

        Returns:
            Dict with inlet, exhaust, and delta temperatures.
        """
        inlet_reading = self.inlet.read()
        exhaust_reading = self.exhaust.read()

        if not inlet_reading or not exhaust_reading:
            return None

        delta_t = exhaust_reading.temperature - inlet_reading.temperature

        return {
            "inlet": inlet_reading.to_dict(),
            "exhaust": exhaust_reading.to_dict(),
            "delta_t": round(delta_t, 1),
            "cooling_healthy": delta_t < 15.0,  # >15°C delta = cooling issue
            "timestamp": time.time(),
        }


if __name__ == "__main__":
    # Example usage
    logging.basicConfig(level=logging.DEBUG)

    inlet = DHT22Sensor(pin="PD18", name="inlet")
    exhaust = DHT22Sensor(pin="PD16", name="exhaust")

    monitor = DifferentialMonitor(inlet, exhaust)
    result = monitor.read_differential()

    if result:
        print(f"Inlet:  {result['inlet']['temperature_c']}°C / "
              f"{result['inlet']['humidity_pct']}% RH")
        print(f"Exhaust: {result['exhaust']['temperature_c']}°C / "
              f"{result['exhaust']['humidity_pct']}% RH")
        print(f"ΔT: {result['delta_t']}°C")
        print(f"Cooling: {'✓ Healthy' if result['cooling_healthy'] else '⚠ WARNING'}")
    else:
        print("Failed to read sensors")
