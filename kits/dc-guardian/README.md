# DC Guardian - Data Center Monitoring Kit

## Overview

The **DC Guardian** kit monitors data center environmental conditions to replace a $48,000/year night shift operator with an $88 hardware solution.

## Use Case

Data centers require 24/7 monitoring for:
- Temperature (overheating detection)
- Humidity (condensation prevention)
- Water leaks (pipeline failures)
- Smoke detection (fire prevention)

This kit provides automated alerts when any threshold is exceeded.

## Bill of Materials (BOM)

| Component | Quantity | Unit Cost | Total | Purchase Link |
|----------|----------|-----------|-------|---------------|
| LicheeRV-Nano (RISC-V board) | 1 | $15 | $15 | [AliExpress](https://s.click.aliexpress.com/e/_DlBh5fh) |
| DHT22 Temperature/Humidity Sensor | 1 | $5 | $5 | [AliExpress](https://s.click.aliexpress.com/e/_DmAF27h) |
| MQ-2 Smoke Sensor | 1 | $3 | $3 | [AliExpress](https://s.click.aliexpress.com/e/_DnCNBHh) |
| Water Leak Sensor | 2 | $2 | $4 | [AliExpress](https://s.click.aliexpress.com/e/_Doe4gXh) |
| Jumper Wires | 10 | $0.5 | $5 | [AliExpress](https://s.click.aliexpress.com/e/_DBbQFLz) |
| 5V Power Supply | 1 | $8 | $8 | [AliExpress](https://s.click.aliexpress.com/e/_DBCdCZh) |
| Case/Enclosure | 1 | $10 | $10 | [AliExpress](https://s.click.aliexpress.com/e/_DdJBtYh) |
| MicroSD Card 8GB | 1 | $8 | $8 | [AliExpress](https://s.click.aliexpress.com/e/_DeHCFLz) |
| **TOTAL** | - | - | **$58** | - |

*Note: Prices are approximate and may vary. Buy extra sensors for redundancy.*

## Wiring Diagram

```
LicheeRV-Nano Pinout:
------------------------
GPIO 18 -> DHT22 Data (Yellow wire)
GPIO 5  -> MQ-2 Analog Output (A0)
GPIO 4  -> Water Leak Sensor 1 (Red wire)
GPIO 15 -> Water Leak Sensor 2 (Red wire)
3.3V   -> DHT22 VCC (Red wire)
3.3V   -> MQ-2 VCC (Red wire)
3.3V   -> Water Leak Sensors VCC (Red wire)
GND    -> All sensors GND (Black wire)

Connections:
[LicheeRV-Nano]     [Sensors]
---------------------------
GPIO 18 ----------> DHT22 Data pin
GPIO 5  ----------> MQ-2 A0 pin
GPIO 4  ----------> Water Leak 1
GPIO 15 ----------> Water Leak 2
3.3V   ----------> VCC (all sensors)
GND     ----------> GND (all sensors)
```

## Assembly Instructions

### Step 1: Prepare the Board
1. Flash PicClaw firmware onto LicheeRV-Nano
2. Insert MicroSD card
3. Connect power supply

### Step 2: Connect Sensors
1. Connect DHT22 to GPIO 18
2. Connect MQ-2 to GPIO 5 (analog)
3. Connect water leak sensors to GPIO 4 and GPIO 15

### Step 3: Enclosure
1. Mount board in enclosure
2. Drill holes for sensor cables
3. Place water leak sensors in potential leak areas

### Step 4: Configure
1. Edit `skill.yaml` with WiFi credentials
2. Set alert thresholds
3. Test all sensors

## PicClaw Configuration

```yaml
# skill.yaml
name: dc-guardian
version: 1.0.0
description: Data center environmental monitoring

sensors:
  - type: dht22
    pin: 18
    name: "Main Room"
    readings:
      - temperature
      - humidity

  - type: mq2
    pin: 5
    name: "Smoke Detector"
    readings:
      - smoke_level

  - type: water_leak
    pins: [4, 15]
    name: "Leak Detectors"
    locations: ["Under AC", "Near Pipes"]

alerts:
  temperature:
    threshold: 30  # Celsius
    message: "Data center temperature critical!"
    
  humidity:
    threshold: 80  # Percentage
    message: "Humidity too high!"
    
  smoke:
    threshold: 300  # PPM
    message: "Smoke detected!"
    
  water_leak:
    message: "Water leak detected!"

actions:
  - type: telegram
    chat_id: YOUR_CHAT_ID
  - type: email
    to: admin@company.com
```

## Cost Breakdown

| Category | Cost | Percentage |
|----------|------|-------------|
| Hardware | $58 | 65% |
| Assembly | $10 | 11% |
| Setup/Config | $10 | 11% |
| Spare Parts | $10 | 11% |
| **Total** | **$88** | **100%** |

## ROI Calculation

| Metric | Traditional | DC Guardian |
|--------|-------------|------------|
| Annual Cost | $48,000 | $88 + $50 maintenance |
| Savings | - | $47,850/year |
| Payback | - | 1 day |

## Testing

```bash
# Test temperature sensor
python drivers/dht22.py

# Test smoke sensor  
python drivers/mq2_smoke.py

# Test water leak
python drivers/water_leak.py

# Run all tests
python -m pytest tests/
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No temperature reading | Check DHT22 wiring, try different GPIO |
| Smoke sensor always high | Let sensor warm up for 5 minutes |
| Water sensor false positives | Adjust sensitivity in code |
| Board not connecting WiFi | Check credentials, try different channel |

## License

CERN-OHL-S-2.0 - See [LICENSE](../LICENSE)
