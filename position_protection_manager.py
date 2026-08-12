import time
from Brokers.MetaApi.metaapi import MetaApiBroker


# ============================================================
# SURGE-SNIPER
# EXISTING POSITION PROTECTION MANAGER
# ============================================================
#
# AUTHORIZED ACTION:
#   Apply Stop Loss ONLY to existing open positions.
#
# WILL NOT:
#   - open trades
#   - close trades
#   - modify Take Profit
#   - modify volume
#
# PROTECTION MODEL:
#   2% of CURRENT EQUITY = maximum additional portfolio risk
#   from the current market price.
#
# IMPORTANT:
#   This script calculates ONE portfolio-level SL for the
#   existing BTC BUY exposure.
# ============================================================


TOTAL_RISK_PERCENT = 0.02

SYMBOL_REQUIRED = "BTCUSDm"

VERIFY_DELAY = 1.0


def money(value):
    return f"${float(value):,.2f}"


def px(value):
    return f"{float(value):,.2f}"


def main():

    print("=" * 68)
    print("SURGE-SNIPER EXISTING POSITION PROTECTION")
    print("=" * 68)

    print("\n⚠️ EXECUTION MODE")
    print("This operation WILL modify existing positions.")
    print("No new orders will be placed.")
    print("No positions will be closed.")
    print("Take Profit values will NOT be changed.")

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
                "❌ Equity unavailable."
            )

        equity = float(equity)

        risk_budget = (
            equity
            * TOTAL_RISK_PERCENT
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
            raise SystemExit(
                "❌ No open positions found."
            )

        print(
            f"\nOpen positions : {len(positions)}"
        )

        # ====================================================
        # SAFETY VALIDATION
        # ====================================================

        total_volume = 0.0
        buy_volume = 0.0
        sell_volume = 0.0

        tickets = []

        for p in positions:

            symbol = p.get("symbol")

            side = str(
                p.get("side", "")
            ).lower()

            ticket = p.get(
                "ticket",
                p.get("id")
            )

            volume = float(
                p.get("volume", 0) or 0
            )

            if symbol != SYMBOL_REQUIRED:

                raise SystemExit(
                    f"❌ Unexpected symbol: {symbol}"
                )

            if side not in (
                "buy",
                "sell"
            ):

                raise SystemExit(
                    f"❌ Unknown position side "
                    f"for {ticket}: {side}"
                )

            if not ticket:

                raise SystemExit(
                    "❌ Position without ticket."
                )

            if volume <= 0:

                raise SystemExit(
                    f"❌ Invalid volume for "
                    f"{ticket}: {volume}"
                )

            tickets.append(str(ticket))

            total_volume += volume

            if side == "buy":
                buy_volume += volume

            else:
                sell_volume += volume

        # ====================================================
        # REQUIRE PURE BUY BOOK
        # ====================================================

        if sell_volume > 0:

            raise SystemExit(
                "❌ SELL exposure detected. "
                "Protection operation aborted."
            )

        if buy_volume <= 0:

            raise SystemExit(
                "❌ No BUY exposure detected."
            )

        # ====================================================
        # CURRENT PRICE
        # ====================================================

        current_price = broker.get_price(
            SYMBOL_REQUIRED
        )

        if current_price is None:

            raise SystemExit(
                "❌ Current BTC price unavailable."
            )

        current_price = float(
            current_price
        )

        # ====================================================
        # CALCULATE PORTFOLIO SL
        # ====================================================

        price_distance = (
            risk_budget
            / buy_volume
        )

        candidate_sl = (
            current_price
            - price_distance
        )

        # Safety check: BUY SL must be BELOW current price.

        if candidate_sl >= current_price:

            raise SystemExit(
                "❌ Calculated BUY Stop Loss "
                "is not below current price."
            )

        # ====================================================
        # DISPLAY EXECUTION PLAN
        # ====================================================

        print("\n" + "=" * 68)
        print("EXECUTION PLAN")
        print("=" * 68)

        print(
            f"Symbol              : {SYMBOL_REQUIRED}"
        )

        print(
            f"Positions            : {len(positions)}"
        )

        print(
            f"BUY volume           : {buy_volume:.2f}"
        )

        print(
            f"Current equity       : {money(equity)}"
        )

        print(
            f"Risk budget          : "
            f"{TOTAL_RISK_PERCENT * 100:.0f}% "
            f"= {money(risk_budget)}"
        )

        print(
            f"Current BTC price    : "
            f"{px(current_price)}"
        )

        print(
            f"SL distance          : "
            f"{px(price_distance)}"
        )

        print(
            f"NEW STOP LOSS        : "
            f"{px(candidate_sl)}"
        )

        print(
            "\nExisting Take Profit values "
            "will remain unchanged."
        )

        print(
            "\nTickets to protect:"
        )

        for ticket in tickets:

            print(
                f"  {ticket} -> SL {px(candidate_sl)}"
            )

        # ====================================================
        # FINAL INTERNAL SAFETY CHECKS
        # ====================================================

        print("\n" + "=" * 68)
        print("FINAL SAFETY CHECKS")
        print("=" * 68)

        print(
            "✓ Existing positions only"
        )

        print(
            "✓ BTCUSDm only"
        )

        print(
            "✓ BUY positions only"
        )

        print(
            "✓ No SELL exposure"
        )

        print(
            "✓ Stop Loss only"
        )

        print(
            "✓ Take Profit untouched"
        )

        print(
            "✓ No order creation"
        )

        print(
            "✓ No position closing"
        )

        print(
            "✓ Portfolio risk budget = 2% equity"
        )

        # ====================================================
        # APPLY
        # ====================================================

        print("\n" + "=" * 68)
        print("APPLYING STOP LOSSES")
        print("=" * 68)

        successful = []
        failed = []

        for p in positions:

            ticket = p.get(
                "ticket",
                p.get("id")
            )

            print(
                f"\n🛡️ Applying SL to "
                f"{ticket}..."
            )

            result = broker.modify_position(
                ticket=ticket,
                stop_loss=candidate_sl
            )

            if result is not None:

                print(
                    f"🟢 PATCH SUCCESS: {ticket}"
                )

                successful.append(
                    str(ticket)
                )

            else:

                print(
                    f"🔴 PATCH FAILED: {ticket}"
                )

                failed.append(
                    str(ticket)
                )

        # ====================================================
        # POST-EXECUTION VERIFICATION
        # ====================================================

        print("\n" + "=" * 68)
        print("POST-EXECUTION VERIFICATION")
        print("=" * 68)

        time.sleep(
            VERIFY_DELAY
        )

        verified_positions = (
            broker.get_positions()
        )

        if verified_positions is None:

            print(
                "🔴 VERIFICATION FAILED: "
                "position state UNKNOWN."
            )

        else:

            verified = 0
            verification_failed = []

            for p in verified_positions:

                ticket = str(
                    p.get(
                        "ticket",
                        p.get("id")
                    )
                )

                if ticket not in tickets:
                    continue

                sl = p.get(
                    "stop_loss"
                )

                if sl is None:

                    verification_failed.append(
                        ticket
                    )

                    continue

                sl = float(sl)

                # Allow a small numerical tolerance.

                tolerance = 0.01

                if abs(
                    sl - candidate_sl
                ) <= tolerance:

                    verified += 1

                else:

                    verification_failed.append(
                        ticket
                    )

            print(
                f"Expected protected : "
                f"{len(tickets)}"
            )

            print(
                f"PATCH successes    : "
                f"{len(successful)}"
            )

            print(
                f"PATCH failures     : "
                f"{len(failed)}"
            )

            print(
                f"Verified SLs       : "
                f"{verified}"
            )

            if verification_failed:

                print(
                    "\n⚠️ VERIFICATION "
                    "EXCEPTIONS:"
                )

                for ticket in (
                    verification_failed
                ):

                    print(
                        f"  - {ticket}"
                    )

        # ====================================================
        # FINAL STATUS
        # ====================================================

        print("\n" + "=" * 68)
        print("PROTECTION RESULT")
        print("=" * 68)

        if not failed:

            print(
                "🟢 ALL PATCH REQUESTS "
                "RETURNED SUCCESSFULLY"
            )

        else:

            print(
                "🔴 SOME PATCH REQUESTS FAILED"
            )

            for ticket in failed:

                print(
                    f"  - {ticket}"
                )

        print(
            "\n⚠️ Existing positions were "
            "the ONLY objects targeted."
        )

        print(
            "⚠️ No new order was created."
        )

        print(
            "⚠️ No position was closed."
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
