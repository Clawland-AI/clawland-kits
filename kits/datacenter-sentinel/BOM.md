# Bill of Materials (BOM)

**Datacenter Sentinel Kit** — Complete parts list with purchase links

Last updated: 2026-02-16

---

## Quick Summary

| Configuration | Total Cost | Components |
|--------------|------------|------------|
| **Minimum** | $56.78 | Core sensors only |
| **Recommended** | $72.26 | + Buzzer, LED, case |
| **Enterprise** | $131.24 | + 4G, battery backup |

---

## Core Components

| # | Component | Specification | Qty | Unit Price | Total | Supplier | Part Number / Link |
|---|-----------|---------------|-----|------------|-------|----------|--------------------|
| 1 | Single Board Computer | LicheeRV-Nano (SG2002, 256MB RAM, WiFi) | 1 | $17.90 | $17.90 | Sipeed/Aliexpress | [Link](https://www.aliexpress.com/item/1005007394149933.html) |
| 1a | *Alternative SBC* | *Raspberry Pi Zero 2 W (RP3A0, 512MB, WiFi)* | *1* | *$15.00* | *$15.00* | *Adafruit* | [*#5291*](https://www.adafruit.com/product/5291) |
| 2 | Temperature/Humidity Sensor | DHT22 (AM2302), ±0.5°C, ±2% RH | 1 | $4.95 | $4.95 | Adafruit | [#385](https://www.adafruit.com/product/385) |
| 3 | Smoke/Gas Sensor | MQ-2 Digital/Analog Module, 5V heater | 1 | $3.49 | $3.49 | Amazon | [B07R9K5R7Z](https://www.amazon.com/dp/B07R9K5R7Z) |
| 4 | Water Leak Sensor | Water Level Detection Module, 3.3V/5V | 2 | $1.99 | $3.98 | Amazon | [B07THDH7Y4](https://www.amazon.com/dp/B07THDH7Y4) |
| 5 | MicroSD Card | 32GB Class 10, A1 rating | 1 | $6.99 | $6.99 | Amazon/SanDisk | [B08TJRVWV1](https://www.amazon.com/dp/B08TJRVWV1) |
| 6 | Power Supply | USB-C 5V 3A (15W), UL listed | 1 | $7.99 | $7.99 | Amazon/Anker | [B07TYQRXTK](https://www.amazon.com/dp/B07TYQRXTK) |
| | | | | **Subtotal (Core)** | **$45.30** | | |

---

## Wiring & Connectors

| # | Component | Specification | Qty | Unit Price | Total | Supplier | Part Number / Link |
|---|-----------|---------------|-----|------------|-------|----------|--------------------|
| 7 | Jumper Wires | Female-to-Female, 20cm, 40-pin set | 1 | $5.99 | $5.99 | Amazon | [B077NH83CJ](https://www.amazon.com/dp/B077NH83CJ) |
| 8 | Breadboard | 400-point solderless (for prototyping) | 1 | $4.99 | $4.99 | Amazon | [B082KBF7MM](https://www.amazon.com/dp/B082KBF7MM) |
| 9 | Pull-up Resistor | 10kΩ 1/4W carbon film (for DHT22) | 1 | $0.10 | $0.10 | DigiKey/Yageo | [CFR-25JB-52-10K](https://www.digikey.com/en/products/detail/yageo/CFR-25JB-52-10K/12697) |
| 10 | Screw Terminals | 2-pin 5mm pitch (for water sensors) | 2 | $0.50 | $1.00 | Amazon | [B07BS126FK](https://www.amazon.com/dp/B07BS126FK) |
| | | | | **Subtotal (Wiring)** | **$12.08** | | |

**Minimum Kit Total**: $45.30 + $12.08 = **$57.38**

---

## Optional Add-ons

### Local Alerts

| # | Component | Specification | Qty | Unit Price | Total | Supplier | Part Number / Link |
|---|-----------|---------------|-----|------------|-------|----------|--------------------|
| 11 | Alarm Buzzer | Active piezo 5V, 85dB @ 10cm | 1 | $2.49 | $2.49 | Adafruit | [#1536](https://www.adafruit.com/product/1536) |
| 12 | Status LED (Red) | 5mm red LED, 20mA | 1 | $0.25 | $0.25 | DigiKey | [QTB](https://www.digikey.com/en/products/detail/qt-brightek/QTB-TWIN5mm/2618030) |
| 13 | Status LED (Green) | 5mm green LED, 20mA | 1 | $0.25 | $0.25 | DigiKey | [QTB](https://www.digikey.com/en/products/detail/qt-brightek/QTB-TWIN5mm/2618030) |
| 14 | LED Resistors | 220Ω 1/4W (current limiting) | 2 | $0.10 | $0.20 | DigiKey | [CFR-25JB-52-220R](https://www.digikey.com/en/products/detail/yageo/CFR-25JB-52-220R/12733) |

**Recommended Kit Total**: $57.38 + $5.19 = **$62.57**

---

### Enterprise Backup

| # | Component | Specification | Qty | Unit Price | Total | Supplier | Part Number / Link |
|---|-----------|---------------|-----|------------|-------|----------|--------------------|
| 15 | 4G LTE Module | SIM7600G-H, global bands, USB | 1 | $39.99 | $39.99 | Amazon/Waveshare | [B08R9YZLVV](https://www.amazon.com/dp/B08R9YZLVV) |
| 16 | Battery Pack | 10,000mAh USB-C PD, ~40h runtime | 1 | $18.99 | $18.99 | Amazon/Anker | [B07QXV6N1B](https://www.amazon.com/dp/B07QXV6N1B) |

**Enterprise Kit Total**: $62.57 + $58.98 = **$121.55**

---

### Enclosure & Mounting

| # | Component | Specification | Qty | Unit Price | Total | Supplier | Notes |
|---|-----------|---------------|-----|------------|-------|----------|-------|
| 17 | 3D Printed Case | PLA/ABS, vented design | 1 | $0-$8 | $8.00 | DIY/Service | See `enclosure/` folder for STL files |
| 18 | Heat Shrink Tubing | 3mm assortment, 2:1 shrink ratio | 1m | $2.99 | $2.99 | Amazon | [B084GDLSCK](https://www.amazon.com/dp/B084GDLSCK) |
| 19 | Zip Ties | 4" black nylon, 100-pack | 10 | $3.99 | $0.40 | Amazon | [B001E1Y5O6](https://www.amazon.com/dp/B001E1Y5O6) |
| 20 | Double-sided Tape | VHB 3M, 1" × 15ft | 1 | $9.99 | $9.99 | Amazon/3M | [B00PX22RO](https://www.amazon.com/dp/B00PX22RO0) |

**Full Kit w/ Enclosure**: $121.55 + $21.38 = **$142.93**

---

## Tools Required (not included)

| Tool | Purpose | Est. Cost | Can borrow? |
|------|---------|-----------|-------------|
| Soldering iron | Solder pull-up resistor, permanent connections | $15-$50 | Yes |
| Wire strippers | Strip jumper wires for screw terminals | $10-$20 | Yes |
| Multimeter | Verify voltage levels, continuity testing | $15-$30 | Yes |
| MicroSD card reader | Flash PicClaw image | $8-$15 | Often built-in |
| 3D Printer | Print enclosure (optional) | $200-$500 | Use service ($8) |

**If you already have basic electronics tools, you need nothing extra.**

---

## Supplier Notes

### Preferred Suppliers (US)

| Supplier | Pros | Cons | Shipping | Best For |
|----------|------|------|----------|----------|
| **Amazon** | Fast (1-2 day Prime), easy returns | Slightly higher prices | Free w/ Prime | Convenience |
| **Adafruit** | High quality, well-documented | Higher prices | $6-$10 | Sensors |
| **DigiKey** | Huge selection, engineering data | Bulk focus (min qty) | Free >$50 | Passives |
| **Aliexpress** | Cheapest prices | 2-4 week shipping | Free slow | Budget |

### International Alternatives

| Region | Supplier | Notes |
|--------|----------|-------|
| **Europe** | Pimoroni, Reichelt, TME | UK/Germany-based |
| **Asia** | Taobao, Shenzhen markets | Local pickup available |
| **Australia** | Core Electronics, element14 | Fast AU shipping |

### Bulk Discounts

Building >10 kits? Contact suppliers for quantity pricing:
- Amazon: 10+ units = ~10% off
- Adafruit: Educational discount program
- DigiKey: Tape-and-reel (1000+ resistors @ $0.002 ea)

---

## Revision History

| Date | Version | Changes | Author |
|------|---------|---------|--------|
| 2026-02-16 | 1.0 | Initial BOM for Issue #1 | Clawland Community |

---

## License

**CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0)**

See [../../LICENSE](../../LICENSE)
