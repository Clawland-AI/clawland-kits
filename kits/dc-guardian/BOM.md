# DC Guardian BOM

Prices are approximate single-unit US street prices before tax and shipping. Purchase links point to common suppliers or manufacturer pages so builders can substitute local stock while keeping the same electrical interfaces.

## Bill of Materials

| Qty | Part | Purpose | Est. unit | Est. total | Purchase link |
|-----|------|---------|-----------|------------|---------------|
| 1 | Sipeed LicheeRV-Nano-WE | Linux edge board with Ethernet and WiFi backup | $26.00 | $26.00 | [Sipeed LicheeRV Nano](https://en.wiki.sipeed.com/hardware/en/lichee/RV_Nano/1_intro.html) |
| 1 | DHT22/AM2302 temperature and humidity sensor | Hot aisle temperature and humidity | $8.00 | $8.00 | [DHT22 AM2302 module](https://www.pishop.us/product/dht22-am2302-digital-temperature-humidity-sensor-for-arduino/) |
| 1 | Grove MQ-2 gas/smoke sensor | Smoke and abnormal gas trend | $7.60 | $7.60 | [Seeed Grove Gas Sensor MQ2](https://www.seeedstudio.com/Grove-Gas-Sensor-MQ2.html) |
| 1 | ADS1115 16-bit ADC breakout | Analog input for MQ-2 trend reading | $14.95 | $14.95 | [Adafruit ADS1115](https://www.adafruit.com/product/1085) |
| 1 | Digital water detection sensor | Floor and condensate leak detection | $1.95 | $1.95 | [Adafruit water detection sensor](https://www.adafruit.com/product/4965) |
| 1 | 4-channel bidirectional level shifter | Protects 3.3 V GPIO from 5 V sensor outputs | $3.95 | $3.95 | [Adafruit BSS138 level shifter](https://www.adafruit.com/product/757) |
| 1 | 16 GB microSD card | Boot storage and local buffer | $6.00 | $6.00 | [SanDisk 16 GB microSD example](https://www.westerndigital.com/products/memory-cards/sandisk-ultra-uhs-i-microsd) |
| 1 | 5 V 2 A USB-C power supply | Board and MQ-2 heater power | $8.00 | $8.00 | [Raspberry Pi USB-C supply](https://www.raspberrypi.com/products/type-c-power-supply/) |
| 1 | Half-size breadboard or solderable proto board | Sensor interconnect | $4.00 | $4.00 | [Adafruit half-size breadboard](https://www.adafruit.com/product/64) |
| 1 | Male/female jumper wire kit | Harness wiring | $4.00 | $4.00 | [Adafruit jumper wires](https://www.adafruit.com/product/1957) |
| 1 | Ventilated ABS enclosure, about 100 mm x 60 mm | Rack-side electronics enclosure | $3.50 | $3.50 | [Polycase enclosure examples](https://www.polycase.com/electronic-enclosures) |

## Cost Breakdown

| Category | Cost |
|----------|------|
| Compute and storage | $32.00 |
| Sensors | $17.55 |
| Signal conditioning | $18.90 |
| Power and wiring | $16.00 |
| Enclosure | $3.50 |
| **Estimated kit total** | **$87.95** |
| Annual overnight operator cost avoided | $48,000.00 |
| Simple first-year savings before network/cloud costs | $47,912.05 |

## Substitution Rules

- Keep all GPIO-facing signals at 3.3 V.
- Use a DHT22/AM2302 class sensor with a digital data pin and 3.3 V compatible output.
- Use an MQ-2 module only for smoke/gas trend alerting. It is not a certified life-safety smoke detector.
- Use any ADS1115-compatible I2C ADC at address `0x48`.
- Use a normally-dry water leak sensor with a digital output.
