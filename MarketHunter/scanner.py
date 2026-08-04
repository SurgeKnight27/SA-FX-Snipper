# ============================================
# Surge-Sniper
# Market Hunter Scanner v2.1
# ============================================

from MarketHunter.signal_engine import SignalEngine
class MarketHunter:

    def __init__(self):
        self.symbol = "XAUUSD"
        self.timeframe = "M15"
        self.price = None
        self.price_history = []
        self.signal_engine = SignalEngine()
        print("📈 Loading Market Hunter...")
        print("✅ Market Hunter Loaded.")

    def set_market(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe

    def update_price(self, price):
        self.price = price
        print(f"📊 Market Hunter Price Update: {price}")

    def scan_market(self):
        print("🔍 Market Hunter scanning market...")
        return self.scan()

    def scan(self):
        print(f"🔍 Analyzing {self.symbol} ({self.timeframe})...")

        trend = "SIDEWAYS"

        if self.price is not None:
            if self.price > 3350:
                trend = "BULLISH"
            elif self.price < 3300:
                trend = "BEARISH"

        confidence = 50

        if trend == "BULLISH":
            confidence += 25
        elif trend == "BEARISH":
            confidence += 25

        if self.price is not None and self.price > 3370:
            confidence += 10

        confidence = min(confidence, 100)

        signal = self.signal_engine.generate(trend, confidence)

        print(f"📈 Trend      : {trend}")
        print(f"🎯 Signal     : {signal}")
        print(f"📊 Confidence : {confidence}%")

        return {
            "trend": trend,
            "signal": signal,
            "confidence": confidence,
        }

    def status(self):
        return "ONLINE"
