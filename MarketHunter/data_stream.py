# ============================================
# Surge-Sniper
# MarketHunter Persistent Data Stream v6.0
# MT5API LIVE QUOTES + PERSISTENT LOCAL M15
# ============================================

import os
import json
import time
from datetime import datetime, timezone

from Brokers.MetaApi.metaapi import MetaApiBroker


class DataStream:

    def __init__(self, symbol="BTCUSDm"):

        self.symbol = symbol

        # ====================================
        # LIVE PRICE STATE
        # ====================================

        self.current_price = None
        self.price_history = []

        # ====================================
        # M15 ENGINE
        # ====================================

        self.timeframe = "M15"
        self.timeframe_seconds = 900

        self.candles = []
        self.current_candle = None

        # ====================================
        # PERSISTENCE
        # ====================================

        self.data_dir = os.path.expanduser(
            "~/Surge-Sniper/MarketHunter/data"
        )

        self.candle_file = os.path.join(
            self.data_dir,
            f"{self.symbol}_M15.json"
        )

        os.makedirs(
            self.data_dir,
            exist_ok=True
        )

        # ====================================
        # BROKER
        # ====================================

        self.broker = MetaApiBroker()

        # ====================================
        # LOAD HISTORY
        # ====================================

        self._load_history()

        # ========================================
        # AUTO CONNECT TO MT5API
        # ========================================
        self.connect()

    # ========================================
    # LOAD HISTORY
    # ========================================

    def _load_history(self):

        try:

            if not os.path.exists(
                self.candle_file
            ):

                print(
                    "📂 No saved M15 history found."
                )

                return

            with open(
                self.candle_file,
                "r"
            ) as f:

                data = json.load(f)

            if isinstance(data, dict):

                saved_candles = data.get(
                    "candles",
                    []
                )

                saved_current = data.get(
                    "current_candle"
                )

            elif isinstance(data, list):

                saved_candles = data
                saved_current = None

            else:

                print(
                    "⚠️ Saved M15 history invalid."
                )

                return

            valid = []

            for candle in saved_candles:

                if not isinstance(
                    candle,
                    dict
                ):

                    continue

                required = [
                    "time",
                    "open",
                    "high",
                    "low",
                    "close"
                ]

                if not all(
                    key in candle
                    for key in required
                ):

                    continue

                try:

                    valid.append({
                        "time": int(
                            candle["time"]
                        ),
                        "open": float(
                            candle["open"]
                        ),
                        "high": float(
                            candle["high"]
                        ),
                        "low": float(
                            candle["low"]
                        ),
                        "close": float(
                            candle["close"]
                        )
                    })

                except (
                    TypeError,
                    ValueError
                ):

                    continue

            self.candles = valid[-100:]

            if isinstance(
                saved_current,
                dict
            ):

                try:

                    self.current_candle = {
                        "time": int(
                            saved_current["time"]
                        ),
                        "open": float(
                            saved_current["open"]
                        ),
                        "high": float(
                            saved_current["high"]
                        ),
                        "low": float(
                            saved_current["low"]
                        ),
                        "close": float(
                            saved_current["close"]
                        )
                    }

                except (
                    KeyError,
                    TypeError,
                    ValueError
                ):

                    self.current_candle = None

            print(
                f"📂 Loaded {len(self.candles)} "
                "saved M15 candles."
            )

            if self.current_candle:

                print(
                    "🕯️ Restored current M15 candle "
                    f"@ {self.current_candle['close']}"
                )

        except Exception as e:

            print(
                f"⚠️ M15 history load error: {e}"
            )

    # ========================================
    # SAVE HISTORY
    # ========================================

    def _save_history(self):

        try:

            payload = {
                "symbol": self.symbol,
                "timeframe": self.timeframe,
                "updated_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "candles": self.candles[-100:],
                "current_candle": self.current_candle
            }

            with open(
                self.candle_file,
                "w"
            ) as f:

                json.dump(
                    payload,
                    f,
                    indent=2
                )

        except Exception as e:

            print(
                f"⚠️ M15 history save error: {e}"
            )

    # ========================================
    # CONNECT
    # ========================================

    def connect(self):

        print(
            "🔌 MarketHunter connecting to MT5API..."
        )

        ok = self.broker.connect()

        if ok:

            print(
                "✅ MarketHunter MT5API "
                "connection ONLINE"
            )

            print(
                f"📊 Persistent M15 candles: "
                f"{len(self.candles)}"
            )

        else:

            print(
                "❌ MarketHunter MT5API "
                "connection FAILED"
            )

        return ok

    # ========================================
    # DISCONNECT
    # ========================================

    # ========================================
    # STATUS
    # ========================================
    def status(self):
        return {
            "connected": self.broker.status(),
            "samples": len(self.candles),
            "price": self.current_price
        }

    def disconnect(self):

        try:

            self.broker.disconnect()

        except Exception:

            pass

    # ========================================
    # CANDLE START
    # ========================================

    def _candle_start(self, timestamp):

        return (
            int(
                timestamp
                // self.timeframe_seconds
            )
            * self.timeframe_seconds
        )

    # ========================================
    # PRINT CLOSED CANDLE
    # ========================================

    def _print_candle(self, candle):

        candle_time = datetime.fromtimestamp(
            candle["time"],
            tz=timezone.utc
        )

        print(
            "\n🕯️ M15 CANDLE CLOSED"
        )

        print(
            f"Time  : {candle_time}"
        )

        print(
            f"Open  : {candle['open']}"
        )

        print(
            f"High  : {candle['high']}"
        )

        print(
            f"Low   : {candle['low']}"
        )

        print(
            f"Close : {candle['close']}"
        )

    # ========================================
    # UPDATE M15 CANDLE
    # ========================================

    def _update_candle(
        self,
        price,
        timestamp
    ):

        try:

            price = float(price)
            timestamp = float(timestamp)

        except (
            TypeError,
            ValueError
        ):

            print(
                "⚠️ Invalid price/timestamp received."
            )

            return False

        candle_start = self._candle_start(
            timestamp
        )

        # ====================================
        # FIRST CANDLE
        # ====================================

        if self.current_candle is None:

            self.current_candle = {
                "time": candle_start,
                "open": price,
                "high": price,
                "low": price,
                "close": price
            }

            self.current_price = price

            self._save_history()

            print(
                "\n🕯️ M15 candle started"
            )

            print(
                "Start :",
                datetime.fromtimestamp(
                    candle_start,
                    tz=timezone.utc
                )
            )

            print(
                f"Open  : {price}"
            )

            return True

        current_start = int(
            self.current_candle["time"]
        )

        # ====================================
        # SAME M15 CANDLE
        # ====================================

        if candle_start == current_start:

            self.current_candle["high"] = max(
                float(
                    self.current_candle["high"]
                ),
                price
            )

            self.current_candle["low"] = min(
                float(
                    self.current_candle["low"]
                ),
                price
            )

            self.current_candle["close"] = price

            self.current_price = price

            self._save_history()

            return True

        # ====================================
        # NEW M15 CANDLE
        # ====================================

        if candle_start > current_start:

            completed = dict(
                self.current_candle
            )

            self.candles.append(
                completed
            )

            if len(self.candles) > 100:

                self.candles = (
                    self.candles[-100:]
                )

            self._print_candle(
                completed
            )

            print(
                f"📚 Completed M15 candles: "
                f"{len(self.candles)}"
            )

            self.current_candle = {
                "time": candle_start,
                "open": price,
                "high": price,
                "low": price,
                "close": price
            }

            self.current_price = price

            self._save_history()

            print(
                "\n🕯️ New M15 candle started"
            )

            print(
                "Start :",
                datetime.fromtimestamp(
                    candle_start,
                    tz=timezone.utc
                )
            )

            print(
                f"Open  : {price}"
            )

            return True

        # ====================================
        # OUT-OF-ORDER TIMESTAMP
        # ====================================

        print(
            "⚠️ Ignoring out-of-order "
            "M15 timestamp."
        )

        return False

    # ========================================
    # LIVE PRICE UPDATE
    # ========================================

    def update_price(
        self,
        price,
        timestamp=None
    ):

        try:

            price = float(price)

        except (
            TypeError,
            ValueError
        ):

            print(
                "⚠️ Invalid live price."
            )

            return False

        # IMPORTANT:
        # MT5API quote timestamp has been observed
        # as 1970-01-01. Therefore we use the
        # phone's actual UTC time.

        if timestamp is None:

            timestamp = datetime.now(
                timezone.utc
            ).timestamp()

        self.current_price = price

        self.price_history.append({
            "time": int(timestamp),
            "price": price
        })

        if len(
            self.price_history
        ) > 200:

            self.price_history = (
                self.price_history[-200:]
            )

        return self._update_candle(
            price,
            timestamp
        )

    # ========================================
    # GET LIVE BROKER PRICE
    # ========================================

    def get_live_price(self):
        """
        Compatibility wrapper for MarketHunter.
        Uses the existing fetch_live_price() implementation.
        """
        return self.fetch_live_price()

    def fetch_live_price(self):

        if not self.broker.connected:

            return None

        price = self.broker.get_price(
            self.symbol
        )

        if price is None:

            return None

        try:

            price = float(price)

        except (
            TypeError,
            ValueError
        ):

            return None

        return price

    # ========================================
    # PROCESS ONE LIVE QUOTE
    # ========================================

    def process_live_quote(self):

        price = self.fetch_live_price()

        if price is None:

            print(
                "⚠️ No live price received."
            )

            return False

        now = datetime.now(
            timezone.utc
        )

        print(
            f"📡 {self.symbol} "
            f"Bid/Price: {price} "
            f"UTC: {now.isoformat()}"
        )

        return self.update_price(
            price,
            now.timestamp()
        )

    # ========================================
    # GET COMPLETED CANDLES
    # ========================================

    def get_candles(self):
        """
        Return locally completed M15 candles.

        Historical MT5API /candles currently returns HTTP 500,
        so the live DataStream builds M15 candles locally from
        the working MT5API quotes endpoint.
        """

        return list(
            self.candles
        )

    # ========================================
    # GET CURRENT CANDLE
    # ========================================

    def get_current_candle(self):

        if self.current_candle is None:

            return None

        return dict(
            self.current_candle
        )

    # ========================================
    # GET ALL DATA
    # ========================================

    def get_data(self):

        return {
            "symbol": self.symbol,
            "timeframe": self.timeframe,
            "current_price": self.current_price,
            "candles": self.get_candles(),
            "current_candle":
                self.get_current_candle()
        }

    # ========================================
    # LIVE READ-ONLY TEST LOOP
    # ========================================

    def run_live_test(
        self,
        iterations=5,
        interval=5
    ):

        print(
            "========================================"
        )

        print(
            "MARKETHUNTER LIVE M15 TEST"
        )

        print(
            "========================================"
        )

        if not self.connect():

            print(
                "❌ Live test aborted."
            )

            return False

        try:

            for i in range(
                iterations
            ):

                print(
                    f"\n--- LIVE TICK "
                    f"{i + 1}/{iterations} ---"
                )

                self.process_live_quote()

                time.sleep(
                    interval
                )

        finally:

            self.disconnect()

        print(
            "\n========================================"
        )

        print(
            "LIVE M15 TEST COMPLETE"
        )

        print(
            "========================================"
        )

        return True
