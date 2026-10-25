# DC Guardian — Data Center Night Shift Monitoring Kit

**An $88 open-hardware kit that watches temperature, smoke, and water ingress in a server room overnight — replacing a $48,000/yr night-shift operator round.**

> Part of the [Clawland Kits](../../README.md) collection. Licensed CERN-OHL-S-2.0.

---

## The Problem

Data centers pay operators to walk the floor at night and check for:

- Hot spots and CRAC failures (temperature / humidity)
- Smoke or burning insulation
- Condensation and water leaks under raised floors

A night-shift operator costs roughly **$48,000/yr**. Most nights nothing happens — but the one night something does, minutes matter.

## The Kit

DC Guardian puts a $35 LicheeRV-Nano and three sensors on the wall. PicoClaw samples them every 30 seconds, applies the thresholds in [`alerts.yaml`](alerts.yaml), and escalates through MQTT / webhook / SMS.

| Capability | Sensor | Sample rate |
|-----------|--------|-------------|
| Temperature + humidity | DHT22 | 30 s |
| Smoke / combustion gas | MQ-2 | 10 s |
| Water on floor | Water leak probe | 5 s |

**Total build cost: ~$88.** See [`BOM.md`](BOM.md) for the full parts list and [`WIRING.md`](WIRING.md) for connections.

## Cost Breakdown

| Item | Qty | Unit | Subtotal |
|------|-----|------|----------|
| LicheeRV-Nano (board) | 1 | $35.00 | $35.00 |
| DHT22 temperature/humidity sensor | 1 | $6.00 | $6.00 |
| MQ-2 smoke sensor module | 1 | $5.00 | $5.00 |
| Water leak probe (resistive) | 1 | $4.00 | $4.00 |
| 5 V / 2 A power supply | 1 | $8.00 | $8.00 |
| 32 GB microSD | 1 | $7.00 | $7.00 |
| DIN-rail / wall enclosure | 1 | $9.00 | $9.00 |
| Jumper wires + terminal blocks | 1 | $3.00 | $3.00 |
| Perfboard + standoffs | 1 | $4.00 | $4.00 |
| Misc (heat-shrink, fuses, cable ties) | 1 | $7.00 | $7.00 |
| **Total** | | | **$88.00** |

**Payback:** under 16 hours of operator time.

## Assembly

Photos live in `docs/images/`. Steps:

1. **Prepare the enclosure.** Drill a 6 mm cable gland hole for the sensor leads and a 12 mm hole for the DC jack. Deburr.
2. **Mount the board.** Fix the LicheeRV-Nano on 5 mm standoffs over the perfboard. Do not let it touch the enclosure floor.
3. **Wire the sensors** exactly as shown in [`WIRING.md`](WIRING.md). Solder the MQ-2 voltage divider inline and heat-shrink it.
4. **Flash PicoClaw** to the microSD, boot the board, confirm it joins the network.
5. **Install the skill:** `picclaw skill install dc-guardian`.
6. **Edit thresholds** in `alerts.yaml` for your room (defaults assume 18–27 °C, 30–60 % RH).
7. **Mount the sensors:** DHT22 at 1.5 m height away from the exhaust; MQ-2 near the ceiling above the racks; leak probe on the floor under the raised-floor tiles.
8. **Run the self-test** (see below) and leave the kit in soak for 24 h before trusting it.

## Self-Test

```bash
picclaw skill run dc-guardian --self-test
```

Expected: three sensor readings, all within plausible range, and one test alert delivered to your configured channel.

## Configuration

- [`skill.yaml`](skill.yaml) — PicoClaw skill definition (sensors, intervals, MQTT topics)
- [`alerts.yaml`](alerts.yaml) — thresholds and escalation ladder

## Safety Notes

- The MQ-2 heater draws ~150 mA at 5 V. Power the kit from its own 5 V / 2 A supply, not from a USB port on a server.
- MQ-2 needs a 24–48 h burn-in before readings stabilise.
- This kit is a **supplement**, not a replacement for a certified fire panel.

## License

CERN Open Hardware Licence Version 2 — Strongly Reciprocal (CERN-OHL-S-2.0). See [LICENSE](../../LICENSE).
