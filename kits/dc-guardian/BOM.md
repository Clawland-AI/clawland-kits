# DC Guardian — Bill of Materials

**Kit cost target: ~$88 USD** | Replaces: $48,000/yr data center night-shift operator

> All prices are approximate retail (March 2026). AliExpress links are cheaper but add 2–4 week shipping. Adafruit/Amazon links ship fast.

---

## Parts List

| # | Component | Qty | Unit Price | Extended | Supplier |
|---|-----------|:---:|:----------:|:--------:|----------|
| 1 | [Sipeed LicheeRV-Nano (512MB DDR3)](https://sipeed.com/licheervnano) | 1 | $15.99 | $15.99 | [AliExpress](https://www.aliexpress.com/item/1005006426114728.html) / [Seeed Studio](https://www.seeedstudio.com/Sipeed-LicheeRV-Nano-p-5681.html) |
| 2 | [DHT22 / AM2302 Temp + Humidity Module](https://www.adafruit.com/product/385) | 1 | $3.95 | $3.95 | [Adafruit](https://www.adafruit.com/product/385) / [Amazon](https://www.amazon.com/dp/B073F472JL) |
| 3 | [MQ-2 Smoke & Gas Sensor Module](https://www.sparkfun.com/products/retired/9405) | 1 | $2.99 | $2.99 | [AliExpress](https://www.aliexpress.com/item/32860220928.html) / [Amazon](https://www.amazon.com/dp/B00H3F9DKW) |
| 4 | [Resistive Water Leak / Rain Sensor Module](https://www.amazon.com/dp/B01N058HS6) | 2 | $1.99 | $3.98 | [Amazon](https://www.amazon.com/dp/B01N058HS6) / [AliExpress](https://www.aliexpress.com/item/32960148699.html) |
| 5 | [Resistor Kit — 1/4W (includes 4.7 kΩ)](https://www.amazon.com/dp/B08BCRZZS3) | 1 | $5.99 | $5.99 | [Amazon](https://www.amazon.com/dp/B08BCRZZS3) |
| 6 | [MicroSD Card 32 GB Class 10 A1](https://www.amazon.com/dp/B08GY9NYRM) | 1 | $8.49 | $8.49 | [Amazon](https://www.amazon.com/dp/B08GY9NYRM) |
| 7 | [USB-C 5 V / 3 A Power Adapter](https://www.amazon.com/dp/B07TYQRXTK) | 1 | $9.99 | $9.99 | [Amazon](https://www.amazon.com/dp/B07TYQRXTK) |
| 8 | [Half-size Breadboard (170 tie-points)](https://www.adafruit.com/product/64) | 1 | $3.95 | $3.95 | [Adafruit](https://www.adafruit.com/product/64) / [Amazon](https://www.amazon.com/dp/B082KBF7MM) |
| 9 | [Jumper Wires M/F 20 cm (40-pack)](https://www.amazon.com/dp/B01EV70C78) | 1 | $3.99 | $3.99 | [Amazon](https://www.amazon.com/dp/B01EV70C78) |
| 10 | [Active Piezo Buzzer 5 V](https://www.amazon.com/dp/B01N7WB5N0) | 1 | $1.99 | $1.99 | [Amazon](https://www.amazon.com/dp/B01N7WB5N0) |
| 11 | [ABS Project Enclosure 100 × 68 × 50 mm](https://www.amazon.com/dp/B07Q6ZKBLP) | 1 | $8.99 | $8.99 | [Amazon](https://www.amazon.com/dp/B07Q6ZKBLP) |
| 12 | [USB-C to USB-A Cable 1 m](https://www.amazon.com/dp/B07K4BZKPQ) | 1 | $4.99 | $4.99 | [Amazon](https://www.amazon.com/dp/B07K4BZKPQ) |
| | | | **Subtotal** | **$79.29** | |
| | Estimated shipping / taxes | | | $8.71 | |
| | **TOTAL** | | | **$88.00** | |

---

## Cost Breakdown by Category

| Category | Items | Cost |
|----------|-------|-----:|
| Compute | LicheeRV-Nano (#1) | $15.99 |
| Sensors | DHT22, MQ-2, Water sensors × 2 (#2–4) | $10.93 |
| Passives & consumables | Resistor kit, jumper wires (#5, 9) | $9.98 |
| Storage & power | MicroSD, USB-C PSU, cable (#6, 7, 12) | $23.47 |
| Prototyping | Breadboard (#8) | $3.95 |
| Alerting | Buzzer (#10) | $1.99 |
| Enclosure | ABS box (#11) | $8.99 |
| **Shipping / tax est.** | | $8.71 |
| **Total** | | **$83.01 – $93.00** |

> Price range reflects supplier variation. Order from AliExpress for ~$65 all-in (add 3-week lead time).

---

## Tools Required (not included)

| Tool | Notes |
|------|-------|
| MicroSD card reader | Flash the PicClaw image |
| Drill + 12 mm bit | Cable glands in enclosure |
| Small Phillips screwdriver | Board mounting |
| Soldering iron (optional) | For permanent sensor leads |
| Multimeter (optional) | Verify wiring before power-on |

---

## Substitutions

| Part | Drop-in Alternative |
|------|---------------------|
| LicheeRV-Nano | Orange Pi Zero 2W ($20) — same GPIO layout, minor driver changes |
| DHT22 | SHT31 breakout (I²C) — more accurate, costs ~$2 more |
| MQ-2 module | MQ-135 — broader air quality (VOC + CO₂); same wiring |
| Resistive water sensor | Float switch NC ($1.50) — simpler digital signal, no analog threshold |
| Active buzzer | Passive buzzer + PWM — allows tone variation in alerts |
