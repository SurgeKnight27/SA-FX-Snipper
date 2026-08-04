# ============================================
# Surge-Sniper
# Technical Indicators v1.0
# ============================================

class Indicators:

    def __init__(self):
        pass

    def ema(self, prices):
        if not prices:
            return None

        return sum(prices) / len(prices)

    def rsi(self, prices):
        if len(prices) < 14:
            return None

        gains = []
        losses = []

        for i in range(1, len(prices)):
            change = prices[i] - prices[i - 1]

            if change > 0:
                gains.append(change)
            else:
                losses.append(abs(change))

        avg_gain = sum(gains) / max(len(gains), 1)
        avg_loss = sum(losses) / max(len(losses), 1)

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss

        return 100 - (100 / (1 + rs))
