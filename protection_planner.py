# ============================================
# Surge-Sniper
# Read-Only Protection Planner v1.0
#
# SAFETY:
# - READ-ONLY
# - Does NOT modify positions
# - Does NOT close positions
# - Does NOT place orders
# - Does NOT send PATCH/POST requests
# ============================================

from Brokers.MetaApi.metaapi import MetaApiBroker


def safe_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def fmt(value):
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def main():

    print("=" * 64)
    print("SURGE-SNIPER READ-ONLY PROTECTION PLANNER")
    print("=" * 64)

    broker = MetaApiBroker()

    # ========================================
    # CONNECT
    # ========================================

    print("\n🔌 Connecting to MT5API...")

    if not broker.connect():
        print("❌ MT5API connection failed.")
        return

    print("✅ MT5API connected.")

    try:

        # ====================================
        # ACCOUNT
        # ====================================

        account = broker.get_account_snapshot()

        print("\n" + "=" * 64)
        print("ACCOUNT SNAPSHOT")
        print("=" * 64)

        if account is None:
            print("⚠️ Account state unavailable.")
        else:
            for key in (
                "id",
                "label",
                "status",
                "mode",
                "balance",
                "equity",
                "free_margin",
                "margin",
                "margin_level",
                "leverage",
            ):
                if key in account:
                    print(f"{key:15}: {account[key]}")

        # ====================================
        # CURRENT PRICE
        # ====================================

        price = broker.get_price("BTCUSDm")

        print("\n" + "=" * 64)
        print("CURRENT MARKET PRICE")
        print("=" * 64)

        print(
            "BTCUSDm price  : "
            f"{fmt(price)}"
        )

        if price is None:
            print(
                "⚠️ Current price unavailable."
            )

        # ====================================
        # POSITIONS
        # ====================================

        positions = broker.get_positions()

        print("\n" + "=" * 64)
        print("POSITION INVENTORY")
        print("=" * 64)

        if positions is None:
            print(
                "❌ POSITION STATE UNKNOWN."
            )
            print(
                "No protection plan will be generated."
            )
            return

        print(
            f"Open positions : "
            f"{len(positions)}"
        )

        if not positions:
            print(
                "No open positions."
            )
            return

        # ====================================
        # AGGREGATE EXPOSURE
        # ====================================

        total_volume = 0.0
        buy_volume = 0.0
        sell_volume = 0.0
        total_profit = 0.0

        for position in positions:

            volume = safe_float(
                position.get("volume")
            )

            profit = safe_float(
                position.get("profit")
            )

            side = str(
                position.get("side", "")
            ).upper()

            total_volume += volume
            total_profit += profit

            if side == "BUY":
                buy_volume += volume

            elif side == "SELL":
                sell_volume += volume

        print("\n" + "=" * 64)
        print("AGGREGATE EXPOSURE")
        print("=" * 64)

        print(
            f"Total volume   : "
            f"{fmt(total_volume)}"
        )

        print(
            f"BUY volume     : "
            f"{fmt(buy_volume)}"
        )

        print(
            f"SELL volume    : "
            f"{fmt(sell_volume)}"
        )

        print(
            f"Floating P/L   : "
            f"{fmt(total_profit)}"
        )

        # ====================================
        # PROTECTION PLAN
        # ====================================

        print("\n" + "=" * 64)
        print("PROPOSED PROTECTION PLAN")
        print("=" * 64)

        print(
            "\n⚠️ IMPORTANT:"
        )

        print(
            "This section calculates STATUS ONLY."
        )

        print(
            "No SL/TP modification will be sent."
        )

        print(
            "No position will be closed."
        )

        print(
            "No order will be created."
        )

        # ====================================
        # POSITION-BY-POSITION PLAN
        # ====================================

        for index, position in enumerate(
            positions,
            1
        ):

            ticket = position.get(
                "ticket",
                position.get("id", "UNKNOWN")
            )

            symbol = position.get(
                "symbol",
                "UNKNOWN"
            )

            side = str(
                position.get(
                    "side",
                    "UNKNOWN"
                )
            ).upper()

            volume = safe_float(
                position.get("volume")
            )

            open_price = position.get(
                "open_price"
            )

            stop_loss = position.get(
                "stop_loss"
            )

            take_profit = position.get(
                "take_profit"
            )

            print(
                "\n" + "-" * 64
            )

            print(
                f"POSITION {index}"
            )

            print(
                f"Ticket       : {ticket}"
            )

            print(
                f"Symbol       : {symbol}"
            )

            print(
                f"Side         : {side}"
            )

            print(
                f"Volume       : {fmt(volume)}"
            )

            print(
                f"Open Price   : {open_price}"
            )

            print(
                f"Current Price: {fmt(price)}"
            )

            print(
                f"Current SL   : "
                f"{stop_loss if stop_loss is not None else 'NONE'}"
            )

            print(
                f"Current TP   : "
                f"{take_profit if take_profit is not None else 'NONE'}"
            )

            # ================================
            # MANAGEMENT STATUS
            # ================================

            if stop_loss is None:

                print(
                    "Protection   : ⚠️ SL REQUIRED"
                )

                print(
                    "Proposed     : "
                    "REVIEW BEFORE MODIFYING"
                )

            else:

                print(
                    "Protection   : 🟢 SL PRESENT"
                )

                print(
                    "Proposed     : "
                    "NO SL CHANGE"
                )

            if take_profit is None:

                print(
                    "TP status    : ⚠️ TP MISSING"
                )

            else:

                print(
                    "TP status    : 🟢 TP PRESENT"
                )

        # ====================================
        # SUMMARY
        # ====================================

        without_sl = sum(
            1
            for p in positions
            if p.get("stop_loss") is None
        )

        without_tp = sum(
            1
            for p in positions
            if p.get("take_profit") is None
        )

        print("\n" + "=" * 64)
        print("PROTECTION SUMMARY")
        print("=" * 64)

        print(
            f"Positions          : {len(positions)}"
        )

        print(
            f"Without Stop Loss  : {without_sl}"
        )

        print(
            f"Without Take Profit: {without_tp}"
        )

        print(
            f"Total BUY exposure : {fmt(buy_volume)}"
        )

        print(
            f"Total SELL exposure: {fmt(sell_volume)}"
        )

        print(
            f"Floating P/L       : {fmt(total_profit)}"
        )

        # ====================================
        # FINAL SAFETY BARRIER
        # ====================================

        print("\n" + "=" * 64)
        print("SAFETY BARRIER")
        print("=" * 64)

        print(
            "🟢 READ-ONLY PLAN COMPLETE"
        )

        print(
            "🟢 NO PATCH REQUEST SENT"
        )

        print(
            "🟢 NO CLOSE REQUEST SENT"
        )

        print(
            "🟢 NO ORDER REQUEST SENT"
        )

        print(
            "🟢 NO POSITION WAS MODIFIED"
        )

    finally:

        broker.disconnect()

        print("\n" + "=" * 64)
        print("MT5API DISCONNECTED")
        print("=" * 64)


if __name__ == "__main__":
    main()
