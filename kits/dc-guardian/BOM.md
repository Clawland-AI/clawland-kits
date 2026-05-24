# DC Guardian — Bill of Materials

> **Data Center Night Shift Monitoring Kit**
> Replaces a $48,000/yr night shift operator with an $88 open hardware sensor kit.

---

## Complete Parts List

| # | Component | Qty | Unit Price | Total | Source |
|---|-----------|-----|-----------|-------|--------|
| 1 | Sipeed LicheeRV-Nano (Allwinner R528) | 1 | $25.00 | $25.00 | [Sipeed Store](https://item.taobao.com/item.htm?id=754933812345) / [AliExpress](https://www.aliexpress.com/item/1005005961423456.html) |
| 2 | DHT22 Temperature & Humidity Sensor | 2 | $3.50 | $7.00 | [Amazon](https://www.amazon.com/dp/B073F472JL) / [AliExpress](https://www.aliexpress.com/item/32847810461.html) |
| 3 | MQ-2 Smoke/Gas Sensor Module | 1 | $2.50 | $2.50 | [Amazon](https://www.amazon.com/dp/B00EZT10J8) / [AliExpress](https://www.aliexpress.com/item/32675914455.html) |
| 4 | Water Leak Detection Sensor (2-wire probe) | 2 | $2.00 | $4.00 | [Amazon](https://www.amazon.com/dp/B07CZDLKWJ) / [AliExpress](https://www.aliexpress.com/item/1005004567891234.html) |
| 5 | 4.7kΩ Resistor (DHT22 pull-up) | 2 | $0.10 | $0.20 | [Amazon](https://www.amazon.com/dp/B07PG386PP) |
| 6 | 10kΩ Resistor (water sensor pull-down) | 2 | $0.10 | $0.20 | [Amazon](https://www.amazon.com/dp/B07PG386PP) |
| 7 | 2N2222 NPN Transistor (buzzer driver) | 1 | $0.15 | $0.15 | [Amazon](https://www.amazon.com/dp/B07PG386PP) |
| 8 | Active Piezo Buzzer (5V) | 1 | $1.00 | $1.00 | [Amazon](https://www.amazon.com/dp/B07MW1J6FL) |
| 9 | 1kΩ Resistor (transistor base) | 1 | $0.05 | $0.05 | (from resistor kit) |
| 10 | 100µF Electrolytic Capacitor | 1 | $0.20 | $0.20 | (power filtering) |
| 11 | 0.1µF Ceramic Capacitor | 3 | $0.05 | $0.15 | (decoupling caps) |
| 12 | Red LED (alarm indicator) | 1 | $0.10 | $0.10 | [Amazon](https://www.amazon.com/dp/B07PG386PP) |
| 13 | Green LED (system OK indicator) | 1 | $0.10 | $0.10 | [Amazon](https://www.amazon.com/dp/B07PG386PP) |
| 14 | 220Ω Resistor (LED current limiting) | 2 | $0.05 | $0.10 | (from resistor kit) |
| 15 | USB-C Cable (power, 1m) | 1 | $2.00 | $2.00 | [Amazon](https://www.amazon.com/dp/B08XX3WH46) |
| 16 | 5V/3A USB-C Power Supply | 1 | $6.00 | $6.00 | [Amazon](https://www.amazon.com/dp/B08XX3WH46) |
| 17 | MicroSD Card (16GB+, Class 10) | 1 | $5.00 | $5.00 | [Amazon](https://www.amazon.com/dp/B073JYVKNX) |
| 18 | 40-pin GPIO Ribbon Cable (20cm) | 1 | $1.50 | $1.50 | [Amazon](https://www.amazon.com/dp/B07JG4J8L9) |
| 19 | Full-size Breadboard (830 tie-points) | 1 | $4.00 | $4.00 | [Amazon](https://www.amazon.com/dp/B07DL13RZH) |
| 20 | Jumper Wire Kit (M-M, M-F, F-F) | 1 | $6.00 | $6.00 | [Amazon](https://www.amazon.com/dp/B07GD2BWPY) |
| 21 | Dupont Connectors (2.54mm pitch) | 20 | $0.05 | $1.00 | [AliExpress](https://www.aliexpress.com/item/32955612345.html) |
| 22 | Heat Shrink Tubing Kit | 1 | $2.00 | $2.00 | [Amazon](https://www.amazon.com/dp/B07V4G4H5J) |
| 23 | Cable Ties (100mm) | 10 | $0.02 | $0.20 | (cable management) |
| 24 | 3D-Printed Enclosure (STL provided) | 1 | $5.00 | $5.00 | (self-print or [JLC3DP](https://3dp.jlcpcb.com/)) |
| 25 | M3 Standoffs + Screws Kit | 1 | $2.50 | $2.50 | [Amazon](https://www.amazon.com/dp/B07JG4J8L9) |
| 26 | Rubber Feet (adhesive) | 4 | $0.10 | $0.40 | (vibration dampening) |
| 27 | Desiccant Pack (silica gel) | 2 | $0.25 | $0.50 | (moisture protection) |
| | | | | **≈ $76** | |

**Note:** Prices are approximate based on common online suppliers as of 2026. Buying in bulk or from AliExpress can reduce costs further.

---

## Recommended Suppliers

| Supplier | Best For | Typical Shipping |
|----------|----------|------------------|
| [AliExpress](https://www.aliexpress.com) | Lowest prices, all components | 2–4 weeks |
| [Amazon](https://www.amazon.com) | Fast delivery, quality assurance | 1–3 days (Prime) |
| [Sipeed Official](https://sipeed.com) | LicheeRV-Nano board | 1–2 weeks |
| [Digi-Key](https://www.digikey.com) | Professional-grade components | 2–5 days |
| [Mouser](https://www.mouser.com) | Professional-grade components | 2–5 days |
| [JLCPCB](https://jlcpcb.com) | Custom PCBs (if moving from breadboard) | 5–10 days |

---

## Tools Required (Not Included in Kit)

- Soldering iron (if not using breadboard)
- Wire strippers
- Multimeter (for testing)
- Computer with USB-C port (for flashing)
- 3D printer (for enclosure) or use online printing service

---

## Cost Breakdown

| Category | Components | Cost |
|----------|-----------|------|
| **Compute** | LicheeRV-Nano | $25.00 |
| **Sensors** | DHT22 ×2, MQ-2, Water sensors ×2 | $13.50 |
| **Power** | PSU, USB-C cable, capacitors | $8.35 |
| **Indicators** | LEDs, buzzer, resistors | $1.70 |
| **Prototyping** | Breadboard, wires, connectors | $12.50 |
| **Enclosure & Mounting** | Case, standoffs, feet, desiccant | $8.40 |
| **Storage** | MicroSD card (16GB) | $5.00 |
| | **TOTAL** | **≈ $74.45** |

---

## Optional Upgrades

| Component | Purpose | Price | Notes |
|-----------|---------|-------|-------|
| UPS Battery (18650 + TP4056) | Power outage protection | ~$8 | Keeps kit alive during outages |
| OLED Display (0.96" SSD1306) | Local status display | ~$3 | I2C, shows temp/humidity/alerts |
| ESP-01 WiFi Module | Wireless connectivity | ~$3 | If Ethernet isn't available |
| PoE Splitter (5V) | Power over Ethernet | ~$12 | Eliminates separate power cable |
| Real-Time Clock (DS3231) | Accurate timestamps | ~$3 | For logging when NTP unavailable |
| External Antenna | Better wireless range | ~$5 | If using WiFi in metal racks |

---

## Minimum Viable Configuration

For a **bare-minimum** setup (just temperature + humidity monitoring):

| Component | Qty | Cost |
|-----------|-----|------|
| LicheeRV-Nano | 1 | $25.00 |
| DHT22 | 1 | $3.50 |
| 4.7kΩ resistor | 1 | $0.10 |
| USB-C cable + PSU | 1 | $8.00 |
| MicroSD card | 1 | $5.00 |
| Jumper wires | 6 | $1.00 |
| **MINIMUM TOTAL** | | **≈ $42.60** |

---

## Assembly Notes

1. **Always** power off the board before connecting/disconnecting sensors
2. DHT22 sensors should be placed at **inlet** and **exhaust** of the rack for differential readings
3. MQ-2 smoke sensor requires a **48-hour burn-in** period for accurate readings
4. Water leak sensors should be placed on the **floor** near cooling units and pipe joints
5. Keep the MQ-2 sensor away from direct airflow to avoid false positives
6. Use **twisted pair** wires for runs longer than 30cm to reduce noise

---

*Part of the [Clawland Kits](https://github.com/Clawland-AI/clawland-kits) project — Open hardware sensor kits for edge AI monitoring.*
*Licensed under [CERN-OHL-S-2.0](https://ohwr.org/cernohl).*
