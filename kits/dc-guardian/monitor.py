#!/usr/bin/env python3
"""
DC Guardian — Main Monitoring Loop
Runs on LicheeRV-Nano to continuously monitor data center conditions.
"""

import time
import json
import logging
import signal
import sys
from datetime import datetime
from pathlib import Path

# Add drivers to path
sys.path.insert(0, str(Path(__file__).parent))
from drivers import DHT22Driver, MQ2Driver, WaterLeakDriver

# Configuration
READ_INTERVAL = 30       # seconds between readings
REPORT_INTERVAL = 300    # seconds between full reports
LOG_FILE = "/var/log/dc-guardian/sensor.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("dc-guardian")


class DCGuardian:
    """Main monitoring class for DC Guardian kit."""

    def __init__(self):
        self.running = True

        # Initialize sensors
        self.sensors = {
            "dht22_hot": DHT22Driver(gpio_pin=12, sensor_id="dht22_hot"),
            "dht22_cold": DHT22Driver(gpio_pin=13, sensor_id="dht22_cold"),
            "mq2_crac": MQ2Driver(analog_pin=14, sensor_id="mq2_crac"),
            "mq2_cable": MQ2Driver(analog_pin=15, sensor_id="mq2_cable"),
            "water_floor": WaterLeakDriver(gpio_pin=16, sensor_id="water_floor"),
            "water_pipe": WaterLeakDriver(gpio_pin=17, sensor_id="water_pipe"),
        }

        # Thresholds
        self.thresholds = {
            "temperature_warning": 28.0,
            "temperature_critical": 32.0,
            "humidity_warning": 55.0,
            "humidity_critical": 65.0,
            "lpg_warning": 100.0,
            "lpg_critical": 200.0,
        }

        self.readings = []
        self._setup_signal_handlers()

    def _setup_signal_handlers(self):
        """Handle graceful shutdown."""
        for sig in (signal.SIGINT, signal.SIGTERM):
            signal.signal(sig, self._shutdown)

    def _shutdown(self, signum, frame):
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False

    def read_all(self) -> dict:
        """Read all sensors and return current state."""
        state = {
            "timestamp": datetime.now().isoformat(),
            "sensors": {},
            "alerts": [],
        }

        # DHT22 readings
        for name in ["dht22_hot", "dht22_cold"]:
            reading = self.sensors[name].read()
            state["sensors"][name] = {
                "temperature_c": reading.temperature_c,
                "temperature_f": reading.temperature_f,
                "humidity": reading.humidity,
                "valid": reading.valid,
            }
            # Check thresholds
            if reading.valid:
                if reading.temperature_c > self.thresholds["temperature_critical"]:
                    state["alerts"].append({
                        "sensor": name,
                        "level": "CRITICAL",
                        "metric": "temperature",
                        "value": reading.temperature_c,
                        "message": f"🔥 CRITICAL: {reading.temperature_c}°C exceeds {self.thresholds['temperature_critical']}°C"
                    })
                elif reading.temperature_c > self.thresholds["temperature_warning"]:
                    state["alerts"].append({
                        "sensor": name,
                        "level": "WARNING",
                        "metric": "temperature",
                        "value": reading.temperature_c,
                        "message": f"🌡️ WARNING: {reading.temperature_c}°C exceeds {self.thresholds['temperature_warning']}°C"
                    })

                if reading.humidity > self.thresholds["humidity_critical"]:
                    state["alerts"].append({
                        "sensor": name,
                        "level": "CRITICAL",
                        "metric": "humidity",
                        "value": reading.humidity,
                        "message": f"💧 CRITICAL: Humidity {reading.humidity}% — condensation risk!"
                    })
                elif reading.humidity > self.thresholds["humidity_warning"]:
                    state["alerts"].append({
                        "sensor": name,
                        "level": "WARNING",
                        "metric": "humidity",
                        "value": reading.humidity,
                        "message": f"💧 WARNING: Humidity {reading.humidity}%"
                    })

        # MQ-2 readings
        for name in ["mq2_crac", "mq2_cable"]:
            reading = self.sensors[name].read()
            state["sensors"][name] = {
                "lpg_ppm": reading.lpg_ppm,
                "smoke_ppm": reading.smoke_ppm,
                "raw": reading.raw_value,
                "alert": reading.alert,
                "valid": reading.valid,
            }
            if reading.valid and reading.alert:
                state["alerts"].append({
                    "sensor": name,
                    "level": "CRITICAL",
                    "metric": "smoke",
                    "value": reading.lpg_ppm,
                    "message": f"🔥 SMOKE DETECTED: {reading.lpg_ppm} ppm LPG"
                })

        # Water leak readings
        for name in ["water_floor", "water_pipe"]:
            reading = self.sensors[name].read()
            state["sensors"][name] = {
                "water_detected": reading.water_detected,
                "raw": reading.raw_value,
                "alert": reading.alert,
                "valid": reading.valid,
            }
            if reading.valid and reading.water_detected:
                state["alerts"].append({
                    "sensor": name,
                    "level": "CRITICAL",
                    "metric": "water_leak",
                    "value": True,
                    "message": f"💧 WATER LEAK DETECTED at {name}!"
                })

        return state

    def run(self):
        """Main monitoring loop."""
        logger.info("=" * 50)
        logger.info("DC Guardian starting...")
        logger.info(f"Read interval: {READ_INTERVAL}s")
        logger.info(f"Report interval: {REPORT_INTERVAL}s")
        logger.info("=" * 50)

        last_report = 0
        iteration = 0

        while self.running:
            try:
                state = self.read_all()
                iteration += 1

                # Log alerts immediately
                for alert in state["alerts"]:
                    logger.warning(f"ALERT [{alert['level']}]: {alert['message']}")

                # Periodic full report
                now = time.time()
                if now - last_report >= REPORT_INTERVAL:
                    self._report(state)
                    last_report = now

                # Store reading
                self.readings.append(state)
                if len(self.readings) > 1000:
                    self.readings = self.readings[-500:]

                time.sleep(READ_INTERVAL)

            except Exception as e:
                logger.error(f"Monitoring error: {e}", exc_info=True)
                time.sleep(10)

        logger.info("DC Guardian stopped.")

    def _report(self, state: dict):
        """Log a full status report."""
        logger.info("─" * 40)
        logger.info(f"📊 Status Report — {state['timestamp']}")
        for name, data in state["sensors"].items():
            if "temperature_c" in data:
                logger.info(
                    f"  {name}: {data['temperature_c']}°C / {data.get('humidity', 'N/A')}% RH"
                )
            elif "lpg_ppm" in data:
                logger.info(f"  {name}: LPG {data['lpg_ppm']} ppm, Smoke {data['smoke_ppm']} ppm")
            elif "water_detected" in data:
                status = "💧 WET" if data["water_detected"] else "✅ DRY"
                logger.info(f"  {name}: {status}")

        if state["alerts"]:
            logger.warning(f"  ⚠️ {len(state['alerts'])} active alert(s)")
        else:
            logger.info("  ✅ All clear — no alerts")
        logger.info("─" * 40)


if __name__ == "__main__":
    guardian = DCGuardian()
    guardian.run()
