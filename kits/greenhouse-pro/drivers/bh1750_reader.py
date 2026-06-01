class BH1750Reader:
    CONTINUOUS_HIGH_RES_MODE = 0x10

    def __init__(self, i2c, address=0x23):
        self.i2c = i2c
        self.address = address

    def read_lux(self):
        data = self.i2c.readfrom_mem(self.address, self.CONTINUOUS_HIGH_RES_MODE, 2)
        raw = (data[0] << 8) | data[1]
        return round(raw / 1.2, 1)

