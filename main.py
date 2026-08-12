# ============================================
# Surge-Sniper
# AI Trading Command Center v5.4
# MT5API DEMO / FAIL-SAFE EXECUTION
# ============================================

import time
import config

from AI.engine import AIEngine
from MarketHunter.scanner import MarketHunter
from RiskCommander.risk import RiskCommander

from Brokers.broker_manager_v2 import BrokerManager

from Logs.trade_logger import TradeLogger
from Logs.trade_history import TradeHistory


def startup():

    ai = AIEngine()
    hunter = MarketHunter()
    risk = RiskCommander()

    broker = BrokerManager()

    logger = TradeLogger()
    history = TradeHistory()

    # ========================================
    # MT5API CONNECTION
    # ========================================

    broker.select_broker("MT5API")

    if not broker.connect():

        print(
            "❌ MT5API connection failed."
        )

        return

    print(
        f"Broker Status : {broker.status()}"
    )

    symbol = "BTCUSDm"
    timeframe = "M15"

    print(
        "\n=================================================="
    )

    print(
        "        Surge-Sniper v5.4"
    )

    print(
        "      AI TRADING COMMAND CENTER"
    )

    print(
        "=================================================="
    )

    print(
        f"Broker    : MT5API"
    )

    print(
        f"Symbol    : {symbol}"
    )

    print(
        f"Timeframe : {timeframe}"
    )

    print(
        "Mode      : DEMO"
    )

    print(
        "=================================================="
    )

    # ========================================
    # ACCOUNT SNAPSHOT
    # ========================================

    account = broker.get_account_snapshot()

    if account:

        print(
            "\n💳 ACCOUNT SNAPSHOT"
        )

        print(
            f"Account ID : {account.get('id')}"
        )

        print(
            f"Label      : {account.get('name', account.get('label'))}"
        )

        print(
            f"Server     : {account.get('server')}"
        )

        print(
            f"Mode       : {account.get('mode')}"
        )

        print(
            f"Leverage   : {account.get('leverage')}"
        )

        print(
            f"Balance    : {account.get('balance')}"
        )

        print(
            f"Equity     : {account.get('equity')}"
        )

    else:

        print(
            "⚠️ Account snapshot unavailable."
        )

    # ========================================
    # EXISTING EXPOSURE
    # ========================================

    existing_positions = broker.get_positions()

    # ----------------------------------------
    # FAIL-SAFE:
    # None means UNKNOWN, NOT ZERO POSITIONS.
    # ----------------------------------------

    if existing_positions is None:

        print(
            "\n🛡️ EXISTING EXPOSURE"
        )

        print(
            "⚠️ Position state UNKNOWN."
        )

        print(
            "🚫 New automatic entries are LOCKED."
        )

        print(
            "Reason: MT5API position state "
            "could not be verified."
        )

        exposure_lock = True

        symbol_positions = []

        total_volume = 0.0

    else:

        symbol_positions = [
            position
            for position in existing_positions
            if position.get("symbol") == symbol
        ]

        total_volume = sum(
            float(
                position.get(
                    "volume",
                    0
                )
            )
            for position in symbol_positions
        )

        print(
            "\n🛡️ EXISTING EXPOSURE"
        )

        print(
            f"Open {symbol} positions : "
            f"{len(symbol_positions)}"
        )

        print(
            f"Total volume            : "
            f"{total_volume}"
        )

        if symbol_positions:

            print(
                f"\n⚠️ EXISTING {symbol} "
                "EXPOSURE DETECTED"
            )

            print(
                f"🚫 New automatic {symbol} "
                "entries are LOCKED."
            )

            print(
                "Existing positions will "
                "NOT be modified."
            )

            exposure_lock = True

        else:

            print(
                f"✅ No existing {symbol} exposure."
            )

            exposure_lock = False

    # ========================================
    # MARKET LOOP
    # ========================================

    cycles = 20

    for cycle in range(
        1,
        cycles + 1
    ):

        print(
            "\n=================================================="
        )

        print(
            f"🔄 MARKET CYCLE {cycle}/{cycles}"
        )

        print(
            "=================================================="
        )

        # ====================================
        # MARKET SCAN
        # ====================================

        result = hunter.scan_market()

        if not result:

            print(
                "⚠️ Market Hunter returned no result."
            )

            time.sleep(2)

            continue

        signal = result.get(
            "signal",
            "HOLD"
        )

        confidence = result.get(
            "confidence",
            0
        )

        samples = result.get(
            "samples",
            len(
                hunter.price_history
            )
        )

        print(
            "\n🎯 MARKET ANALYSIS"
        )

        print(
            f"Signal     : {signal}"
        )

        print(
            f"Confidence : {confidence}%"
        )

        print(
            f"Samples    : "
            f"{samples}/{hunter.minimum_samples}"
        )

        # ====================================
        # MARKET NOT READY
        # ====================================

        if not result.get(
            "ready",
            False
        ):

            print(
                "⏳ MarketHunter is still "
                "collecting live data."
            )

            time.sleep(2)

            continue

        # ====================================
        # HOLD
        # ====================================

        if signal == "HOLD":

            print(
                "⏸ No trade signal."
            )

            time.sleep(2)

            continue

        # ====================================
        # CONFIDENCE CHECK
        # ====================================

        if confidence < 70:

            print(
                f"⏸ Trade blocked: "
                f"confidence {confidence}% "
                "is below 70%."
            )

            time.sleep(2)

            continue

        # ====================================
        # EXPOSURE LOCK
        # ====================================

        if exposure_lock:

            print(
                f"⏸ Trade blocked: "
                f"{symbol} exposure is locked."
            )

            time.sleep(2)

            continue

        # ====================================
        # RISK / TARGETS
        # ====================================

        price = result.get(
            "price"
        )

        if price is None:

            print(
                "❌ Trade blocked: "
                "market price unavailable."
            )

            time.sleep(2)

            continue

        volume = 0.1

        # ------------------------------------
        # Simple demo targets
        # ------------------------------------

        if signal == "BUY":

            entry = float(price)

            stop_loss = (
                entry - 100
            )

            take_profit = (
                entry + 200
            )

        elif signal == "SELL":

            entry = float(price)

            stop_loss = (
                entry + 100
            )

            take_profit = (
                entry - 200
            )

        else:

            print(
                f"❌ Unsupported signal: "
                f"{signal}"
            )

            time.sleep(2)

            continue

        targets = {

            "entry": entry,

            "stop_loss": stop_loss,

            "take_profit": take_profit

        }

        # ====================================
        # TRADE PLAN
        # ====================================

        print(
            "\n⚡ MT5API EXECUTION"
        )

        print(
            f"Symbol     : {symbol}"
        )

        print(
            f"Direction  : {signal}"
        )

        print(
            f"Entry      : {targets['entry']}"
        )

        print(
            f"Volume     : {volume}"
        )

        print(
            f"Stop Loss  : "
            f"{targets['stop_loss']}"
        )

        print(
            f"Take Profit: "
            f"{targets['take_profit']}"
        )

        # ====================================
        # EXECUTION MODE GUARD
        # ====================================

        if str(config.MODE).upper() != "LIVE":
            print(
                f"🛡️ TRADE BLOCKED: "
                f"MODE={config.MODE}"
            )
            print(
                "ℹ️ Signal/targets calculated, "
                "but no order was sent to MT5API."
            )

            time.sleep(2)
            continue

        # ====================================
        # EXECUTE
        # ====================================

        trade_result = broker.execute_trade(
            signal,
            symbol,
            volume,
            targets["stop_loss"],
            targets["take_profit"]
        )

        # ====================================
        # EXECUTION RESULT
        # ====================================

        if trade_result:

            order_status = str(
                trade_result.get(
                    "status",
                    "unknown"
                )
            ).lower()

            order_id = trade_result.get(
                "id"
            )

            filled_volume = float(
                trade_result.get(
                    "filled_volume",
                    0
                ) or 0
            )

            print(
                "\n📋 MT5API EXECUTION STATE"
            )

            print(
                f"Order ID      : {order_id}"
            )

            print(
                f"API Status    : "
                f"{order_status.upper()}"
            )

            print(
                f"Filled Volume : "
                f"{filled_volume}"
            )

            # =================================
            # FILLED / OPEN
            # =================================

            if (
                order_status in (
                    "filled",
                    "open"
                )
                and filled_volume > 0
            ):

                print(
                    "🟢 MT5API POSITION FILLED"
                )

                logger.log_trade(
                    symbol,
                    signal,
                    targets["entry"],
                    filled_volume,
                    targets["stop_loss"],
                    targets["take_profit"],
                    status="OPEN"
                )

                exposure_lock = True

                total_volume += filled_volume

            # =================================
            # PENDING / UNCONFIRMED
            # =================================

            else:

                if order_status == "pending":

                    print(
                        "🟡 MT5API ORDER PENDING"
                    )

                else:

                    print(
                        "⚠️ MT5API ORDER STATE "
                        "NOT CONFIRMED AS FILLED."
                    )

                print(
                    "Order has NOT been recorded "
                    "as an OPEN trade."
                )

                print(
                    "🚫 New automatic entries "
                    "LOCKED."
                )

                exposure_lock = True

        else:

            print(
                "🔴 MT5API ORDER FAILED"
            )

            print(
                "No local trade recorded."
            )
        time.sleep(2)

    # ========================================
    # SESSION COMPLETE
    # ========================================

    print(
        "\n=================================================="
    )

    print(
        "📊 SESSION COMPLETE"
    )

    print(
        "=================================================="
    )

    print(
        "MODE   : DEMO"
    )

    print(
        "BROKER : MT5API"
    )

    print(
        f"SYMBOL : {symbol}"
    )

    print(
        "=================================================="
    )

    # ========================================
    # PERFORMANCE REPORT
    # ========================================

    print(
        "\n=================================================="
    )

    print(
        "📊 PERFORMANCE REPORT"
    )

    print(
        "=================================================="
    )

    print(
        f"Total Trades : "
        f"{logger.total_trades()}"
    )

    print(
        "Wins         : 0"
    )

    print(
        "Losses       : 0"
    )

    print(
        "Win Rate     : 0%"
    )

    print(
        "Net P/L      : 0"
    )

    print(
        "Best Trade   : 0"
    )

    print(
        "Worst Trade  : 0"
    )

    print(
        "Average Win  : 0"
    )

    print(
        "Average Loss : 0"
    )

    # ========================================
    # DISCONNECT
    # ========================================

    broker.disconnect()


if __name__ == "__main__":

    startup()
