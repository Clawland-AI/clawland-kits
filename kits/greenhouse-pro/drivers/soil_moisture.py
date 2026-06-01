class SoilMoisture:
    def __init__(self, adc, dry_adc, wet_adc):
        self.adc = adc
        self.dry_adc = dry_adc
        self.wet_adc = wet_adc

    def read_percent(self):
        raw = self.adc.read_u16() if hasattr(self.adc, "read_u16") else int(self.adc())
        span = max(1, self.dry_adc - self.wet_adc)
        pct = (self.dry_adc - raw) * 100 / span
        return max(0, min(100, round(pct, 1)))

