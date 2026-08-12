import math

from Brokers.MetaApi.metaapi import MetaApiBroker


# ============================================================
# SURGE-SNIPER
# READ-ONLY POSITION PROTECTION PLANNER
# ============================================================
#
# SAFETY:
# - Does NOT modify positions
# - Does NOT close positions
# - Does NOT place orders
# - Does NOT send PATCH requests
#
# It calculates candidate protection levels only.
# ============================================================


RISK_LEVELS = (
    0.01,
    0.02,
    0.05,
    0.10,
)


def money(value):
    if value is None:
        return "N/A"

    return f"${float(value):,.2f}"


def price(value):
    if value is None:
        return "N/A"

    return f"{float(value):,.2f}"


def main():

    print("=" * 64)
    print("SURGE-SNIPER READ-ONLY PROTECTION PLANNER")
    print("=" * 64)

    broker = MetaApiBroker()

    if not broker.connect():
        raise SystemExit(
            "❌ MT5API connection failed."
        )

    try:

        # ====================================================
        # ACCOUNT
        # ====================================================

        account = broker.get_account_snapshot()

        if not account:
            raise SystemExit(
                "❌ Account state unavailable."
            )

        equity = account.get("equity")

        if equity is None:
            raise SystemExit(
                "❌ Equity unavailable."
            )

        equity = float(equity)

        # ====================================================
        # POSITIONS
        # ====================================================

        positions = broker.get_positions()

        if positions is None:
            raise SystemExit(
                "❌ Position state UNKNOWN."
            )

        if not positions:
            print("\n🟢 No open positions.")
            return

        print(
            f"\n📊 OPEN POSITIONS: {len(positions)}"
        )

        # ====================================================
        # EXPOSURE
        # ====================================================

        total_buy = 0.0
        total_sell = 0.0

        weighted_entry_value = 0.0
        total_volume = 0.0

        symbols = set()

        for p in positions:

            symbol = p.get("symbol")
            side = str(
                p.get("side", "")
            ).lower()

            volume = float(
                p.get("volume", 0) or 0
            )

            entry = p.get("open_price")

            if entry is None:
                continue

            entry = float(entry)

            symbols.add(symbol)

            total_volume += volume
            weighted_entry_value += (
                entry * volume
            )

            if side == "buy":
                total_buy += volume

            elif side == "sell":
                total_sell += volume

        if total_volume <= 0:
            raise SystemExit(
                "❌ No measurable position volume."
            )

        weighted_entry = (
            weighted_entry_value
            / total_volume
        )

        # ====================================================
        # CURRENT PRICE
        # ====================================================

        if len(symbols) != 1:

            print(
                "\n⚠️ Multiple symbols detected:"
            )

            for symbol in sorted(
                str(s) for s in symbols
            ):
                print(
                    f"  - {symbol}"
                )

            print(
                "\n❌ Planner currently requires "
                "one symbol."
            )

            return

        symbol = next(iter(symbols))

        current_price = broker.get_price(
            symbol
        )

        if current_price is None:
            raise SystemExit(
                "❌ Current price unavailable."
            )

        current_price = float(
            current_price
        )

        # ====================================================
        # HEADER
        # ====================================================

        print("\n" + "=" * 64)
        print("CURRENT EXPOSURE")
        print("=" * 64)

        print(
            f"Symbol              : {symbol}"
        )

        print(
            f"Positions           : {len(positions)}"
        )

        print(
            f"Total volume        : {total_volume:.2f}"
        )

        print(
            f"BUY volume          : {total_buy:.2f}"
        )

        print(
            f"SELL volume         : {total_sell:.2f}"
        )

        print(
            f"Weighted entry      : "
            f"{price(weighted_entry)}"
        )

        print(
            f"Current price       : "
            f"{price(current_price)}"
        )

        print(
            f"Account equity      : "
            f"{money(equity)}"
        )

        # ====================================================
        # CURRENT FLOATING P/L
        # ====================================================

        floating = 0.0

        for p in positions:

            try:
                floating += float(
                    p.get("profit", 0) or 0
                )
            except (
                TypeError,
                ValueError
            ):
                pass

        print(
            f"Floating P/L        : "
            f"{money(floating)}"
        )

        # ====================================================
        # POSITION DIRECTION
        # ====================================================

        print("\n" + "=" * 64)
        print("POSITION DIRECTION")
        print("=" * 64)

        if total_buy > 0 and total_sell == 0:

            direction = "BUY"

            print(
                "Direction           : BUY"
            )

        elif total_sell > 0 and total_buy == 0:

            direction = "SELL"

            print(
                "Direction           : SELL"
            )

        else:

            direction = "MIXED"

            print(
                "Direction           : MIXED"
            )

        # ====================================================
        # PROTECTION PLANNING
        # ====================================================

        print("\n" + "=" * 64)
        print("CANDIDATE PROTECTION LEVELS")
        print("=" * 64)

        print(
            "\nThese are CALCULATED LEVELS ONLY."
        )

        print(
            "No position will be modified."
        )

        print(
            "No PATCH request will be sent."
        )

        print(
            "The calculation represents "
            "ADDITIONAL risk from the "
            "current market price."
        )

        print(
            "\nRisk budget | $ Risk | "
            "Price distance | Candidate level"
        )

        print("-" * 64)

        if direction == "BUY":

            usable_volume = total_buy

        elif direction == "SELL":

            usable_volume = total_sell

        else:

            usable_volume = 0.0

        if usable_volume <= 0:

            print(
                "❌ Cannot calculate a single "
                "directional protection level."
            )

        else:

            for risk_fraction in RISK_LEVELS:

                risk_budget = (
                    equity
                    * risk_fraction
                )

                price_distance = (
                    risk_budget
                    / usable_volume
                )

                if direction == "BUY":

                    candidate = (
                        current_price
                        - price_distance
                    )

                else:

                    candidate = (
                        current_price
                        + price_distance
                    )

                print(
                    f"{risk_fraction * 100:>5.0f}%"
                    f"       | "
                    f"{money(risk_budget):>9}"
                    f" | "
                    f"{price_distance:>13.2f}"
                    f" | "
                    f"{price(candidate):>14}"
                )

        # ====================================================
        # IMPORTANT DISTANCE INFORMATION
        # ====================================================

        print("\n" + "=" * 64)
        print("ENTRY VS CURRENT PRICE")
        print("=" * 64)

        entry_difference = (
            weighted_entry
            - current_price
        )

        print(
            f"Weighted entry      : "
            f"{price(weighted_entry)}"
        )

        print(
            f"Current price       : "
            f"{price(current_price)}"
        )

        print(
            f"Entry-current       : "
            f"{price(entry_difference)}"
        )

        if direction == "BUY":

            print(
                "\n⚠️ The positions are BUY positions "
                "and the market is below the "
                "weighted entry."
            )

        elif direction == "SELL":

            print(
                "\n⚠️ The positions are SELL positions "
                "and the market is above the "
                "weighted entry."
            )

        # ====================================================
        # EXISTING PROTECTION
        # ====================================================

        without_sl = []
        without_tp = []

        for p in positions:

            ticket = p.get(
                "ticket",
                p.get("id")
            )

            if p.get("stop_loss") is None:
                without_sl.append(ticket)

            if p.get("take_profit") is None:
                without_tp.append(ticket)

        print("\n" + "=" * 64)
        print("EXISTING PROTECTION")
        print("=" * 64)

        print(
            f"Without Stop Loss  : "
            f"{len(without_sl)}/{len(positions)}"
        )

        print(
            f"Without Take Profit: "
            f"{len(without_tp)}/{len(positions)}"
        )

        # ====================================================
        # SAFETY BARRIER
        # ====================================================

        print("\n" + "=" * 64)
        print("SAFETY BARRIER")
        print("=" * 64)

        print(
            "🟢 READ-ONLY PROTECTION PLAN COMPLETE"
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

        print(
            "\n" + "=" * 64
        )

        print(
            "MT5API DISCONNECTED"
        )

        print(
            "=" * 64
        )


if __name__ == "__main__":
    main()
