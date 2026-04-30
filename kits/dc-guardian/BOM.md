# DC Guardian — Bill of Materials (BOM)

Complete parts list for the data center night shift monitoring kit.

> **Total estimated cost: ~$84–88** (excluding taxes)

---

## Core Components

| # | Component | Specification | Qty | Unit Price | Total | Purchase Links |
|---|-----------|--------------|-----|-----------|-------|---------------|
| 1 | **LicheeRV-Nano** | RISC-V, 64MB RAM, WiFi/BT, USB-C | 1 | $29.00 | $29.00 | [AliExpress](https://www.aliexpress.com/item/1005006925258860.html) · [Seeed Studio](https://www.seeedstudio.com/LicheeRV-Nano.html) |
| 2 | **DHT22** | Temperature & humidity, -40~80°C, 0-100% RH | 2 | $3.50 | $7.00 | [Amazon](https://www.amazon.com/dp/B0795FJWGP) · [Adafruit](https://www.adafruit.com/product/385) |
| 3 | **MQ-2 Gas/Smoke Sensor Module** | LPG, propane, methane detection, analog+digital out | 2 | $2.50 | $5.00 | [Amazon (5-pack)](https://www.amazon.com/dp/B00LG1DHKK) · [AliExpress](https://www.aliexpress.com/item/32831520.html) |
| 4 | **Water Leak Sensor Module** | Conductive detection, digital output | 2 | $2.00 | $4.00 | [Amazon (5-pack)](https://www.amazon.com/dp/B07V5P6LVT) · [AliExpress](https://www.aliexpress.com/item/1005001623285782.html) |

## Accessories & Consumables

| # | Component | Specification | Qty | Unit Price | Total | Purchase Links |
|---|-----------|--------------|-----|-----------|-------|---------------|
| 5 | **Breadboard** | 830-point solderless | 1 | $5.00 | $5.00 | [Amazon](https://www.amazon.com/dp/B07DL13RZH) (includes jumpers) |
| 6 | **Jumper Wires** | M-F, F-F, M-M assortment (120 pcs) | 1 | — | incl. | Included with breadboard kit above |
| 7 | **USB-C Power Supply** | 5V/3A, UL listed | 1 | $6.00 | $6.00 | [Amazon](https://www.amazon.com/dp/B0962SLBQM) |
| 8 | **MicroSD Card** | 32GB Class 10 (A1) | 1 | $5.00 | $5.00 | [Amazon](https://www.amazon.com/dp/B06XWN9Q99) |
| 9 | **Ethernet Cable** | Cat6, 1m/3ft | 1 | $2.00 | $2.00 | [Amazon (5-pack)](https://www.amazon.com/dp/B00NOV71XS) |
| 10 | **ABS Project Enclosure** | 150×100×55mm, waterproof (IP65) | 1 | $8.00 | $8.00 | [Amazon](https://www.amazon.com/dp/B07QF9S1NQ) |
| 11 | **Cable Ties + Mounting Tape** | Assorted sizes + 3M VHB pads | 1 | $3.00 | $3.00 | [Amazon](https://www.amazon.com/dp/B081NQ3FHY) |

## Optional Upgrades

| # | Component | Purpose | Unit Price | Purchase Links |
|---|-----------|---------|-----------|---------------|
| 12 | **OLED Display (0.96" SSD1306)** | Local status readout | $3.50 | [Amazon](https://www.amazon.com/dp/B08JLT237F) |
| 13 | **Buzzer Module (Active)** | Audible local alarm | $1.00 | [AliExpress](https://www.aliexpress.com/item/32802677.html) |
| 14 | **PoE HAT for LicheeRV** | Power over Ethernet (no USB supply needed) | $12.00 | [AliExpress](https://www.aliexpress.com/item/100500612345.html) |
| 15 | **4-Channel Relay Module** | Auto-cut power to rack on critical alert | $3.00 | [Amazon](https://www.amazon.com/dp/B0057OC6O8) |

---

## Notes

- **All prices** are estimates as of May 2026 and may vary by supplier/location
- **AliExpress** links typically offer the lowest prices but with longer shipping (2-4 weeks)
- **Amazon** links offer faster delivery (Prime) at slightly higher cost
- **Bulk orders** (5+ units) can reduce per-kit cost by 15-20%
- **Seeed Studio** is recommended for LicheeRV-Nano as they are an authorized distributor

## Sourcing Strategy

For a **single kit**: Order LicheeRV-Nano from Seeed, sensors from Amazon — total ~$88, arrives in 3-5 days.

For **5+ kits**: Order everything from AliExpress — total ~$65/kit, arrives in 2-3 weeks.

For **production (50+ kits)**: Contact Sgica, DFRobot, or Seeed for OEM pricing — target <$40/kit.
