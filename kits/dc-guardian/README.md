# DC Guardian

DC Guardian is the data center night shift monitoring kit from Clawland Kits. It watches rack aisle temperature, humidity, smoke/gas trend, and floor water leaks, then sends PicClaw alerts before a human operator would normally find the issue on patrol.

Target replacement: one $48,000/yr overnight operator watch loop.

Target hardware budget: about $88 before tax and shipping.

## What It Monitors

| Risk | Sensor | Default action |
|------|--------|----------------|
| Hot aisle excursion | DHT22/AM2302 temperature | Warn at 30 C, critical at 35 C |
| Humidity drift | DHT22/AM2302 humidity | Warn below 25% or above 60%, critical above 70% |
| Smoke or abnormal gas trend | Grove MQ-2 smoke/gas sensor | Warn after 90 seconds above baseline, critical after 30 seconds at high threshold |
| Condensate or pipe leak | Digital water leak sensor | Critical immediately |
| Kit offline | PicClaw heartbeat | Critical after 120 seconds without readings |

## Files

- [BOM.md](BOM.md) - purchase links and cost breakdown.
- [WIRING.md](WIRING.md) - ASCII wiring diagram, pin map, and electrical notes.
- [ASSEMBLY.md](ASSEMBLY.md) - build steps with photo references.
- [skill.yaml](skill.yaml) - PicClaw/PicoClaw skill configuration.
- [alerts.yaml](alerts.yaml) - scenario thresholds and escalation policy.

## Placement

Mount the LicheeRV-Nano-WE in a small ventilated case on the side of a rack, 1.2 m to 1.5 m above the floor. Place the DHT22 in the hot aisle airflow, keep the MQ-2 exposed but away from direct fan blast, and mount the water sensor at the lowest point under the rack or condensate line.

Use Ethernet for the primary network path. Keep WiFi enabled only as a backup path if the site policy allows it.

## Verification Notes

- Confirm the kit boots and appears in PicClaw as `dc-guardian-night-shift`.
- Confirm a DHT22 reading arrives at least once every 10 seconds.
- Confirm the ADS1115 is visible at I2C address `0x48`.
- Confirm touching the water sensor with a damp cloth produces a critical `water_leak` event.
- Confirm MQ-2 baseline calibration completes only after the sensor has warmed for at least 10 minutes.
