# ============================================
# Surge-Sniper
# Market Hunter Scanner v3.7.1
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

        if len(self.price_history) < 20:
            self.price_history = self.data_stream.get_prices().copy()

        new_price = self.data_stream.next_price()

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

        if ema_fast is not None and ema_slow is not None:
            if ema_fast > ema_slow:
                trend = "BULLISH"
            elif ema_fast < ema_slow:
                trend = "BEARISH"

        confidence = 50

        if trend != "SIDEWAYS":
            confidence += 20

        if rsi is not None:
            if rsi > 60 or rsi < 40:
                confidence += 15

        confidence = min(confidence, 100)

        signal = self.signal_engine.generate(trend, confidence)

        print(f"📈 Trend      : {trend}")
        print(f"🎯 Signal     : {signal}")
        print(f"📊 Confidence : {confidence}%")
        print(f"📚 Price Samples : {len(self.price_history)}")

        print("\n==================================================")
        print("📊 DECISION ENGINE")
        print("==================================================")

        if ema_fast is not None and ema_slow is not None:
            ema_cross = "Bullish ✅" if ema_fast > ema_slow else "Bearish 🔻"
        else:
            ema_cross = "Waiting..."

        print(f"EMA Cross     : {ema_cross}")

        if rsi is not None:
            if rsi < 30:
                rsi_status = "Oversold ✅"
            elif rsi > 70:
                rsi_status = "Overbought 🔴"
            else:
                rsi_status = "Neutral 🟡"
        else:
            rsi_status = "Waiting..."

        print(f"RSI Status    : {rsi_status}")
        print(f"Trend         : {trend}")
        print(f"Signal        : {signal}")
        print(f"Confidence    : {confidence}%")

        print("\n🧠 Reason:")

        if signal == "BUY":
            print("📈 EMA fast above EMA slow")
            print("🟢 Momentum supports buyers")
           
