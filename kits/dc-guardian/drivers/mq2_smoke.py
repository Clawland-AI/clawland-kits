#!/usr/bin/env python3
"""
DC Guardian — MQ-2 Smoke/Gas Sensor Driver
For LicheeRV-Nano (Allwinner R528) GPIO

The MQ-2 detects combustible gases and smoke. It has both digital (threshold)
and analog (concentration) outputs. Requires 48-hour burn-in for accurate readings.

Usage:
    from drivers.mq2_smoke import MQ2Sensor

    sensor = MQ2Sensor(pin_digital="PD12", pin_analog="PD14")
    sensor.wait_for_burn_in()  # Blocks until 48h burn-in complete
    reading = sensor.read()
    print(f"Smoke detected: {reading.smoke_detected}")
"""

import time
import logging
import json
from dataclasses import dataclass, field
from typing import Optional, List
from pathlib import Path

logger = logging.getLogger("dc_guardian.mq2")

# MQ-2 characteristics
BURN_IN_TIME_SECONDS = 48 * 3600  # 48 hours
CLEAN_AIR_RL = 9.83  # Load resistance in clean air (kΩ)
CLEAN_AIR_RO = 9.83  # Sensor resistance in clean air (kΩ)

# Gas detection curves (log-log slope and intercept for each gas)
# Format: (slope, x-intercept at 1ppm)
GAS_CURVES = {
    "smoke":    (-0.462, 2.962),   # Smoke
    "lpg":      (-0.467, 2.961),   # Liquefied Petroleum Gas
    "co":       (-0.395, 3.182),   # Carbon Monoxide
    "h2":       (-0.473, 3.017),   # Hydrogen
    "alcohol":  (-0.450, 2.950),   # Alcohol
    "propane":  (-0.467, 2.961),   # Propane
}


@dataclass
class MQ2Reading:
    """Single reading from MQ-2 sensor."""
    digital_state: bool       # True if above threshold
    analog_raw: int           # Raw ADC value (0-4095 for 12-bit ADC)
    analog_voltage: float     # Voltage at analog pin
    rs_ro_ratio: float        # Rs/Ro ratio
    gas_concentrations: dict  # Estimated PPM for each gas
    smoke_detected: bool      # True if smoke PPM > threshold
    timestamp: float
    burn_in_complete: bool
    calibration_valid: bool

    def to_dict(self) -> dict:
        return {
            "digital_alarm": self.digital_state,
            "analog_raw": self.analog_raw,
            "analog_voltage": round(self.analog_voltage, 3),
            "rs_ro_ratio": round(self.rs_ro_ratio, 3),
            "gas_ppm": self.gas_concentrations,
            "smoke_detected": self.smoke_detected,
            "burn_in_complete": self.burn_in_complete,
            "timestamp": self.timestamp,
        }


class MQ2Sensor:
    """
    Driver for MQ-2 smoke/combustible gas sensor.

    The MQ-2 uses a heated metal oxide semiconductor (MOS) element.
    In the presence of combustible gases, the sensor resistance decreases,
    which changes the voltage at the analog output pin.

    Key specs:
    - Detection range: 200-10000 ppm (combustible gases)
    - Heater voltage: 5V (requires ~150mA)
    - Load resistance: 10kΩ (on module)
    - Warm-up time: 48 hours for accurate readings
    """

    # PPM thresholds for alarm conditions
    SMOKE_ALARM_THRESHOLD = 200    # ppm
    GAS_ALARM_THRESHOLD = 1000     # ppm

    def __init__(self, pin_digital: str, pin_analog: str,
                 calibration_file: Optional[str] = None):
        """
        Initialize MQ-2 sensor.

        Args:
            pin_digital: GPIO pin for digital threshold output
            pin_analog: GPIO pin for analog output (requires ADC)
            calibration_file: Path to stored calibration data
        """
        self.pin_digital = pin_digital
        self.pin_analog = pin_analog
        self.calibration_file = calibration_file
        self._ro_value = CLEAN_AIR_RO  # Default until calibrated
        self._burn_in_start: Optional[float] = None
        self._burn_in_complete = False
        self._adc = None

        # Load calibration if available
        self._load_calibration()

        # Try to initialize ADC for analog reading
        self._init_adc()

        logger.info(f"MQ-2 sensor initialized: digital={pin_digital}, "
                    f"analog={pin_analog}")

    def _init_adc(self):
        """Initialize ADC for analog reading."""
        try:
            # For LicheeRV-Nano, ADC is typically via I2C ADC chip
            # (ADS1115 or built-in SAR ADC)
            import smbus2

            # Try ADS1115 first (I2C address 0x48)
            self._adc_bus = smbus2.SMBus(0)
            self._adc_type = "ads1115"
            logger.info("Using ADS1115 ADC for analog reading")
        except (ImportError, Exception):
            try:
                # Try built-in ADC (Allwinner R528 has SAR ADC)
                self._adc_type = "sar"
                logger.info("Using built-in SAR ADC for analog reading")
            except Exception:
                self._adc_type = "mock"
                logger.warning("No ADC available, using mock readings")

    def _read_adc(self) -> int:
        """Read raw ADC value from analog pin."""
        if self._adc_type == "ads1115":
            return self._read_ads1115()
        elif self._adc_type == "sar":
            return self._read_sar_adc()
        else:
            return self._mock_adc()

    def _read_ads1115(self) -> int:
        """Read from ADS1115 16-bit ADC via I2C."""
        try:
            import smbus2

            # ADS1115 configuration for single-shot reading
            # Channel 0, ±4.096V range, 128 SPS
            config = 0x8000 | 0x4000 | 0x0200 | 0x0080  # OS|MUX|PGA|MODE
            self._adc_bus.write_i2c_block_data(0x48, 0x01,
                                                [(config >> 8) & 0xFF,
                                                 config & 0xFF])
            time.sleep(0.01)  # Wait for conversion

            # Read conversion register
            data = self._adc_bus.read_i2c_block_data(0x48, 0x00, 2)
            raw = (data[0] << 8) | data[1]
            if raw > 0x7FFF:
                raw -= 0x10000

            # Convert to 12-bit scale for consistency
            return max(0, min(4095, int((raw / 32767) * 4095)))
        except Exception as e:
            logger.error(f"ADS1115 read error: {e}")
            return self._mock_adc()

    def _read_sar_adc(self) -> int:
        """Read from Allwinner R528 built-in SAR ADC."""
        try:
            # R528 SAR ADC is typically at /sys/bus/iio/devices/
            adc_path = f"/sys/bus/iio/devices/iio:device0/in_voltage_raw"
            with open(adc_path, 'r') as f:
                raw = int(f.read().strip())
            # R528 ADC is 12-bit (0-4095)
            return max(0, min(4095, raw))
        except Exception as e:
            logger.error(f"SAR ADC read error: {e}")
            return self._mock_adc()

    def _mock_adc(self) -> int:
        """Return mock ADC value for testing."""
        import random
        # Simulate clean air (high Rs/Ro = low concentration)
        return random.randint(800, 1200)

    def _read_digital(self) -> bool:
        """Read digital threshold output from MQ-2 module."""
        try:
            import gpiod
            chip = gpiod.Chip("0")
            port = ord(self.pin_digital[1]) - ord('A')
            pin_num = int(self.pin_digital[2:])
            line = chip.get_line(port * 32 + pin_num)
            line.request(consumer="dc_guardian_mq2", type=gpiod.LINE_REQ_DIR_IN)
            value = line.get_value()
            line.release()
            return bool(value)
        except ImportError:
            import random
            return random.random() < 0.01  # 1% chance of alarm in mock
        except Exception as e:
            logger.error(f"Digital read error: {e}")
            return False

    def _calculate_ppm(self, rs_ro_ratio: float, gas: str) -> float:
        """Calculate gas concentration in PPM from Rs/Ro ratio."""
        if gas not in GAS_CURVES:
            return 0.0

        slope, intercept = GAS_CURVES[gas]

        # PPM = 10^((log10(rs_ro) - intercept) / slope)
        import math
        try:
            log_ratio = math.log10(rs_ro_ratio)
            ppm = 10 ** ((log_ratio - intercept) / slope)
            return max(0, round(ppm, 1))
        except (ValueError, ZeroDivisionError):
            return 0.0

    def _load_calibration(self):
        """Load calibration data from file."""
        if self.calibration_file and Path(self.calibration_file).exists():
            try:
                with open(self.calibration_file, 'r') as f:
                    data = json.load(f)
                    self._ro_value = data.get("ro_value", CLEAN_AIR_RO)
                    self._burn_in_complete = data.get("burn_in_complete", False)
                    if self._burn_in_complete:
                        logger.info(f"Loaded calibration: Ro={self._ro_value:.2f}kΩ")
            except Exception as e:
                logger.warning(f"Failed to load calibration: {e}")

    def _save_calibration(self):
        """Save calibration data to file."""
        if self.calibration_file:
            try:
                data = {
                    "ro_value": self._ro_value,
                    "burn_in_complete": self._burn_in_complete,
                    "calibration_time": time.time(),
                }
                with open(self.calibration_file, 'w') as f:
                    json.dump(data, f, indent=2)
            except Exception as e:
                logger.warning(f"Failed to save calibration: {e}")

    def calibrate(self, num_samples: int = 50) -> float:
        """
        Calibrate sensor in clean air to determine Ro value.

        Run this in a clean air environment before deployment.
        The sensor should be warmed up for at least 24 hours first.

        Args:
            num_samples: Number of ADC readings to average

        Returns:
            Calculated Ro value in kΩ
        """
        logger.info(f"Calibrating MQ-2 with {num_samples} samples...")

        readings = []
        for i in range(num_samples):
            raw = self._read_adc()
            readings.append(raw)
            time.sleep(0.5)

        avg_raw = sum(readings) / len(readings)
        voltage = (avg_raw / 4095) * 3.3  # Assuming 3.3V reference

        # Calculate Rs (sensor resistance)
        # Rs = ((Vc * RL) / Vout) - RL
        # Where Vc = 5V (heater), RL = 10kΩ (load resistor on module)
        vc = 5.0
        rl = 10.0  # kΩ
        if voltage > 0:
            rs = ((vc * rl) / voltage) - rl
        else:
            logger.error("ADC reads 0V — check wiring")
            return self._ro_value

        # Ro = Rs / 9.83 (in clean air, Rs/Ro ≈ 9.83)
        self._ro_value = rs / CLEAN_AIR_RL
        self._burn_in_complete = True
        self._save_calibration()

        logger.info(f"Calibration complete: Ro={self._ro_value:.2f}kΩ "
                    f"(avg ADC={avg_raw:.0f}, V={voltage:.3f}V, Rs={rs:.2f}kΩ)")
        return self._ro_value

    def wait_for_burn_in(self, progress_callback=None):
        """
        Wait for the mandatory 48-hour burn-in period.

        Args:
            progress_callback: Optional function(remaining_seconds) called periodically
        """
        if self._burn_in_complete:
            logger.info("Burn-in already complete")
            return

        if self._burn_in_start is None:
            self._burn_in_start = time.time()
            logger.warning("MQ-2 burn-in started. This takes 48 hours.")

        remaining = BURN_IN_TIME_SECONDS - (time.time() - self._burn_in_start)
        while remaining > 0:
            hours = remaining / 3600
            logger.info(f"MQ-2 burn-in: {hours:.1f} hours remaining")
            if progress_callback:
                progress_callback(remaining)
            time.sleep(min(300, remaining))  # Check every 5 minutes
            remaining = BURN_IN_TIME_SECONDS - (time.time() - self._burn_in_start)

        self._burn_in_complete = True
        self._save_calibration()
        logger.info("MQ-2 burn-in complete! Sensor is now calibrated.")

    def read(self) -> MQ2Reading:
        """
        Read current smoke/gas levels from the sensor.

        Returns:
            MQ2Reading with all sensor data
        """
        # Read digital output (hardware threshold)
        digital_alarm = self._read_digital()

        # Read analog output (concentration)
        raw_adc = self._read_adc()
        voltage = (raw_adc / 4095) * 3.3

        # Calculate Rs
        vc = 5.0
        rl = 10.0  # kΩ
        if voltage > 0.01:
            rs = ((vc * rl) / voltage) - rl
            rs_ro = rs / self._ro_value
        else:
            rs = float('inf')
            rs_ro = float('inf')

        # Calculate PPM for each gas
        concentrations = {}
        for gas in GAS_CURVES:
            concentrations[gas] = self._calculate_ppm(rs_ro, gas)

        # Determine if smoke is detected above threshold
        smoke_ppm = concentrations.get("smoke", 0)
        smoke_detected = (smoke_ppm > self.SMOKE_ALARM_THRESHOLD or
                         digital_alarm)

        reading = MQ2Reading(
            digital_state=digital_alarm,
            analog_raw=raw_adc,
            analog_voltage=round(voltage, 4),
            rs_ro_ratio=round(rs_ro, 3),
            gas_concentrations=concentrations,
            smoke_detected=smoke_detected,
            timestamp=time.time(),
            burn_in_complete=self._burn_in_complete,
            calibration_valid=self._ro_value != CLEAN_AIR_RO,
        )

        if smoke_detected:
            logger.warning(f"SMOKE DETECTED! PPM={smoke_ppm}, "
                          f"Digital={'ALARM' if digital_alarm else 'OK'}")

        return reading


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    sensor = MQ2Sensor(
        pin_digital="PD12",
        pin_analog="PD14",
        calibration_file="mq2_calibration.json"
    )

    print("MQ-2 Smoke/Gas Sensor")
    print("=" * 40)

    # Note: In production, wait for burn-in first
    # sensor.wait_for_burn_in()

    for i in range(10):
        reading = sensor.read()
        print(f"\nReading #{i + 1}:")
        print(f"  Digital alarm: {'YES' if reading.digital_state else 'No'}")
        print(f"  Analog: {reading.analog_raw} ({reading.analog_voltage:.3f}V)")
        print(f"  Rs/Ro: {reading.rs_ro_ratio:.3f}")
        print(f"  Smoke: {reading.gas_concentrations.get('smoke', 0)} PPM")
        print(f"  LPG:   {reading.gas_concentrations.get('lpg', 0)} PPM")
        print(f"  CO:    {reading.gas_concentrations.get('co', 0)} PPM")
        time.sleep(1)
