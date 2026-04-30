#!/usr/bin/env python3
"""
MQ-2 Smoke/Gas Sensor Driver for LicheeRV-Nano
Reads LPG, propane, methane, and smoke levels via analog input.
"""

import time
import logging
import math
from dataclasses import dataclass

logger = logging.getLogger("dc-guardian.mq2")


@dataclass
class MQ2Reading:
    """MQ-2 sensor reading."""
    lpg_ppm: float          # LPG concentration in ppm
    smoke_ppm: float        # Smoke concentration estimate in ppm
    raw_value: int          # Raw ADC value (0-4095 for 12-bit)
    voltage: float          # Voltage at analog pin
    sensor_id: str
    timestamp: float
    alert: bool = False     # True if above threshold
    valid: bool = True


class MQ2Driver:
    """
    Driver for MQ-2 gas/smoke sensor module.
    Reads analog output and converts to ppm estimates.
    """

    # MQ-2 calibration constants (derived from datasheet)
    # RL = 5kΩ (module load resistor), Ro ≈ 10kΩ (in clean air)
    RL_VALUE = 5.0       # Load resistance in kΩ
    RO_CLEAN_AIR = 10.0  # Sensor resistance in clean air (kΩ)
    
    # LPG curve: log(y) = -0.44 * log(x/Ro) + 0.25
    LPG_CURVE = (-0.44, 0.25)
    
    # Default alert thresholds
    DEFAULT_LPG_THRESHOLD = 200.0   # ppm
    DEFAULT_SMOKE_THRESHOLD = 150.0 # ppm

    def __init__(
        self,
        analog_pin: int,
        sensor_id: str = "mq2",
        lpg_threshold: float = DEFAULT_LPG_THRESHOLD,
        smoke_threshold: float = DEFAULT_SMOKE_THRESHOLD,
        adc_resolution: int = 4095,  # 12-bit ADC
        vref: float = 3.3,
    ):
        self.analog_pin = analog_pin
        self.sensor_id = sensor_id
        self.lpg_threshold = lpg_threshold
        self.smoke_threshold = smoke_threshold
        self.adc_resolution = adc_resolution
        self.vref = vref
        self._calibration_value = self.RO_CLEAN_AIR

    def calibrate(self, samples: int = 50) -> float:
        """
        Calibrate Ro value in clean air.
        Run this in a known-clean environment before deployment.
        
        Returns the calibrated Ro value in kΩ.
        """
        logger.info(f"Calibrating {self.sensor_id} with {samples} samples...")
        
        readings = []
        for i in range(samples):
            raw = self._read_adc()
            if raw >= 0:
                readings.append(raw)
            time.sleep(0.1)
        
        if not readings:
            logger.warning("No valid readings during calibration")
            return self._calibration_value
        
        avg_raw = sum(readings) / len(readings)
        voltage = avg_raw * self.vref / self.adc_resolution
        
        # Rs = RL * (Vc - V) / V  where Vc = Vref
        if voltage > 0:
            rs = self.RL_VALUE * (self.vref - voltage) / voltage
        else:
            rs = self.RL_VALUE * 100  # Fallback
        
        self._calibration_value = rs
        logger.info(f"Calibrated Ro = {rs:.2f} kΩ")
        return rs

    def read(self) -> MQ2Reading:
        """Read gas concentration from MQ-2 sensor."""
        try:
            raw = self._read_adc()
            voltage = raw * self.vref / self.adc_resolution if raw >= 0 else 0.0
            
            # Calculate sensor resistance
            if voltage > 0.01:
                rs = self.RL_VALUE * (self.vref - voltage) / voltage
            else:
                rs = float("inf")
            
            # Ratio Rs/Ro
            ratio = rs / self._calibration_value if self._calibration_value > 0 else 1.0
            
            # Convert to ppm using characteristic curves
            lpg_ppm = self._ratio_to_ppm(ratio, self.LPG_CURVE)
            smoke_ppm = lpg_ppm * 0.8  # Approximate smoke from LPG curve
            
            alert = lpg_ppm > self.lpg_threshold or smoke_ppm > self.smoke_threshold
            
            return MQ2Reading(
                lpg_ppm=round(lpg_ppm, 1),
                smoke_ppm=round(smoke_ppm, 1),
                raw_value=raw,
                voltage=round(voltage, 3),
                sensor_id=self.sensor_id,
                timestamp=time.time(),
                alert=alert,
            )
            
        except Exception as e:
            logger.error(f"MQ-2 read error on {self.sensor_id}: {e}")
            return MQ2Reading(
                lpg_ppm=float("nan"),
                smoke_ppm=float("nan"),
                raw_value=-1,
                voltage=0.0,
                sensor_id=self.sensor_id,
                timestamp=time.time(),
                valid=False,
            )

    def _read_adc(self) -> int:
        """Read analog value from ADC pin."""
        try:
            import lgpio
            h = lgpio.gpiochip_open(0)
            try:
                # Read ADC value (platform-specific)
                # For LicheeRV-Nano, use the onboard ADC
                value = lgpio.gpio_read(h, self.analog_pin)
                return value
            finally:
                lgpio.gpiochip_close(h)
        except ImportError:
            # Simulated value for testing
            return 800  # ~clean air reading

    def _ratio_to_ppm(self, ratio: float, curve: tuple) -> float:
        """Convert Rs/Ro ratio to ppm using sensor curve."""
        if ratio <= 0:
            return 0.0
        try:
            slope, intercept = curve
            log_ppm = (math.log10(ratio) - intercept) / slope
            if log_ppm < 0:
                return 0.0
            return 10 ** log_ppm
        except (ValueError, ZeroDivisionError):
            return 0.0


# Self-test
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    # Sensor #1 (near CRAC) on analog pin 14
    mq2_1 = MQ2Driver(analog_pin=14, sensor_id="mq2_crac")
    r1 = mq2_1.read()
    print(f"[{r1.sensor_id}] LPG: {r1.lpg_ppm} ppm | Smoke: {r1.smoke_ppm} ppm | Raw: {r1.raw_value} | Alert: {r1.alert}")
    
    # Sensor #2 (cable tray) on analog pin 15
    mq2_2 = MQ2Driver(analog_pin=15, sensor_id="mq2_cable_tray")
    r2 = mq2_2.read()
    print(f"[{r2.sensor_id}] LPG: {r2.lpg_ppm} ppm | Smoke: {r2.smoke_ppm} ppm | Raw: {r2.raw_value} | Alert: {r2.alert}")
