# DC Guardian — Data Center Night Shift Monitoring Kit

> **Replaces:** $48,000/year human night shift operator  
> **Total cost:** ~$88 in parts  
> **ROI:** 54,545% in the first year (545× return)  
> **Board:** LicheeRV-Nano (RISC-V, WiFi)  
> **Sensors:** DHT22 (temp/humidity), MQ-2 (smoke), Water leak sensor

---

## Use Case

Data centers require 24/7 monitoring for temperature spikes, smoke/fire, and water leaks. A human night shift operator costs ~$48,000/year. The DC Guardian kit provides automated real-time monitoring with instant alerts at a fraction of the cost.

### What It Detects

| Threat | Sensor | Threshold (default) | Alert Level |
|--------|--------|---------------------|-------------|
| Overheating | DHT22 | > 30°C (86°F) | 🔴 Critical |
| Humidity spike | DHT22 | > 60% RH | 🟡 Warning |
| Smoke / fire | MQ-2 | LPG > 200 ppm | 🔴 Critical |
| Water leak | Water sensor | Any contact | 🔴 Critical |

---

## Quick Start

1. **Order parts** — See [BOM.md](./BOM.md) for the complete parts list with purchase links
2. **Wire it up** — Follow the [WIRING.md](./WIRING.md) guide for connections
3. **Install drivers** — Copy `drivers/` to your LicheeRV-Nano
4. **Load the skill** — `picclaw skill install dc-guardian`
5. **Configure alerts** — Edit thresholds in `alerts.yaml`
6. **Monitor** — Check `dashboard.json` for Grafana setup

---

## Cost Breakdown

| Component | Unit Price | Qty | Total |
|-----------|-----------|-----|-------|
| LicheeRV-Nano board | $29.00 | 1 | $29.00 |
| DHT22 temp/humidity sensor | $3.50 | 2 | $7.00 |
| MQ-2 smoke/gas sensor module | $2.50 | 2 | $5.00 |
| Water leak sensor module | $2.00 | 2 | $4.00 |
| Breadboard + jumper wires kit | $5.00 | 1 | $5.00 |
| USB-C power supply (5V/3A) | $6.00 | 1 | $6.00 |
| MicroSD card (32GB) | $5.00 | 1 | $5.00 |
| Ethernet cable (1m) | $2.00 | 1 | $2.00 |
| ABS project enclosure | $8.00 | 1 | $8.00 |
| Cable ties + mounting tape | $3.00 | 1 | $3.00 |
| **Subtotal (parts)** | | | **$74.00** |
| Shipping (estimate) | $7–14 | | ~$10.00 |
| **Total** | | | **~$84–88** |

### ROI Calculation

| Item | Annual Cost |
|------|-------------|
| Human night shift operator (US avg) | $48,000 |
| DC Guardian kit (one-time) | $88 |
| Electricity (~5W × 8760h × $0.12/kWh) | $5.26 |
| Maintenance / replacement (estimate) | $50 |
| **DC Guardian Year 1 total** | **$143.26** |
| **Annual savings** | **$47,856.74** |
| **ROI** | **54,545%** |

---

## Deployment Tips

- **Place DHT22 sensors** at hot-aisle intake and cold-aisle exhaust
- **Mount MQ-2 sensors** near CRAC units and cable trays (smoke rises)
- **Position water sensors** under raised flooring and near cooling pipes
- **Secure the LicheeRV-Nano** in its enclosure on a rack shelf
- **Connect via Ethernet** for reliability (WiFi as fallback)

---

## Alerts & Escalation

See [alerts.yaml](./alerts.yaml) for configurable thresholds. Default escalation:

1. **Warning** → Log + Slack message
2. **Critical** → Log + Slack + SMS + PagerDuty
3. **Sustained critical (>5 min)** → Auto-ticket creation + phone call

---

## License

CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0)  
Hardware designs must remain open. See root [LICENSE](../../LICENSE).
