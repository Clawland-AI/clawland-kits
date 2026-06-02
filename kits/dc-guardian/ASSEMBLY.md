# DC Guardian Assembly

## Photo References

Use these photos while identifying the parts on the bench:

| Step | Photo |
|------|-------|
| LicheeRV-Nano board orientation | ![LicheeRV-Nano board](https://en.wiki.sipeed.com/hardware/en/lichee/assets/RV_Nano/intro/RV_Nano_3.jpg) |
| DHT22/AM2302 body and three-wire lead | ![DHT22 AM2302 sensor](https://cdn-shop.adafruit.com/145x109/393-00.jpg) |
| MQ-2 smoke/gas module | ![Grove MQ-2 module](https://media-cdn.seeedstudio.com/media/catalog/product/cache/48035b5512857d0ab907b31a092da78f/h/t/httpsstatics3.seeedstudio.comimagesproductgas20sensor20mq.jpg) |
| ADS1115 ADC breakout | ![ADS1115 ADC breakout](https://cdn-shop.adafruit.com/145x109/1085-10.jpg) |
| Water leak sensor trace face | ![Water leak sensor](https://cdn-shop.adafruit.com/145x109/4965-06.jpg) |

## Assembly Steps

1. Flash the LicheeRV-Nano-WE boot image onto the microSD card and confirm the board reaches a shell before adding sensors.
2. Install headers on the LicheeRV-Nano, ADS1115, level shifter, and sensor modules if they were purchased without headers.
3. Mount the LicheeRV-Nano and breadboard or proto board inside the ventilated enclosure. Leave airflow slots unobstructed.
4. Wire the 3.3 V rail, 5 V rail, and common ground first. Verify 3.3 V and 5 V with a multimeter before connecting signal wires.
5. Wire the ADS1115 to I2C SDA/SCL, 3.3 V, and ground. Boot the board and verify `i2cdetect` shows address `0x48`.
6. Wire DHT22 VCC to 3.3 V, GND to ground, and DATA to `GPIO17`.
7. Wire MQ-2 VCC to 5 V and GND to common ground. Route MQ-2 analog output through a 20 k / 10 k divider before ADS1115 `A0`.
8. Wire the water sensor output through the level shifter into `GPIO27`; keep the exposed copper traces facing the floor.
9. Route sensor leads through cable glands or strain relief holes. Label both ends of every field lead.
10. Mount the enclosure on the rack side rail. Place the DHT22 in the airflow, the MQ-2 in open air, and the water sensor at the lowest expected leak point.
11. Install [skill.yaml](skill.yaml) and [alerts.yaml](alerts.yaml), then run the verification checklist in the kit README.

## Bench Test

| Test | Expected result |
|------|-----------------|
| Boot with no sensors touched | PicClaw reports normal status after MQ-2 warm-up |
| Warm DHT22 gently by hand | Temperature trend rises within 10 seconds |
| Breathe near DHT22 briefly | Humidity trend rises within 10 seconds |
| Touch water sensor with damp cloth | Critical `water_leak` alert fires immediately |
| Hold MQ-2 near a safe smoke/gas test source | `smoke_gas_trend` moves above baseline |

Do not test the MQ-2 with open flame inside a rack room. Calibrate with the sensor on the bench or with a controlled non-production test source.
