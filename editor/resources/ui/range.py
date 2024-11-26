from resources.ui.ticker import Ticker

class Range(Ticker):
    def __init__(self, x, y, width, height, border_radius, font_size, init_value, min_val, max_val, increment_value=1):
        super().__init__(x, y, width, height, border_radius, font_size, init_value, increment_value)

        self.min_val = min_val
        self.max_val = max_val

    def update(self):
        super().update()

        if self.value > self.max_val:
            self.value = self.max_val
        if self.value < self.min_val:
            self.value = self.min_val