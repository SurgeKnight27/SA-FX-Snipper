# ============================================
# Surge-Sniper
# Market Hunter Scanner v3.5.2
# ============================================

from MarketHunter.signal_engine import SignalEngine
from MarketHunter.indicators import Indicators
from MarketHunter.data_stream import DataStream


class MarketHunter:

    def __init__(self):
        self.symbol = "XAUUSD"
        self.timeframe = "M15"

        self.price = None
        self.price_history = []

        self.signal_engine = SignalEngine()
        self.indicators = Indicators()
        self.data_stream = DataStream()

    def load(self):
        print("📈 Loading Market Hunter...")
        print("✅ Market Hunter Loaded.")

    def set_market(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe

    def update_price(self, price):
        self.price = price

        self.price_history.append(price)

        if len(self.price_history) > 100:
            self.price_history.pop(0)

        print(f"📊 Market Hunter Price Update: {price}")

    def scan_market(self):
        print("🔍 Market Hunter scanning market...")
        return self.scan()

    def scan(self):

        # Build initial history
        if len(self.price_history) < 15:
            self.price_history = self.data_stream.get_prices().copy()

        # Simulate arrival of the next market price
        new_price = self.data_stream.next_price()
        self.price = new_price

        self.price_history.append(new_price)

        if len(self.price_history) > 100:
            self.price_history.pop(0)

        print(f"🔍 Analyzing {self.symbol} ({self.timeframe})...")

        ema = self.indicators.ema(self.price_history)
        rsi = self.indicators.rsi(self.price_history)

        print(f"📊 EMA        : {round(ema,2) if ema is not None else None}")
        print(f"⚡ RSI        : {rsi}")

        trend = "SIDEWAYS"

        if ema is not None:
            if self.price > ema:
                trend = "BULLISH"
            elif self.price < ema:
                trend = "BEARISH"

        confidence = 50

        if trend != "SIDEWAYS":
            confidence += 20

        if rsi is not None:
            if rsi > 55:
                confidence += 15
            elif rsi < 45:
                confidence += 15

        confidence = min(confidence, 100)

        signal = self.signal_engine.generate(trend, confidence)

        print(f"📈 Trend      : {trend}")
        print(f"🎯 Signal     : {signal}")
        print(f"📊 Confidence : {confidence}%")
        print(f"📚 Price Samples : {len(self.price_history)}")

        return {
            "trend": trend,
            "signal": signal,
            "confidence": confidence,
            "ema": ema,
            "rsi": rsi,
            "samples": len(self.price_history),
            "price": self.price,
        }

    def status(self):
        return "ONLINE"
