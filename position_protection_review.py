import math

from Brokers.MetaApi.metaapi import MetaApiBroker


# ============================================================
# SURGE-SNIPER
# PER-POSITION PROTECTION REVIEW
# ============================================================
#
# READ-ONLY ONLY
#
# This script:
#   - Reads open positions
#   - Reads account equity
#   - Reads current market price
#   - Calculates candidate SL levels
#   - Calculates estimated loss at each level
#
# This script DOES NOT:
#   - PATCH positions
#   - CLOSE positions
#   - PLACE orders
# ============================================================


RISK_LEVELS = (
    0.01,
    0.02,
    0.05,
    0.10,
    0.20,
)


def money(value):
    return f"${float(value):,.2f}"


def px(value):
    return f"{float(value):,.2f}"


def main():

    print("=" * 68)
    print("SURGE-SNIPER PER-POSITION PROTECTION REVIEW")
    print("=" * 68)

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
                "❌ Account data unavailable."
            )

        equity = account.get("equity")

        if equity is None:
            raise SystemExit(
                "❌ Account equity unavailable."
            )

        equity = float(equity)

        print(
            f"\nAccount equity : {money(equity)}"
        )

        # ====================================================
        # POSITIONS
        # ====================================================

        positions = broker.get_positions()

        if positions is None:
            raise SystemExit(
                "❌ Position state UNKNOWN."
            )

        if not positions:
            print(
                "\n🟢 No open positions."
            )
            return

        print(
            f"Open positions : {len(positions)}"
        )

        # ====================================================
        # PROCESS EACH POSITION
        # ====================================================

        for number, position in enumerate(
            positions,
            1
        ):

            ticket = position.get(
                "ticket",
                position.get("id")
            )

            symbol = position.get(
                "symbol",
                "UNKNOWN"
            )

            side = str(
                position.get(
                    "side",
                    ""
                )
            ).upper()

            volume = float(
                position.get(
                    "volume",
                    0
                ) or 0
            )

            entry = position.get(
                "open_price"
            )

            stop_loss = position.get(
                "stop_loss"
            )

            take_profit = position.get(
                "take_profit"
            )

            profit = float(
                position.get(
                    "profit",
                    0
                ) or 0
            )

            print("\n" + "=" * 68)
            print(
                f"POSITION {number}/{len(positions)}"
            )
            print("=" * 68)

            print(
                f"Ticket          : {ticket}"
            )

            print(
                f"Symbol          : {symbol}"
            )

            print(
                f"Side            : {side}"
            )

            print(
                f"Volume          : {volume:.2f}"
            )

            print(
                f"Entry price     : "
                f"{px(entry) if entry is not None else 'N/A'}"
            )

            print(
                f"Current P/L     : {money(profit)}"
            )

            print(
                f"Existing SL     : "
                f"{px(stop_loss) if stop_loss is not None else 'NONE'}"
            )

            print(
                f"Existing TP     : "
                f"{px(take_profit) if take_profit is not None else 'NONE'}"
            )

            # =================================================
            # CURRENT PRICE
            # =================================================

            current = broker.get_price(
                symbol
            )

            if current is None:

                print(
                    "\n❌ Current price unavailable."
                )

                continue

            current = float(current)

            print(
                f"Current price   : {px(current)}"
            )

            # =================================================
            # POSITION VALIDATION
            # =================================================

            if entry is None:

                print(
                    "\n⚠️ Entry price unavailable."
                )

                continue

            entry = float(entry)

            if volume <= 0:

                print(
                    "\n⚠️ Invalid position volume."
                )

                continue

            if side not in (
                "BUY",
                "SELL"
            ):

                print(
                    "\n⚠️ Unknown position direction."
                )

                continue

            # =================================================
            # DISTANCE FROM ENTRY
            # =================================================

            if side == "BUY":

                current_to_entry = (
                    entry - current
                )

            else:

                current_to_entry = (
                    current - entry
                )

            print(
                f"Adverse distance: "
                f"{px(current_to_entry)}"
            )

            # =================================================
            # CANDIDATE LEVELS
            # =================================================

            print(
                "\nCANDIDATE STOP-LOSS LEVELS"
            )

            print(
                "-" * 68
            )

            print(
                "Risk   Budget       Price distance    Candidate SL"
            )

            print(
                "-" * 68
            )

            for risk_fraction in RISK_LEVELS:

                risk_budget = (
                    equity
                    * risk_fraction
                )

                price_distance = (
                    risk_budget
                    / volume
                )

                if side == "BUY":

                    candidate_sl = (
                        current
                        - price_distance
                    )

                else:

                    candidate_sl = (
                        current
                        + price_distance
                    )

                print(
                    f"{risk_fraction * 100:>3.0f}%   "
                    f"{money(risk_budget):>10}   "
                    f"{price_distance:>14.2f}   "
                    f"{px(candidate_sl):>14}"
                )

            # =================================================
            # ENTRY-BASED PROTECTION INFORMATION
            # =================================================

            print(
                "\nENTRY-BASED INFORMATION"
            )

            print(
                "-" * 68
            )

            for percentage in (
                1,
                2,
                5
            ):

                distance = (
                    entry
                    * percentage
                    / 100
                )

                if side == "BUY":

                    level = (
                        entry
                        - distance
                    )

                else:

                    level = (
                        entry
                        + distance
                    )

                print(
                    f"{percentage}% from entry : "
                    f"{px(level)}"
                )

            # =================================================
            # SAFETY ASSESSMENT
            # =================================================

            print(
                "\nREVIEW"
            )

            if stop_loss is None:

                print(
                    "⚠️ No existing Stop Loss."
                )

            else:

                print(
                    "🟢 Existing Stop Loss present."
                )

            if take_profit is None:

                print(
                    "⚠️ No existing Take Profit."
                )

            else:

                print(
                    "🟢 Existing Take Profit present."
                )

            if side == "BUY" and current < entry:

                print(
                    "🔴 BUY position is currently "
                    "below entry."
                )

            elif side == "SELL" and current > entry:

                print(
                    "🔴 SELL position is currently "
                    "above entry."
                )

            else:

                print(
                    "🟢 Position is currently "
                    "favorable versus entry."
                )

        # ====================================================
        # FINAL SAFETY BARRIER
        # ====================================================

        print("\n" + "=" * 68)
        print("READ-ONLY SAFETY BARRIER")
        print("=" * 68)

        print(
            "🟢 PROTECTION REVIEW COMPLETE"
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
            "\n" + "=" * 68
        )

        print(
            "MT5API DISCONNECTED"
        )

        print(
            "=" * 68
        )


if __name__ == "__main__":
    main()
