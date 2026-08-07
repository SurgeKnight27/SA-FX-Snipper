# ============================================
# Surge-Sniper
# Market Hunter Scanner v3.8.0
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

        if price is None:
            return

        self.price = price
        self.price_history.append(price)

        if len(self.price_history) > 100:
            self.price_history.pop(0)

        print(f"📊 Market Hunter Price Update: {price}")

    def scan_market(self):
        print("🔍 Market Hunter scanning market...")
        return self.scan()

    def scan(self):

        # Only use DataStream if broker has not supplied prices yet
        if len(self.price_history) < 20:

            if self.price is None:
                self.price_history = self.data_stream.get_prices().copy()

            else:
                while len(self.price_history) < 20:
                    self.price_history.append(self.price)


        if self.price is None:
            new_price = self.data_stream.next_price()
        else:
            new_price = self.price


        self.price = new_price
        self.price_history.append(new_price)

        if len(self.price_history) > 100:
            self.price_history.pop(0)


        ema_fast = self.indicators.ema_fast(self.price_history)
        ema_slow = self.indicators.ema_slow(self.price_history)
        rsi = self.indicators.rsi(self.price_history)


        print(f"🔍 Analyzing {self.symbol} ({self.timeframe})...")
        print(f"⚡ EMA(10)    : {ema_fast}")
        print(f"📈 EMA(20)    : {ema_slow}")
        print(f"📊 RSI(14)    : {rsi}")


        trend = "SIDEWAYS"


        if ema_fast and ema_slow:

            if ema_fast > ema_slow:
                trend = "BULLISH"

            elif ema_fast < ema_slow:
                trend = "BEARISH"


        confidence = 50


        if trend != "SIDEWAYS":
            confidence += 20


        if rsi is not None and (rsi > 60 or rsi < 40):
            confidence += 15


        confidence = min(confidence, 100)


        signal = self.signal_engine.generate(
            trend,
            confidence
        )


        print(f"📈 Trend      : {trend}")
        print(f"🎯 Signal     : {signal}")
        print(f"📊 Confidence : {confidence}%")
        print(f"📚 Price Samples : {len(self.price_history)}")


        print("\n==================================================")
        print("📊 DECISION ENGINE")
        print("==================================================")


        print(f"Trend         : {trend}")
        print(f"Signal        : {signal}")
        print(f"Confidence    : {confidence}%")


        print("\n🧠 Reason:")


        reasons = []


        if signal == "BUY":
            reasons.append("📈 EMA fast above EMA slow")
            reasons.append("🟢 Momentum supports buyers")


        elif signal == "SELL":
            reasons.append("📉 EMA fast below EMA slow")
            reasons.append("🔴 Momentum supports sellers")


        for reason in reasons:
            print(reason)


        return {
            "signal": signal,
            "confidence": confidence,
            "trend": trend,
            "price": self.price
        }
