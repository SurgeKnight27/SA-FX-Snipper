# ============================================
# Surge-Sniper
# Market Hunter Scanner v7.1
# LOCAL M15 CANDLE ANALYSIS
# MT5API LIVE QUOTE ENGINE
# STRICT SIGNAL GATE
# ============================================

from MarketHunter.signal_engine import SignalEngine
from MarketHunter.indicators import Indicators
from MarketHunter.data_stream import DataStream


class MarketHunter:

    def __init__(self):

        self.symbol = "BTCUSDm"
        self.timeframe = "M15"

        # Current live price
        self.price = None

        # Raw live-price history retained for diagnostics
        self.price_history = []

        # Completed M15 candles
        self.candle_history = []

        # Require enough completed M15 candles
        # before calculating M15 indicators.
        self.minimum_candles = 13
        self.minimum_samples = self.minimum_candles

        self.signal_engine = SignalEngine()
        self.indicators = Indicators()

        self.data_stream = DataStream(
            self.symbol
        )

    # ========================================
    # LOAD
    # ========================================

    def load(self):

        print(
            "📈 Loading Market Hunter..."
        )

        print(
            f"📡 Symbol    : {self.symbol}"
        )

        print(
            f"⏱️ Timeframe : {self.timeframe}"
        )

        if self.data_stream.connect():

            print(
                "✅ Market Hunter Loaded."
            )

            # Synchronize any persisted
            # completed M15 candles.
            self.update_candle_history()

            return True

        print(
            "❌ Market Hunter failed to connect."
        )

        return False

    # ========================================
    # MARKET
    # ========================================

    def set_market(
        self,
        symbol,
        timeframe
    ):

        self.symbol = symbol
        self.timeframe = timeframe

        self.price = None
        self.price_history = []
        self.candle_history = []

        self.data_stream = DataStream(
            symbol
        )

    # ========================================
    # LIVE PRICE UPDATE
    # ========================================

    def update_price(
        self,
        price
    ):

        if price is None:
            return

        try:

            self.price = float(
                price
            )

        except (
            TypeError,
            ValueError
        ):

            print(
                "⚠️ Invalid Market Hunter price."
            )

            return

        self.price_history.append(
            self.price
        )

        if len(
            self.price_history
        ) > 500:

            self.price_history.pop(0)

        print(
            "📊 Market Hunter Price Update: "
            f"{self.price}"
        )

    # ========================================
    # UPDATE CANDLE HISTORY
    # ========================================

    def update_candle_history(self):

        candles = (
            self.data_stream.get_candles()
        )

        if candles is None:
            return []

        if not isinstance(
            candles,
            list
        ):
            return []

        self.candle_history = list(
            candles
        )

        return self.candle_history

    # ========================================
    # GET LIVE MT5API PRICE
    # ========================================

    def update_from_broker(self):

        # Get the latest live quote through
        # the existing DataStream connection.
        price = (
            self.data_stream.get_live_price()
        )

        if price is None:
            return None

        # Keep MarketHunter's raw live price
        # history for diagnostics/dashboard use.
        self.update_price(
            price
        )

        # IMPORTANT:
        # Feed the live price into DataStream.
        #
        # DataStream.update_price() creates/
        # updates the local M15 candle using
        # the phone's real UTC timestamp when
        # no broker timestamp is supplied.
        candle_updated = (
            self.data_stream.update_price(
                price
            )
        )

        if not candle_updated:

            print(
                "⚠️ DataStream M15 candle "
                "was not updated."
            )

        # Refresh MarketHunter's completed
        # M15 candle history after the price
        # has been processed.
        self.update_candle_history()

        return price

    # ========================================
    # COLLECT LIVE SAMPLE
    # ========================================

    def collect_sample(self):

        return self.update_from_broker()

    # ========================================
    # SCAN MARKET
    # ========================================

    def scan_market(self):

        print(
            "🔍 Market Hunter scanning market..."
        )

        self.update_from_broker()

        return self.scan()

    # ========================================
    # GET CANDLE CLOSES
    # ========================================

    def get_candle_closes(self):

        closes = []

        for candle in self.candle_history:

            if not isinstance(
                candle,
                dict
            ):
                continue

            close = candle.get(
                "close"
            )

            if close is None:
                continue

            try:

                closes.append(
                    float(close)
                )

            except (
                TypeError,
                ValueError
            ):

                continue

        return closes

    # ========================================
    # ANALYSIS
    # ========================================

    def scan(self):

        print(
            f"🔍 Analyzing "
            f"{self.symbol} "
            f"({self.timeframe})..."
        )

        candle_count = len(
            self.candle_history
        )

        # ====================================
        # M15 CANDLE HISTORY CHECK
        # ====================================

        if candle_count < self.minimum_candles:

            print(
                "⏳ Building local M15 candle "
                "history..."
            )

            print(
                f"🕯️ Completed M15 Candles: "
                f"{candle_count}/"
                f"{self.minimum_candles}"
            )

            return {
                "signal": "HOLD",
                "confidence": 0,
                "trend": "WAITING",
                "price": self.price,
                "rsi": None,
                "ema_fast": None,
                "ema_slow": None,
                "ready": False,
                "samples": candle_count,
                "reason":
                    "Insufficient completed "
                    "M15 candles."
            }

        # ====================================
        # CANDLE CLOSE DATA
        # ====================================

        closes = (
            self.get_candle_closes()
        )

        if len(closes) < self.minimum_candles:

            print(
                "⏳ M15 candle data is "
                "not ready."
            )

            return {
                "signal": "HOLD",
                "confidence": 0,
                "trend": "WAITING",
                "price": self.price,
                "rsi": None,
                "ema_fast": None,
                "ema_slow": None,
                "ready": False,
                "samples": len(closes),
                "reason":
                    "Insufficient valid "
                    "M15 candle closes."
            }

        # ====================================
        # INDICATORS
        # ====================================

        ema_fast = (
            self.indicators.ema_fast(
                closes
            )
        )

        ema_slow = (
            self.indicators.ema_slow(
                closes
            )
        )

        rsi = (
            self.indicators.rsi(
                closes
            )
        )

        print(
            f"⚡ EMA(10) : {ema_fast}"
        )

        print(
            f"📈 EMA(20) : {ema_slow}"
        )

        print(
            f"📊 RSI(14) : {rsi}"
        )

        # ====================================
        # TREND
        # ====================================

        trend = "SIDEWAYS"

        if (
            ema_fast is not None
            and
            ema_slow is not None
        ):

            ema_gap = abs(
                ema_fast - ema_slow
            )

            # Require meaningful separation.
            if ema_gap >= 2.0:

                if ema_fast > ema_slow:

                    trend = "BULLISH"

                elif ema_fast < ema_slow:

                    trend = "BEARISH"

        # ====================================
        # M15 PRICE ACTION
        # ====================================

        bullish_price_confirmation = False
        bearish_price_confirmation = False

        if len(closes) >= 5:

            recent_closes = closes[-5:]

            upward_moves = 0
            downward_moves = 0

            for i in range(
                1,
                len(recent_closes)
            ):

                if (
                    recent_closes[i]
                    >
                    recent_closes[i - 1]
                ):

                    upward_moves += 1

                elif (
                    recent_closes[i]
                    <
                    recent_closes[i - 1]
                ):

                    downward_moves += 1

            recent_move = (
                recent_closes[-1]
                -
                recent_closes[0]
            )

            bullish_price_confirmation = (
                upward_moves >= 3
                and
                recent_move > 0
            )

            bearish_price_confirmation = (
                downward_moves >= 3
                and
                recent_move < 0
            )

            print(
                f"📌 Recent M15 Move : "
                f"{recent_move}"
            )

            print(
                "📈 Bullish M15 Price "
                "Confirmation : "
                f"{bullish_price_confirmation}"
            )

            print(
                "📉 Bearish M15 Price "
                "Confirmation : "
                f"{bearish_price_confirmation}"
            )

        else:

            print(
                "⏳ Waiting for M15 "
                "price-action confirmation..."
            )

        # ====================================
        # STRICT CONFIDENCE MODEL
        # ====================================

        confidence = 0

        # ====================================
        # BULLISH SETUP
        # ====================================

        if trend == "BULLISH":

            confidence = 55

            if rsi is not None:

                if 55 <= rsi <= 70:

                    confidence += 15

                elif 50 <= rsi < 55:

                    confidence += 5

                elif rsi > 70:

                    confidence -= 10

                elif rsi < 50:

                    confidence -= 15

        # ====================================
        # BEARISH SETUP
        # ====================================

        elif trend == "BEARISH":

            confidence = 55

            if rsi is not None:

                if 30 <= rsi <= 45:

                    confidence += 15

                elif 45 < rsi <= 50:

                    confidence += 5

                elif rsi < 30:

                    confidence -= 10

                elif rsi > 50:

                    confidence -= 15

        # ====================================
        # SIDEWAYS
        # ====================================

        else:

            confidence = 30

        confidence = max(
            0,
            min(
                confidence,
                100
            )
        )

        # ====================================
        # STRICT ENTRY FILTER
        # ====================================

        strict_signal = "HOLD"

        strict_reason = (
            "No sufficiently confirmed "
            "entry setup."
        )

        if (
            trend == "BULLISH"
            and
            rsi is not None
            and
            rsi >= 55
            and
            rsi < 70
            and
            bullish_price_confirmation
            and
            confidence >= 70
        ):

            strict_signal = "BUY"

            strict_reason = (
                "Bullish M15 EMA trend "
                "confirmed by RSI and "
                "price action."
            )

        elif (
            trend == "BEARISH"
            and
            rsi is not None
            and
            rsi <= 45
            and
            rsi > 30
            and
            bearish_price_confirmation
            and
            confidence >= 70
        ):

            strict_signal = "SELL"

            strict_reason = (
                "Bearish M15 EMA trend "
                "confirmed by RSI and "
                "price action."
            )

        else:

            if trend == "BULLISH":

                if (
                    rsi is not None
                    and
                    rsi > 70
                ):

                    strict_reason = (
                        f"BUY blocked: RSI "
                        f"{rsi:.2f} is overbought."
                    )

                elif not bullish_price_confirmation:

                    strict_reason = (
                        "BUY blocked: bullish "
                        "M15 price confirmation "
                        "is missing."
                    )

                elif confidence < 70:

                    strict_reason = (
                        "BUY blocked: confidence "
                        f"is only {confidence}%."
                    )

                else:

                    strict_reason = (
                        "Bullish trend detected, "
                        "but entry confirmation "
                        "is insufficient."
                    )

            elif trend == "BEARISH":

                if (
                    rsi is not None
                    and
                    rsi < 30
                ):

                    strict_reason = (
                        f"SELL blocked: RSI "
                        f"{rsi:.2f} is oversold."
                    )

                elif not bearish_price_confirmation:

                    strict_reason = (
                        "SELL blocked: bearish "
                        "M15 price confirmation "
                        "is missing."
                    )

                elif confidence < 70:

                    strict_reason = (
                        "SELL blocked: confidence "
                        f"is only {confidence}%."
                    )

                else:

                    strict_reason = (
                        "Bearish trend detected, "
                        "but entry confirmation "
                        "is insufficient."
                    )

            else:

                strict_reason = (
                    "Market structure is not "
                    "strong enough for entry."
                )

        # ====================================
        # SIGNAL ENGINE
        # ====================================

        decision = (
            self.signal_engine.decision(
                trend,
                confidence,
                rsi
            )
        )

        # ====================================
        # SAFETY OVERRIDE
        # ====================================

        # The strict scanner filter has final
        # authority.

        signal = strict_signal
        reason = strict_reason

        # ====================================
        # MARKET REPORT
        # ====================================

        print(
            "\n=================================================="
        )

        print(
            "📊 MARKET DECISION"
        )

        print(
            "=================================================="
        )

        print(
            f"Symbol       : {self.symbol}"
        )

        print(
            f"Timeframe    : {self.timeframe}"
        )

        print(
            f"Price        : {self.price}"
        )

        print(
            f"EMA Fast     : {ema_fast}"
        )

        print(
            f"EMA Slow     : {ema_slow}"
        )

        print(
            f"RSI          : {rsi}"
        )

        print(
            f"Trend        : {trend}"
        )

        print(
            f"Signal       : {signal}"
        )

        print(
            f"Confidence   : {confidence}%"
        )

        print(
            f"Reason       : {reason}"
        )

        print(
            f"Completed M15 Candles : "
            f"{candle_count}"
        )

        # ====================================
        # RETURN DECISION
        # ====================================

        return {
            "signal": signal,
            "confidence": confidence,
            "trend": trend,
            "price": self.price,
            "rsi": rsi,
            "ema_fast": ema_fast,
            "ema_slow": ema_slow,
            "ready": True,
            "samples": candle_count,
            "reason": reason
        }

    # ========================================
    # STATUS
    # ========================================

    def status(self):

        return {
            "symbol":
                self.symbol,

            "timeframe":
                self.timeframe,

            "price":
                self.price,

            "samples":
                len(
                    self.candle_history
                ),

            "live_price_samples":
                len(
                    self.price_history
                ),

            "broker":
                self.data_stream.status()
        }
