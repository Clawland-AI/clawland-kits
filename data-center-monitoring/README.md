# Data Center Night Shift Monitoring Kit

A $88 kit that replaces a $48,000/year night shift operator with automated monitoring.

## Bill of Materials (BOM)

| Component | Quantity | Unit Price | Total | Source |
|-----------|----------|------------|-------|--------|
| Raspberry Pi Pico W | 1 | $6.00 | $6.00 | [Adafruit](https://www.adafruit.com/product/5526) |
| DHT22 Temperature/Humidity Sensor | 2 | $4.50 | $9.00 | [Adafruit](https://www.adafruit.com/product/385) |
| DS18B20 Waterproof Temperature Probe | 2 | $3.50 | $7.00 | [Adafruit](https://www.adafruit.com/product/381) |
| 4.7kΩ Resistor (for DS18B20) | 2 | $0.10 | $0.20 | [Adafruit](https://www.adafruit.com/product/2784) |
| LED (Status Indicator) | 3 | $0.20 | $0.60 | [Adafruit](https://www.adafruit.com/product/1760) |
| 220Ω Resistors (for LEDs) | 3 | $0.10 | $0.30 | [Adafruit](https://www.adafruit.com/product/2780) |
| Breadboard (Full Size) | 1 | $5.00 | $5.00 | [Adafruit](https://www.adafruit.com/product/239) |
| Jumper Wires (M-M Pack) | 1 | $4.00 | $4.00 | [Adafruit](https://www.adafruit.com/product/1957) |
| USB-C Cable (Power) | 1 | $3.00 | $3.00 | [Adafruit](https://www.adafruit.com/product/5179) |
| Micro USB Cable (Programming) | 1 | $3.00 | $3.00 | [Adafruit](https://www.adafruit.com/product/592) |
| Enclosure (Weather Resistant) | 1 | $15.00 | $15.00 | [Amazon](https://www.amazon.com/dp/B08GJBXJ4F) |
| Power Supply (5V 2A) | 1 | $8.00 | $8.00 | [Adafruit](https://www.adafruit.com/product/1995) |
| Velcro Strips (Mounting) | 1 | $5.00 | $5.00 | [Amazon](https://www.amazon.com/dp/B07H5JJPJL) |
| Zip Ties (Cable Management) | 1 | $3.00 | $3.00 | [Amazon](https://www.amazon.com/dp/B07H5JJPJL) |
| Heat Shrink Tubing | 1 | $5.00 | $5.00 | [Amazon](https://www.amazon.com/dp/B07H5JJPJL) |
| **TOTAL** | | | **$88.10** | |

## Wiring Diagram (ASCII)

```
                    ┌─────────────────────────────────────────┐
                    │          Raspberry Pi Pico W            │
                    │                                         │
                    │  3V3 ────────────────────────────────── │
                    │  GND ────────────────────────────────── │
                    │  GP2 ────────────────────────────────── │
                    │  GP3 ────────────────────────────────── │
                    │  GP4 ────────────────────────────────── │
                    │  GP5 ────────────────────────────────── │
                    │  GP6 ────────────────────────────────── │
                    │  GP7 ────────────────────────────────── │
                    │  GP8 ────────────────────────────────── │
                    │  GP9 ────────────────────────────────── │
                    └─────────────────────────────────────────┘
                              │   │   │   │   │   │
                              │   │   │   │   │   │
        ┌─────────────────────┘   │   │   │   │   └─────────────────────┐
        │                         │   │   │   │                         │
        ▼                         ▼   ▼   ▼   ▼                         ▼
   ┌─────────┐              ┌─────────┐   ┌─────────┐              ┌─────────┐
   │  DHT22  │              │ DS18B20 │   │ DS18B20 │              │  DHT22  │
   │ Sensor 1│              │ Probe 1 │   │ Probe 2 │              │ Sensor 2│
   │         │              │         │   │         │              │         │
   │ VCC─3V3 │              │ VCC─3V3 │   │ VCC─3V3 │              │ VCC─3V3 │
   │ GND─GND │              │ GND─GND │   │ GND─GND │              │ GND─GND │
   │ DATA─GP2│              │ DATA─GP4│   │ DATA─GP6│              │ DATA─GP8│
   └─────────┘              └────┬────┘   └────┬────┘              └─────────┘
                                 │             │
                                 │             │
                            ┌────┴────┐   ┌────┴────┐
                            │ 4.7kΩ   │   │ 4.7kΩ   │
                            │ Pull-up │   │ Pull-up │
                            │ to 3V3  │   │ to 3V3  │
                            └─────────┘   └─────────┘

   LED Status Indicators:
   ┌─────────┐  ┌─────────┐  ┌─────────┐
   │ Green   │  │ Yellow  │  │ Red     │
   │ (OK)    │  │ (Warn)  │  │ (Alert) │
   │ GP3     │  │ GP5     │  │ GP7     │
   └─────────┘  └─────────┘  └─────────┘
```

## Assembly Instructions

### Step 1: Prepare the Pico W

1. Solder headers to the Pico W if not pre-soldered
2. Connect Pico W to breadboard
3. Connect power rails (3V3 and GND)

### Step 2: Install DHT22 Sensors

1. Place DHT22 sensors on breadboard
2. Connect VCC to 3V3 rail
3. Connect GND to GND rail
4. Connect DATA pins to GP2 and GP8
5. Add 10kΩ pull-up resistor between DATA and VCC (optional, DHT22 has internal pull-up)

### Step 3: Install DS18B20 Probes

1. Connect DS18B20 probes to breadboard
2. Connect VCC to 3V3 rail
3. Connect GND to GND rail
4. Connect DATA pins to GP4 and GP6
5. Add 4.7kΩ pull-up resistor between DATA and 3V3 (required for OneWire)

### Step 4: Install LED Indicators

1. Connect LEDs to breadboard
2. Connect 220Ω resistors in series with each LED
3. Connect Green LED to GP3
4. Connect Yellow LED to GP5
5. Connect Red LED to GP7

### Step 5: Mount in Enclosure

1. Place breadboard in weather-resistant enclosure
2. Secure with velcro strips
3. Route cables through enclosure holes
4. Seal with heat shrink tubing

### Step 6: Configure PicoClaw

1. Flash MicroPython firmware to Pico W
2. Upload monitoring script
3. Configure WiFi credentials
4. Set temperature thresholds

## Cost Breaktable

| Category | Cost |
|----------|------|
| Microcontroller | $6.00 |
| Sensors | $16.00 |
| Passive Components | $4.10 |
| Cables & Connectors | $6.00 |
| Enclosure & Mounting | $23.00 |
| Power Supply | $8.00 |
| **Total Hardware** | **$63.10** |
| Shipping (estimated) | $25.00 |
| **Grand Total** | **$88.10** |

## ROI Calculation

- **Night Shift Operator Cost:** $48,000/year
- **Kit Cost:** $88.10 (one-time)
- **Annual Savings:** $47,911.90
- **ROI:** 54,372%

## Maintenance

- Replace sensors every 2-3 years
- Check connections monthly
- Update firmware quarterly
- Backup configuration weekly

## Troubleshooting

### Sensor Not Reading
- Check wiring connections
- Verify pull-up resistors
- Test with multimeter

### No WiFi Connection
- Verify SSID and password
- Check signal strength
- Move closer to router

### False Alerts
- Adjust thresholds in config
- Check sensor placement
- Verify calibration

## License

MIT
