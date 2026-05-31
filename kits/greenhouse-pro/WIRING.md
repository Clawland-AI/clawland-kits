# Greenhouse Pro Wiring Guide

All sensor wiring is low-voltage. Keep fan and pump mains wiring outside the controller enclosure and switch it only through a properly rated relay module.

## Pin Map

| Board pin | Signal | Device |
| --- | --- | --- |
| 3V3 | VCC | BME280, BH1750, SCD41 |
| 5V | VCC | Relay module, DS18B20 if using long cable |
| GND | Ground | All modules |
| I2C SDA | Data | BME280, BH1750, SCD41 |
| I2C SCL | Clock | BME280, BH1750, SCD41 |
| ADC0 | Analog | Soil moisture probe A |
| ADC1 | Analog | Soil moisture probe B |
| GPIO16 | 1-Wire | DS18B20 data |
| GPIO17 | Digital out | Relay channel 1, fan |
| GPIO18 | Digital out | Relay channel 2, irrigation pump |

## ASCII Wiring Diagram

```text
                    +----------------------+
                    | PicClaw edge board   |
                    |                      |
  3V3 --------------+--- BME280 VCC        |
       |            |    BH1750 VCC        |
       |            |    SCD41 VCC         |
       |            |                      |
  GND --------------+--- all sensor GND ---+-------------+
                    |                                      |
  SDA --------------+--- BME280 SDA --- BH1750 SDA --- SCD41 SDA
  SCL --------------+--- BME280 SCL --- BH1750 SCL --- SCD41 SCL
                    |
  ADC0 -------------+--- soil probe A analog
  ADC1 -------------+--- soil probe B analog
                    |
  GPIO16 -----------+--- DS18B20 DATA
                    |        |
  3V3 --------------+------[4.7k] pull-up
                    |
  GPIO17 -----------+--- relay IN1 -> circulation fan
  GPIO18 -----------+--- relay IN2 -> irrigation pump
  5V ---------------+--- relay VCC
                    +----------------------+
```

## Assembly Steps

1. Mount the controller board inside the enclosure using nylon standoffs.
2. Install cable glands for soil probes, DS18B20, power, and relay control wiring.
3. Wire the I2C sensors in parallel on SDA/SCL. Keep wires shorter than 30 cm or use shielded cable.
4. Connect soil probes to ADC0 and ADC1. Label probe A as "bed inlet" and probe B as "bed outlet".
5. Add the 4.7 kOhm pull-up resistor between DS18B20 data and 3V3.
6. Wire relay IN1 to GPIO17 and IN2 to GPIO18. Keep the load side isolated from sensor wiring.
7. Run the validator and dry-run driver scripts before energizing the pump or fan.

## Placement

- Place BME280 and SCD41 in the plant canopy airflow path, shielded from direct mist.
- Place BH1750 above the canopy with a small diffuser cap.
- Insert soil probes at root-zone depth and at least 10 cm from irrigation emitters.
- Strap the DS18B20 probe to a representative leaf clip or reservoir pipe.

## Bring-Up Checklist

- I2C scan detects addresses `0x23` for BH1750, `0x62` for SCD41, and `0x76` or `0x77` for BME280.
- Soil dry calibration is higher than wet calibration for the selected ADC wiring.
- Relay LEDs toggle without load before connecting fan or pump.
- First report contains all expected fields from `skill.yaml`.

