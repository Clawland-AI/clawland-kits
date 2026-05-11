# Assembly Instructions

## Tools

- Small screwdriver
- Wire cutter/stripper
- Multimeter
- Laptop with SSH access to the board
- Label maker or tape marker

## Step 1: Bench-check the board

1. Flash the PicClaw image or install PicClaw manually.
2. Connect the board to USB-C power.
3. Confirm it boots and joins the expected network.
4. Run `picclaw status`.

Photo checklist: board powered on, serial/SSH console visible.

## Step 2: Wire sensors on the bench

1. Connect 3V3 and GND rails first.
2. Add DHT22 #1 on GPIO17 and DHT22 #2 on GPIO18.
3. Add DS18B20 on GPIO19 with a 4.7k pull-up.
4. Add the leak probe, MQ-2 digital alert, reed switches, LEDs, and buzzer.
5. Add ADS1115 on I2C and connect the SCT-013 signal to A0.

Photo checklist: full breadboard top-down view and close-up of pull-up resistors.

## Step 3: Run sensor smoke tests

```bash
python drivers/read_dht22.py --pin GPIO17
python drivers/read_ds18b20.py --pin GPIO19
python drivers/read_discrete.py --pin GPIO20 --name leak
```

Expected result: each command prints one JSON object with `ok: true` or a clear error.

## Step 4: Load the scenario config

```bash
picclaw skill install ./kits/dc-guardian
picclaw gateway
```

Watch for a healthy `/healthz` response and normal startup logs.

## Step 5: Install in the rack room

1. Power down the prototype before moving it.
2. Put the board and breadboard into the vented enclosure.
3. Route sensor cables through strain-relief holes.
4. Place sensors using the placement rules in [WIRING.md](WIRING.md).
5. Restore power and confirm alerts reach Telegram, Discord, or webhook.

Photo checklist: final enclosure, mounted sensors, cable labels, and dashboard/alert screenshot.

## Acceptance test

Trigger each alert path once:

| Test | Method | Expected result |
|---|---|---|
| High temp | Warm DHT22 gently by hand | Warning alert, red LED |
| Door open | Move magnet away from reed switch | Security alert |
| Leak | Bridge leak probe with wet cloth | Critical leak alert, buzzer |
| Smoke/gas | Use approved canned test gas or module test button | Critical smoke alert |
| Current | Clamp known load conductor | Non-zero current sample |
