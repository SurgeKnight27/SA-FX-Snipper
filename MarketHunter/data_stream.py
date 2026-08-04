# ============================================
# Surge-Sniper
# Market Data Stream v2.0
# ============================================

class DataStream:

    def __init__(self):
        self.prices = [
            3370.5,
            3371.8,
            3372.9,
            3373.6,
            3374.2,
            3375.5,
            3376.1,
            3375.8,
            3376.9,
            3377.3,
            3378.0,
            3378.7,
            3379.1,
            3380.0,
            3381.2,
        ]

        self.index = 0

    def get_prices(self):
        return self.prices.copy()

    def next_price(self):

        price = self.prices[self.index]

        self.index += 1

        if self.index >= len(self.prices):
            self.index = 0

        return price
