# ============================================
# Surge-Sniper
# Market Hunter Indicators v1.0
# ============================================


class Indicators:

    def __init__(self):
        pass

    def ema(self, prices, period=10):
        if len(prices) < period:
            return None

        prices = prices[-period:]

        return sum(prices) / period


    def rsi(self, prices, period=14):
        if len(prices) <= period:
            return None

        gains = 0
        losses = 0

        for i in range(1, period + 1):
            change = prices[-i] - prices[-i-1]

            if change > 0:
                gains += change
            else:
                losses += abs(change)

        if losses == 0:
            return 100

        rs = gains / losses

        return round(100 - (100 / (1 + rs)), 2)
