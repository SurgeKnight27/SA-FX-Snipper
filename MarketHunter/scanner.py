# ============================================
# Surge-Sniper
# Market Hunter Scanner v4.0
# LIVE MARKET HISTORY
# ============================================

from MarketHunter.signal_engine import SignalEngine
from MarketHunter.indicators import Indicators


class MarketHunter:

    def __init__(self):

        self.symbol = "XAUUSD"
        self.timeframe = "M15"

        self.price = None
        self.price_history = []

        self.signal_engine = SignalEngine()
        self.indicators = Indicators()


    # ========================================
    # LOAD
    # ========================================

    def load(self):

        print("📈 Loading Market Hunter...")
        print("✅ Market Hunter Loaded.")


    # ========================================
    # MARKET
    # ========================================

    def set_market(self, symbol, timeframe):

        self.symbol = symbol
        self.timeframe = timeframe


    # ========================================
    # LIVE PRICE UPDATE
    # ========================================

    def update_price(self, price):

        if price is None:
            return

        self.price = float(price)

        self.price_history.append(self.price)

        if len(self.price_history) > 100:
            self.price_history.pop(0)

        print(
            f"📊 Market Hunter Price Update: "
            f"{self.price}"
        )


    # ========================================
    # SCAN
    # ========================================

    def scan_market(self):

        print("🔍 Market Hunter scanning market...")

        return self.scan()


    def scan(self):

        print(
            f"🔍 Analyzing "
            f"{self.symbol} ({self.timeframe})..."
        )


        sample_count = len(self.price_history)


        # ------------------------------------
        # REQUIRE REAL MARKET HISTORY
        # ------------------------------------

        if sample_count < 20:

            print(
                f"⏳ Collecting live market history..."
            )

            print(
                f"📚 Real Price Samples: "
                f"{sample_count}/20"
            )

            return {

                "signal": "HOLD",
                "confidence": 0,
                "trend": "WAITING",
                "price": self.price,
                "ready": False

            }


        # ------------------------------------
        # INDICATORS
        # ------------------------------------

        ema_fast = self.indicators.ema_fast(
            self.price_history
        )

        ema_slow = self.indicators.ema_slow(
            self.price_history
        )

        rsi = self.indicators.rsi(
            self.price_history
        )


        print(
            f"⚡ EMA(10)    : {ema_fast}"
        )

        print(
            f"📈 EMA(20)    : {ema_slow}"
        )

        print(
            f"📊 RSI(14)    : {rsi}"
        )


        # ------------------------------------
        # TREND
        # ------------------------------------

        trend = "SIDEWAYS"


        if ema_fast is not None and ema_slow is not None:

            if ema_fast > ema_slow:
                trend = "BULLISH"

            elif ema_fast < ema_slow:
                trend = "BEARISH"


        # ------------------------------------
        # CONFIDENCE
        # ------------------------------------

        confidence = 50


        if trend != "SIDEWAYS":
            confidence += 20


        if rsi is not None:

            if rsi > 60 or rsi < 40:
                confidence += 15


        confidence = min(confidence, 100)


        # ------------------------------------
        # SIGNAL
        # ------------------------------------

        signal = self.signal_engine.generate(
            trend,
            confidence
        )


        print(
            f"📈 Trend      : {trend}"
        )

        print(
            f"🎯 Signal     : {signal}"
        )

        print(
            f"📊 Confidence : {confidence}%"
        )

        print(
            f"📚 Price Samples : "
            f"{len(self.price_history)}"
        )


        # ------------------------------------
        # DECISION ENGINE
        # ------------------------------------

        print(
            "\n=================================================="
        )

        print("📊 DECISION ENGINE")

        print(
            "=================================================="
        )

        print(
            f"Trend         : {trend}"
        )

        print(
            f"Signal        : {signal}"
        )

        print(
            f"Confidence    : {confidence}%"
        )


        print("\n🧠 Reason:")


        reasons = []


        if signal == "BUY":

            reasons.append(
                "📈 EMA fast above EMA slow"
            )

            reasons.append(
                "🟢 Momentum supports buyers"
            )


        elif signal == "SELL":

            reasons.append(
                "📉 EMA fast below EMA slow"
            )

            reasons.append(
                "🔴 Momentum supports sellers"
            )


        else:

            reasons.append(
                "⏸️ No confirmed trading setup"
            )


        for reason in reasons:
            print(reason)


        return {

            "signal": signal,
            "confidence": confidence,
            "trend": trend,
            "price": self.price,
            "ready": True

        }







