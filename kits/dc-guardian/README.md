# DC Guardian Kit

DC Guardian is an $88 edge-monitoring kit for unattended data-center night shifts. It pairs a LicheeRV Nano or similar PicClaw-capable board with environmental, leak, smoke, door, and power sensors.

## What it monitors

- Rack-room temperature and humidity
- HVAC or cold-aisle spot temperature
- Water leak near cooling lines or floor drains
- Smoke / abnormal combustible gas signal
- Rack or room door open events
- Utility or UPS branch current draw

## Deliverables

- [BOM.md](BOM.md) — parts list, purchase links, and cost breakdown
- [WIRING.md](WIRING.md) — ASCII wiring diagram and pin map
- [ASSEMBLY.md](ASSEMBLY.md) — step-by-step build guide with photo checklist
- [skill.yaml](skill.yaml) — PicClaw scenario configuration
- [alerts.yaml](alerts.yaml) — thresholds and escalation rules
- [drivers/](drivers/) — lightweight reference sensor readers

## ROI

| Item | Cost |
| --- | ---: |
| Human night-shift operator | $48,000 / year |
| DC Guardian hardware | $87.59 one-time |
| Suggested maintenance reserve | $30 / year |
| First-year avoided cost | $47,882.41 |
| Payback period | < 1 day |

## Safety notes

This kit monitors power through isolated current sensors only. Do not expose the board or breadboard wiring to mains voltage. For permanent deployments, mount the kit in an insulated enclosure and have any mains-current clamp installation reviewed by a qualified electrician.
