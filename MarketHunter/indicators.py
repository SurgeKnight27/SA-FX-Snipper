# ============================================
# Surge-Sniper
# Indicator Engine v3.6.1
# ============================================

class Indicators:

    def ema(self, prices, period=10):

        if len(prices) < period:
            return None

        data = prices[-period:]

        return round(sum(data) / len(data), 2)

    def ema_fast(self, prices):
        return self.ema(prices, 10)

    def ema_slow(self, prices):
        return self.ema(prices, 20)

    def rsi(self, prices, period=14):

        if len(prices) < period + 1:
            return None

        gains = []
        losses = []

        for i in range(-period, 0):

            change = prices[i] - prices[i - 1]

            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        avg_gain = sum(gains) / period if gains else 0
        avg_loss = sum(losses) / period if losses else 0

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss

        return round(100 - (100 / (1 + rs)), 2)
