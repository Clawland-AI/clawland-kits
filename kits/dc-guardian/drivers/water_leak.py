#!/usr/bin/env python3
"""
DC Guardian — Water Leak Detection Sensor Driver
For LicheeRV-Nano (Allwinner R528) GPIO

Simple two-probe water detection with debounce logic to prevent false alarms.

Usage:
    from drivers.water_leak import WaterLeakSensor

    sensor = WaterLeakSensor(pin="PD10", name="floor", location="Under rack row A")
    reading = sensor.read()
    print(f"Water detected: {reading.water_detected}")
"""

import time
import logging
from dataclasses import dataclass
from typing import Optional
from collections import deque

logger = logging.getLogger("dc_guardian.water_leak")


@dataclass
class WaterLeakReading:
    """Single reading from a water leak sensor."""
    water_detected: bool     # True if water is present
    raw_state: bool          # Raw GPIO state (before debounce)
    pin: str                 # GPIO pin identifier
    name: str                # Sensor role (e.g., "floor", "cooling_unit")
    confidence: float        # 0.0-1.0 confidence in detection
    timestamp: float         # Unix timestamp

    def to_dict(self) -> dict:
        return {
            "water_detected": self.water_detected,
            "raw_state": self.raw_state,
            "pin": self.pin,
            "name": self.name,
            "confidence": round(self.confidence, 2),
            "timestamp": self.timestamp,
        }


class WaterLeakSensor:
    """
    Driver for two-probe water leak detection sensor.

    The sensor consists of two exposed conductive probes. When water
    bridges the probes, the circuit completes and the GPIO reads HIGH.

    A 10kΩ pull-down resistor ensures the pin reads LOW when dry.

    Features:
    - Configurable debounce (prevents false positives from splashes)
    - Confidence scoring based on consistent readings
    - Alert cooldown to prevent alarm flooding
    """

    # Debounce settings
    DEBOUNCE_READINGS = 3      # Number of consistent readings required
    DEBOUNCE_INTERVAL = 0.5    # Seconds between debounce reads
    ALERT_COOLDOWN = 60        # Seconds between repeated alerts

    def __init__(self, pin: str, name: str = "water_leak",
                 location: str = "", pull_down: bool = True):
        """
        Initialize water leak sensor.

        Args:
            pin: GPIO pin identifier (e.g., "PD10")
            name: Sensor role name (e.g., "floor", "cooling_unit")
            location: Human-readable location description
            pull_down: True if using pull-down resistor (HIGH = water)
        """
        self.pin = pin
        self.name = name
        self.location = location
        self.pull_down = pull_down  # True = HIGH means water detected

        # State tracking
        self._state_history = deque(maxlen=10)
        self._current_alarm = False
        self._last_alert_time = 0.0
        self._last_reading: Optional[WaterLeakReading] = None
        self._detection_start: Optional[float] = None

        logger.info(f"Water leak sensor '{name}' initialized on pin {pin} "
                    f"at {location or 'unspecified location'}")

    def _read_gpio(self) -> bool:
        """
        Read the raw GPIO state of the water sensor.

        Returns:
            True if water is detected (pin HIGH with pull-down)
        """
        try:
            import gpiod
            chip = gpiod.Chip("0")
            port = ord(self.pin[1]) - ord('A')
            pin_num = int(self.pin[2:])
            line = chip.get_line(port * 32 + pin_num)
            line.request(consumer="dc_guardian_water", type=gpiod.LINE_REQ_DIR_IN)
            value = line.get_value()
            line.release()

            # With pull-down: HIGH = water, LOW = dry
            # With pull-up: LOW = water, HIGH = dry
            return bool(value) if self.pull_down else not bool(value)

        except ImportError:
            # Mock mode for testing
            import random
            return random.random() < 0.02  # 2% chance of water detection

        except Exception as e:
            logger.error(f"Water sensor '{self.name}' GPIO read error: {e}")
            return False

    def _debounce_read(self) -> bool:
        """
        Read with debounce logic.

        Takes multiple readings and only returns True if all readings
        are consistent. This prevents false positives from electrical
        noise or brief splashes.

        Returns:
            Debounced water detection state
        """
        readings = []
        for _ in range(self.DEBOUNCE_READINGS):
            readings.append(self._read_gpio())
            time.sleep(self.DEBOUNCE_INTERVAL)

        # All readings must agree for a positive detection
        if all(readings):
            return True
        elif not any(readings):
            return False
        else:
            # Mixed readings — likely noise
            logger.debug(f"Water sensor '{self.name}': mixed readings {readings}")
            return sum(readings) >= len(readings) * 0.8  # 80% threshold

    def _calculate_confidence(self) -> float:
        """
        Calculate confidence score based on reading history.

        More consistent readings = higher confidence.

        Returns:
            Confidence score from 0.0 to 1.0
        """
        if len(self._state_history) < 3:
            return 0.5  # Insufficient data

        recent = list(self._state_history)[-5:]
        if all(recent):
            return 1.0  # Consistently detecting water
        elif not any(recent):
            return 1.0  # Consistently dry
        else:
            # Mixed — lower confidence
            water_ratio = sum(recent) / len(recent)
            return 0.5 + abs(water_ratio - 0.5)  # Higher when one dominates

    def _should_alert(self) -> bool:
        """Check if we should send an alert (respects cooldown)."""
        if not self._current_alarm:
            return False

        now = time.time()
        if now - self._last_alert_time >= self.ALERT_COOLDOWN:
            self._last_alert_time = now
            return True
        return False

    def read(self) -> WaterLeakReading:
        """
        Read the water leak sensor with debounce.

        Returns:
            WaterLeakReading with detection status and confidence
        """
        # Perform debounced read
        water_detected = self._debounce_read()
        raw_state = self._read_gpio()

        # Update state history
        self._state_history.append(water_detected)

        # Track detection duration
        if water_detected:
            if self._detection_start is None:
                self._detection_start = time.time()
                logger.warning(f"WATER DETECTED by '{self.name}' at {self.location}")
        else:
            if self._detection_start is not None:
                duration = time.time() - self._detection_start
                logger.info(f"Water cleared for '{self.name}' after {duration:.0f}s")
                self._detection_start = None

        # Update alarm state
        self._current_alarm = water_detected

        # Calculate confidence
        confidence = self._calculate_confidence()

        reading = WaterLeakReading(
            water_detected=water_detected,
            raw_state=raw_state,
            pin=self.pin,
            name=self.name,
            confidence=confidence,
            timestamp=time.time(),
        )

        self._last_reading = reading

        # Log alert if warranted
        if self._should_alert():
            duration = time.time() - (self._detection_start or time.time())
            logger.critical(f"⚠️ WATER LEAK ALERT: '{self.name}' at {self.location} "
                           f"(conf={confidence:.0%}, duration={duration:.0f}s)")

        return reading

    def get_status(self) -> dict:
        """Get current sensor status summary."""
        return {
            "name": self.name,
            "pin": self.pin,
            "location": self.location,
            "water_detected": self._current_alarm,
            "detection_duration": (
                time.time() - self._detection_start
                if self._detection_start else 0
            ),
            "confidence": self._calculate_confidence(),
            "readings_count": len(self._state_history),
        }


class FloodMonitor:
    """
    Monitors multiple water leak sensors for comprehensive flood detection.

    Provides aggregated status and can detect patterns like:
    - Single point leak (one sensor triggered)
    - Widespread flooding (multiple sensors triggered)
    - Progressive flooding (sensors triggering sequentially)
    """

    def __init__(self, sensors: list[WaterLeakSensor]):
        self.sensors = sensors
        self._alert_history = []

    def read_all(self) -> dict:
        """
        Read all water sensors and return aggregated status.

        Returns:
            Dict with individual readings and overall flood status
        """
        readings = {}
        triggered = []

        for sensor in self.sensors:
            reading = sensor.read()
            readings[sensor.name] = reading.to_dict()
            if reading.water_detected:
                triggered.append(sensor.name)

        # Determine flood severity
        if len(triggered) == 0:
            severity = "none"
        elif len(triggered) == 1:
            severity = "warning"  # Single point leak
        elif len(triggered) <= len(self.sensors) // 2:
            severity = "critical"  # Multiple points
        else:
            severity = "emergency"  # Widespread flooding

        return {
            "timestamp": time.time(),
            "sensors": readings,
            "triggered_count": len(triggered),
            "total_sensors": len(self.sensors),
            "triggered_locations": triggered,
            "severity": severity,
            "is_flood": len(triggered) > 0,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    # Create sensors for DC Guardian
    sensors = [
        WaterLeakSensor(
            pin="PD10",
            name="floor",
            location="Under rack row A, near CRAC unit"
        ),
        WaterLeakSensor(
            pin="PD8",
            name="cooling_unit",
            location="Under CRAH unit #2, drip tray"
        ),
    ]

    monitor = FloodMonitor(sensors)

    print("DC Guardian — Water Leak Monitor")
    print("=" * 50)
    print("Monitoring for water leaks... (Ctrl+C to stop)\n")

    try:
        while True:
            status = monitor.read_all()

            if status["is_flood"]:
                print(f"⚠️  FLOOD DETECTED! Severity: {status['severity']}")
                for loc in status["triggered_locations"]:
                    print(f"   → {loc}")
            else:
                print(f"✓ All clear ({status['total_sensors']} sensors active)")

            time.sleep(5)

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")
