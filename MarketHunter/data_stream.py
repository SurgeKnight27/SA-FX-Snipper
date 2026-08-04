# ============================================
# Surge-Sniper
# Market Data Stream v3.0
# ============================================

class DataStream:

    def __init__(self):

        self.prices = [
            3365.2,
            3365.8,
            3366.4,
            3367.1,
            3367.9,
            3368.5,
            3369.0,
            3369.7,
            3370.2,
            3370.8,
            3371.4,
            3372.0,
            3372.7,
            3373.3,
            3373.9,
            3374.4,
            3375.0,
            3375.5,
            3376.1,
            3376.8,
            3377.2,
            3377.9,
            3378.3,
            3378.8,
            3379.2,
            3379.8,
            3380.3,
            3380.9,
            3381.4,
            3382.0
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
