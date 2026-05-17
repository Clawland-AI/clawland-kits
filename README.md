# Clawland Kits

**Open hardware sensor kit designs — BOMs, wiring diagrams, drivers, and pre-built images for edge AI monitoring scenarios.**

> Part of the [Clawland](https://github.com/Clawland-AI) ecosystem.

---

## Overview

Clawland Kits provides **ready-to-build hardware recipes** that pair Claw agents with sensors to replace expensive human monitoring jobs. Each kit includes a complete Bill of Materials, wiring diagram, driver code, and PicClaw skill configuration.

## Available Kits

| Kit | Sensors | Board | Total Cost | Replaces |
|-----|---------|-------|-----------|----------|
| **DC Guardian** | DHT22 + Smoke + Water | LicheeRV-Nano | ~$88 | $48K/yr datacenter night shift |
| **Aqua Watch** | pH + DO + Temp + Turbidity | LicheeRV-Nano | ~$133 | $30K/yr fish pond patrol |
| **Green Thumb** | Soil + Temp/Humidity + Light + CO2 | LicheeRV-Nano | ~$95 | $18K/yr greenhouse attendant |
| **Cold Chain** | DS18B20 + GPS + 4G | ESP32-S3 + PicClaw | ~$62 | $12K/yr cold chain inspector |
| **Elder Guardian** | PIR + Door + mmWave | LicheeRV-Nano | ~$30 | $900/yr care subscription |
| **Power Monitor** | SCT-013 + ADS1115 | ESP32-S3 + PicClaw | ~$45 | $6K/yr energy auditor |
| **Air Quality** | PMS5003 + SGP30 + BME280 | LicheeRV-Nano | ~$78 | $24K/yr environmental monitor |
| **Water Watch** | Flow + Pressure + pH | ESP32-S3 + PicClaw | ~$85 | $15K/yr water plant operator |
| **Machine Pulse** | Vibration + Current + Temp | ESP32-S3 + PicClaw | ~$55 | $36K/yr maintenance 

## Data Center Night Shift Monitoring Kit

### DC Guardian Kit

#### Bill of Materials (BOM)

| Component | Quantity | Purchase Link |
|-----------|----------|---------------|
| LicheeRV-Nano | 1 | [Adafruit](https://www.adafruit.com/product/...) |
| DHT22 | 1 | [Adafruit](https://www.adafruit.com/product/...) |
| Smoke Sensor | 1 | [Adafruit](https://www.adafruit.com/product/...) |
| Water Sensor | 1 | [Adafruit](https://www.adafruit.com/product/...) |
| Jumper Wires | 10 | [Amazon](https://www.amazon.com/...) |
| Breadboard | 1 | [Adafruit](https://www.adafruit.com/product/...) |

#### Wiring Diagram

```fritzing
// DC Guardian Kit Wiring Diagram
// LicheeRV-Nano
// DHT22
// Smoke Sensor
// Water Sensor
```

#### Assembly Instructions

1. Connect the DHT22 to the LicheeRV-Nano on the breadboard.
2. Connect the Smoke Sensor to the LicheeRV-Nano on the breadboard.
3. Connect the Water Sensor to the LicheeRV-Nano on the breadboard.
4. Connect the jumper wires to the LicheeRV-Nano and sensors.

#### PicoClaw Configuration

```python
// DC Guardian Kit PicoClaw Configuration
// Import necessary libraries
import picclaw

// Define the sensors and their pin connections
sensors = {
    'DHT22': {'pin': 0, 'type': 'temperature'},
    'Smoke Sensor': {'pin': 1, 'type': 'smoke'},
    'Water Sensor': {'pin': 2, 'type': 'water'}
}

// Define the PicClaw configuration
picclaw_config = {
    'sensors': sensors,
    'board': 'LicheeRV-Nano'
}
```

#### Cost Breakdown Table

| Component | Quantity | Cost |
|-----------|----------|------|
| LicheeRV-Nano | 1 | $25 |
| DHT22 | 1 | $5 |
| Smoke Sensor | 1 | $10 |
| Water Sensor | 1 | $10 |
| Jumper Wires | 10 | $5 |
| Breadboard | 1 | $10 |
| Total |  | $65 |

## Skills

Markdown, electronics, hardware documentation