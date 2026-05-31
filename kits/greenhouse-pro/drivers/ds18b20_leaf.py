class LeafTemperature:
    def __init__(self, ds18b20, rom):
        self.ds18b20 = ds18b20
        self.rom = rom

    def read_celsius(self):
        self.ds18b20.convert_temp()
        return round(float(self.ds18b20.read_temp(self.rom)), 2)

