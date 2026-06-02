# DC Guardian Wiring

This guide uses an ASCII wiring diagram instead of a Fritzing file. Pin names are logical PicClaw names; map them to the matching LicheeRV-Nano header pins in the board pinout before soldering the final harness.

## ASCII Diagram

```
                         DC Guardian rack monitor

            +------------------------------------------------+
            |              Sipeed LicheeRV-Nano-WE           |
            |                                                |
            |  5V  o----------------------+------------------+---- MQ-2 VCC
            | 3V3  o----+-----------------+-------------+----+---- DHT22 VCC
            | GND  o----+-----------------+-------------+----+---- all GND
            |                                                |
            | SDA  o--------------------------- ADS1115 SDA   |
            | SCL  o--------------------------- ADS1115 SCL   |
            | GPIO17 o------------------------- DHT22 DATA    |
            | GPIO27 o---- level shifter -----> WATER OUT     |
            |                                                |
            +------------------------------------------------+
                              |
                              | I2C, address 0x48
                              v
            +---------------- ADS1115 ------------------------+
            | VDD <- 3V3    GND <- GND                       |
            | A0  <- MQ-2 analog output through divider       |
            | A1  reserved for second leak tape               |
            | A2  reserved for door/airflow sensor            |
            | A3  reserved for spare analog sensor            |
            +------------------------------------------------+

            +---------------- MQ-2 smoke/gas -----------------+
            | VCC <- 5V heater supply                         |
            | GND <- common GND                               |
            | AO  -> 20 k / 10 k divider -> ADS1115 A0        |
            | DO  -> optional level shifter -> GPIO22         |
            +------------------------------------------------+
```

## Pin Map

| Signal | LicheeRV-Nano logical pin | Device pin | Voltage | Notes |
|--------|----------------------------|------------|---------|-------|
| 3V3 | 3.3 V output | DHT22 VCC, ADS1115 VDD, level shifter LV | 3.3 V | Do not power MQ-2 heater from 3.3 V |
| 5V | USB 5 V/VBUS | MQ-2 VCC, level shifter HV | 5 V | MQ-2 heater load belongs on 5 V |
| GND | Ground | All modules | 0 V | All grounds must be common |
| SDA | I2C SDA | ADS1115 SDA | 3.3 V | Use short wires or twisted pair with GND |
| SCL | I2C SCL | ADS1115 SCL | 3.3 V | ADS1115 address remains `0x48` |
| GPIO17 | Digital input | DHT22 DATA | 3.3 V | DHT22/AM2302 modules usually include pull-up |
| GPIO27 | Digital input | Water OUT through level shifter | 3.3 V | Active high when wet |
| GPIO22 | Digital input, optional | MQ-2 DO through level shifter | 3.3 V | Optional fast threshold input |
| ADS1115 A0 | Analog input | MQ-2 AO through divider | 0 V to 3.3 V max | Use 20 k top / 10 k bottom divider for 5 V AO |

## Electrical Notes

- Power down the kit before changing sensor wiring.
- Use the level shifter for any module output that can rise to 5 V.
- The MQ-2 heater needs warm-up time and can draw more current than the logic sensors; keep it on the 5 V rail.
- Keep the DHT22 away from the LicheeRV-Nano heat plume so rack temperature readings are not biased high.
- Treat MQ-2 readings as trend signals only. This kit supplements, but does not replace, code-required fire detection.
