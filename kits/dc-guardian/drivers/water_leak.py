#!/usr/bin/env python3
"""
Water Leak Sensor Driver for LicheeRV-Nano
Detects water presence via digital output from conductive probe.
"""

import time
import logging
from dataclasses import dataclass

logger = logging.getLogger("dc-guardian.water_leak")


@dataclass
class WaterLeakReading:
    """Water leak sensor reading."""
    water_detected: bool      # True if water is detected
    raw_value: int            # Raw GPIO value (0 or 1)
    sensor_id: str
    timestamp: float
    alert: bool = False       # True if water detected
    valid: bool = True


class WaterLeakDriver:
    """
    Driver for water leak detection sensor module.
    Uses digital output (HIGH = wet, LOW = dry, or vice versa depending on module).
    """

    # Most common modules output LOW when wet (conductive path to ground)
    WET_STATE = 0  # GPIO reads 0 when water detected

    def __init__(
        self,
        gpio_pin: int,
        sensor_id: str = "water_leak",
        wet_state: int = WET_STATE,
        debounce_seconds: float = 0.5,
    ):
        """
        Args:
            gpio_pin: GPIO pin number for digital input
            sensor_id: Human-readable sensor identifier
            wet_state: GPIO value when water is detected (0 or 1)
            debounce_seconds: Minimum time between state changes
        """
        self.gpio_pin = gpio_pin
        self.sensor_id = sensor_id
        self.wet_state = wet_state
        self.debounce_seconds = debounce_seconds
        self._last_state_change: float = 0
        self._last_reading: WaterLeakReading | None = None

    def read(self) -> WaterLeakReading:
        """Read water leak sensor state."""
        try:
            raw = self._read_gpio()
            water_detected = (raw == self.wet_state)
            
            # Debounce: only change alert state after debounce period
            now = time.time()
            if (self._last_reading is None or 
                water_detected != self._last_reading.water_detected):
                if now - self._last_state_change >= self.debounce_seconds:
                    self._last_state_change = now
                else:
                    # Keep previous state during debounce
                    water_detected = self._last_reading.water_detected if self._last_reading else False
            
            reading = WaterLeakReading(
                water_detected=water_detected,
                raw_value=raw,
                sensor_id=self.sensor_id,
                timestamp=now,
                alert=water_detected,
            )
            self._last_reading = reading
            return reading
            
        except Exception as e:
            logger.error(f"Water leak read error on {self.sensor_id}: {e}")
            return WaterLeakReading(
                water_detected=False,
                raw_value=-1,
                sensor_id=self.sensor_id,
                timestamp=time.time(),
                valid=False,
            )

    def _read_gpio(self) -> int:
        """Read digital GPIO value."""
        try:
            import lgpio
            h = lgpio.gpiochip_open(0)
            try:
                lgpio.gpio_claim_input(h, self.gpio_pin)
                return lgpio.gpio_read(h, self.gpio_pin)
            finally:
                lgpio.gpiochip_close(h)
        except ImportError:
            # Simulated: dry (no water)
            return 1 if self.wet_state == 0 else 0

    @property
    def last_reading(self) -> WaterLeakReading | None:
        return self._last_reading


# Self-test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Sensor #1 (under raised floor) on GPIO_16
    wl1 = WaterLeakDriver(gpio_pin=16, sensor_id="water_raised_floor")
    r1 = wl1.read()
    status = "💧 WATER DETECTED!" if r1.water_detected else "✅ Dry"
    print(f"[{r1.sensor_id}] {status} | Raw: {r1.raw_value} | Alert: {r1.alert}")
    
    # Sensor #2 (near cooling pipes) on GPIO_17
    wl2 = WaterLeakDriver(gpio_pin=17, sensor_id="water_cooling_pipes")
    r2 = wl2.read()
    status = "💧 WATER DETECTED!" if r2.water_detected else "✅ Dry"
    print(f"[{r2.sensor_id}] {status} | Raw: {r2.raw_value} | Alert: {r2.alert}")
