# ============================================
# Surge-Sniper
# Read-Only Position Auditor v1.0
#
# SAFETY:
# - GET requests only
# - Does NOT place orders
# - Does NOT modify positions
# - Does NOT close positions
# - Does NOT print API credentials
# ============================================

from collections import defaultdict

from Brokers.MetaApi.metaapi import MetaApiBroker


def money(value):
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def number(value):
    try:
        return f"{float(value):,.2f}"
    except (TypeError, ValueError):
        return "N/A"


def main():

    print("=" * 60)
    print("SURGE-SNIPER READ-ONLY POSITION AUDITOR")
    print("=" * 60)

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
        # READ POSITIONS
        # ====================================

        positions = broker.get_positions()

        if positions is None:
            print("\n❌ POSITION STATE UNKNOWN.")
            print("No management decision should be made.")
            return

        print(f"\n📊 OPEN POSITIONS: {len(positions)}")

        if not positions:
            print("No open positions reported by MT5API.")
            return

        # ====================================
        # SUMMARY VARIABLES
        # ====================================

        total_volume = 0.0
        total_profit = 0.0

        positions_without_sl = []
        positions_without_tp = []

        by_symbol = defaultdict(
            lambda: {
                "count": 0,
                "volume": 0.0,
                "profit": 0.0,
                "buy_volume": 0.0,
                "sell_volume": 0.0,
            }
        )

        # ====================================
        # POSITION REPORT
        # ====================================

        print("\n" + "=" * 60)
        print("POSITION DETAILS")
        print("=" * 60)

        for index, position in enumerate(positions, 1):

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

            volume_raw = position.get(
                "volume",
                0
            )

            profit_raw = position.get(
                "profit",
                0
            )

            try:
                volume = float(volume_raw or 0)
            except (TypeError, ValueError):
                volume = 0.0

            try:
                profit = float(profit_raw or 0)
            except (TypeError, ValueError):
                profit = 0.0

            stop_loss = position.get(
                "stop_loss"
            )

            take_profit = position.get(
                "take_profit"
            )

            total_volume += volume
            total_profit += profit

            # =================================
            # SYMBOL AGGREGATION
            # =================================

            group = by_symbol[symbol]

            group["count"] += 1
            group["volume"] += volume
            group["profit"] += profit

            if side == "BUY":
                group["buy_volume"] += volume

            elif side == "SELL":
                group["sell_volume"] += volume

            # =================================
            # RISK COVERAGE
            # =================================

            if stop_loss is None:
                positions_without_sl.append(ticket)

            if take_profit is None:
                positions_without_tp.append(ticket)

            # =================================
            # PRINT POSITION
            # =================================

            print("\n" + "-" * 60)

            print(f"POSITION {index}")
            print(f"Ticket       : {ticket}")
            print(f"Symbol       : {symbol}")
            print(f"Side         : {side}")
            print(f"Volume       : {number(volume)}")
            print(
                f"Open Price   : "
                f"{position.get('open_price', 'N/A')}"
            )
            print(
                f"Stop Loss    : "
                f"{stop_loss if stop_loss is not None else 'NONE'}"
            )
            print(
                f"Take Profit  : "
                f"{take_profit if take_profit is not None else 'NONE'}"
            )
            print(f"Floating P/L : {money(profit)}")

        # ====================================
        # SYMBOL EXPOSURE
        # ====================================

        print("\n" + "=" * 60)
        print("EXPOSURE BY SYMBOL")
        print("=" * 60)

        for symbol, group in by_symbol.items():

            print("\n" + "-" * 60)
            print(f"Symbol       : {symbol}")
            print(f"Positions    : {group['count']}")
            print(
                f"Total Volume : "
                f"{number(group['volume'])}"
            )
            print(
                f"BUY Volume   : "
                f"{number(group['buy_volume'])}"
            )
            print(
                f"SELL Volume  : "
                f"{number(group['sell_volume'])}"
            )
            print(
                f"Floating P/L : "
                f"{money(group['profit'])}"
            )

        # ====================================
        # OVERALL SUMMARY
        # ====================================

        print("\n" + "=" * 60)
        print("OVERALL EXPOSURE")
        print("=" * 60)

        print(f"Open Positions       : {len(positions)}")
        print(f"Total Volume         : {number(total_volume)}")
        print(f"Total Floating P/L   : {money(total_profit)}")

        # ====================================
        # PROTECTION AUDIT
        # ====================================

        print("\n" + "=" * 60)
        print("PROTECTION AUDIT")
        print("=" * 60)

        sl_count = (
            len(positions) -
            len(positions_without_sl)
        )

        tp_count = (
            len(positions) -
            len(positions_without_tp)
        )

        print(
            f"Positions WITH SL    : "
            f"{sl_count}/{len(positions)}"
        )

        print(
            f"Positions WITHOUT SL : "
            f"{len(positions_without_sl)}/{len(positions)}"
        )

        print(
            f"Positions WITH TP    : "
            f"{tp_count}/{len(positions)}"
        )

        print(
            f"Positions WITHOUT TP : "
            f"{len(positions_without_tp)}/{len(positions)}"
        )

        if positions_without_sl:

            print("\n⚠️ POSITIONS WITHOUT STOP LOSS:")

            for ticket in positions_without_sl:
                print(f"  - {ticket}")

        if positions_without_tp:

            print("\nℹ️ POSITIONS WITHOUT TAKE PROFIT:")

            for ticket in positions_without_tp:
                print(f"  - {ticket}")

        # ====================================
        # FINAL SAFETY STATUS
        # ====================================

        print("\n" + "=" * 60)
        print("AUDIT STATUS")
        print("=" * 60)

        print("🟢 READ-ONLY AUDIT COMPLETE")
        print("🟢 NO ORDER WAS PLACED")
        print("🟢 NO POSITION WAS MODIFIED")
        print("🟢 NO POSITION WAS CLOSED")

    finally:

        broker.disconnect()

        print("\n" + "=" * 60)
        print("MT5API DISCONNECTED")
        print("=" * 60)


if __name__ == "__main__":
    main()
