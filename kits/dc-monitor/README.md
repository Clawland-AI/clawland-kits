# Data Center Night Shift Monitoring Kit 🏢🐾⚡️

This kit provides 24/7 environmental monitoring for data centers, designed to replace manual inspections with high-precision automation.

## 💰 Cost Breakdown Table

| Item | Unit Cost | Quantity | Total |
| :--- | :--- | :--- | :--- |
| **PicoClaw** (RP2040) | $15.00 | 1 | $15.00 |
| **DHT22** Temp/Humidity Sensor | $5.00 | 1 | $5.00 |
| **MQ-2** Gas/Smoke Sensor | $7.00 | 1 | $7.00 |
| **I2C OLED Display** (128x64) | $8.00 | 1 | $8.00 |
| **Passive Buzzer** | $2.00 | 1 | $2.00 |
| **Enclosure & Jumpers** | $10.00 | 1 | $10.00 |
| **TOTAL** | | | **$47.00** |

## 📦 Bill of Materials (BOM)

1.  **PicoClaw Control Board**: [Buy on Amazon/AliExpress]
2.  **DHT22 Sensor**: For precise thermal monitoring.
3.  **MQ-2 Sensor**: For smoke and fire detection.
4.  **0.96" OLED Display**: Local status visualization.
5.  **Buzzer**: Audible alarm for local technicians.

## 🔌 Wiring Diagram (ASCII)

```text
       +-----------------------+
       |       PicoClaw        |
       |                       |
       |  3V3 ---- DHT22 VCC   |
       |  GND ---- DHT22 GND   |
       |  GP15 --- DHT22 DATA  |
       |                       |
       |  3V3 ---- OLED VCC    |
       |  GND ---- OLED GND    |
       |  GP4 ---- OLED SDA    |
       |  GP5 ---- OLED SCL    |
       |                       |
       |  5V  ---- MQ-2 VCC    |
       |  GND ---- MQ-2 GND    |
       |  GP26 --- MQ-2 ANALOG |
       |                       |
       |  GP16 --- Buzzer (+)  |
       |  GND ---- Buzzer (-)  |
       +-----------------------+
```

## 🛠 Assembly Instructions

1.  **Prepare the Enclosure**: Drill holes for the DHT22 and MQ-2 sensors to ensure airflow.
2.  **Mount the Board**: Secure the PicoClaw using M2.5 standoffs.
3.  **Wiring**: Follow the diagram above using female-to-female jumper wires.
4.  **Final Check**: Ensure no loose wires are touching the Pico's heat sink.

## ⚙️ PicoClaw Configuration

Deploy the `temperature-alert` skill and configure thresholds:
- `threshold_high`: 35°C (Ambient) / 75°C (Rack)
- `gas_threshold`: 300 ppm

---
*Replacing high-cost labor with low-cost, high-reliability Clawland automation. ⚡️🐾*
