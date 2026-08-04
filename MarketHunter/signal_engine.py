# ============================================
# Surge-Sniper
# Signal Engine v1.0
# ============================================

class SignalEngine:

    def generate(self, trend, confidence):
        if trend == "BULLISH" and confidence >= 80:
            return "BUY"

        if trend == "BEARISH" and confidence >= 80:
            return "SELL"

        return "HOLD"
