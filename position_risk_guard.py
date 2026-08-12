# ============================================================
# Surge-Sniper
# READ-ONLY POSITION RISK GUARD
# ============================================================
#
# SAFETY:
#   GET requests only.
#
# This module NEVER:
#   - places orders
#   - modifies SL/TP
#   - closes positions
#   - sends PATCH requests
#   - sends POST requests
#
# ============================================================

from Brokers.MetaApi.metaapi import MetaApiBroker


class PositionRiskGuard:

    def __init__(self):
        self.broker = MetaApiBroker()

    # ========================================================
    # READ ACCOUNT
    # ========================================================

    def get_account(self):

        account = self.broker.get_account_snapshot()

        if not account:
            return None

        return account

    # ========================================================
    # READ POSITIONS
    # ========================================================

    def get_positions(self):

        positions = self.broker.get_positions()

        if positions is None:
            return None

        return positions

    # ========================================================
    # CALCULATE EXPOSURE
    # ========================================================

    def calculate_exposure(self, positions):

        if not positions:
            return {
                "count": 0,
                "total_volume": 0.0,
                "buy_volume": 0.0,
                "sell_volume": 0.0,
                "weighted_entry": None,
                "floating_profit": 0.0,
            }

        total_volume = 0.0
        buy_volume = 0.0
        sell_volume = 0.0
        weighted_value = 0.0
        floating_profit = 0.0

        for position in positions:

            volume = float(
                position.get("volume", 0) or 0
            )

            entry = position.get("open_price")

            profit = float(
                position.get("profit", 0) or 0
            )

            side = str(
                position.get("side", "")
            ).lower()

            total_volume += volume
            floating_profit += profit

            if entry is not None:

                weighted_value += (
                    float(entry) * volume
                )

            if side == "buy":
                buy_volume += volume

            elif side == "sell":
                sell_volume += volume

        weighted_entry = None

        if total_volume > 0:

            weighted_entry = (
                weighted_value / total_volume
            )

        return {
            "count": len(positions),
            "total_volume": total_volume,
            "buy_volume": buy_volume,
            "sell_volume": sell_volume,
            "weighted_entry": weighted_entry,
            "floating_profit": floating_profit,
        }

    # ========================================================
    # STRESS TEST
    # ========================================================

    def stress_test(
        self,
        exposure,
        current_price,
        equity
    ):

        volume = exposure["total_volume"]

        scenarios = [
            100,
            250,
            500,
            750,
            1000,
            1250,
        ]

        print("\n" + "=" * 64)
        print("READ-ONLY BTC STRESS TEST")
        print("=" * 64)

        if current_price is None:
            print("⚠️ Current price unavailable.")
            return

        if equity is None:
            print("⚠️ Equity unavailable.")
            return

        print(
            f"Current BTC price : ${current_price:,.2f}"
        )

        print(
            f"Total BTC volume  : {volume:.2f}"
        )

        print(
            f"Current equity    : ${equity:,.2f}"
        )

        print("\nDOWNWARD PRICE SCENARIOS")
        print("-" * 64)

        for move in scenarios:

            additional_loss = (
                move * volume
            )

            estimated_equity = (
                equity - additional_loss
            )

            print(
                f"-${move:<5} BTC move | "
                f"Additional loss: ${additional_loss:>8.2f} | "
                f"Est. equity: ${estimated_equity:>8.2f}"
            )

            if estimated_equity <= 0:

                print(
                    "    🚨 ESTIMATED EQUITY <= $0"
                )

            elif estimated_equity < equity * 0.25:

                print(
                    "    🔴 SEVERE EQUITY STRESS"
                )

            elif estimated_equity < equity * 0.50:

                print(
                    "    🟠 HIGH EQUITY STRESS"
                )

            elif estimated_equity < equity * 0.75:

                print(
                    "    🟡 MODERATE EQUITY STRESS"
                )

    # ========================================================
    # PROTECTION AUDIT
    # ========================================================

    def protection_audit(self, positions):

        without_sl = []
        without_tp = []

        for position in positions:

            ticket = position.get(
                "ticket",
                position.get("id")
            )

            stop_loss = position.get(
                "stop_loss"
            )

            take_profit = position.get(
                "take_profit"
            )

            if stop_loss is None:
                without_sl.append(ticket)

            if take_profit is None:
                without_tp.append(ticket)

        print("\n" + "=" * 64)
        print("PROTECTION AUDIT")
        print("=" * 64)

        print(
            f"Positions          : {len(positions)}"
        )

        print(
            f"Without Stop Loss : {len(without_sl)}"
        )

        print(
            f"Without Take Profit: {len(without_tp)}"
        )

        if without_sl:

            print(
                "\n⚠️ POSITIONS WITHOUT STOP LOSS"
            )

            for ticket in without_sl:

                print(
                    f"  - {ticket}"
                )

        if without_tp:

            print(
                "\n⚠️ POSITIONS WITHOUT TAKE PROFIT"
            )

            for ticket in without_tp:

                print(
                    f"  - {ticket}"
                )

    # ========================================================
    # FULL READ-ONLY AUDIT
    # ========================================================

    def run(self):

        print("=" * 64)
        print("SURGE-SNIPER READ-ONLY RISK GUARD")
        print("=" * 64)

        if not self.broker.connect():

            raise SystemExit(
                "❌ MT5API connection failed"
            )

        try:

            account = self.get_account()

            positions = self.get_positions()

            if positions is None:

                print(
                    "❌ Position state UNKNOWN."
                )

                return

            print(
                f"\n📊 OPEN POSITIONS: "
                f"{len(positions)}"
            )

            exposure = self.calculate_exposure(
                positions
            )

            print("\n" + "=" * 64)
            print("EXPOSURE")
            print("=" * 64)

            print(
                f"Positions       : "
                f"{exposure['count']}"
            )

            print(
                f"Total volume    : "
                f"{exposure['total_volume']:.2f}"
            )

            print(
                f"BUY volume      : "
                f"{exposure['buy_volume']:.2f}"
            )

            print(
                f"SELL volume     : "
                f"{exposure['sell_volume']:.2f}"
            )

            if exposure["weighted_entry"] is not None:

                print(
                    f"Weighted entry  : "
                    f"{exposure['weighted_entry']:.2f}"
                )

            print(
                f"Floating P/L    : "
                f"${exposure['floating_profit']:.2f}"
            )

            current_price = None

            if positions:

                symbol = positions[0].get(
                    "symbol"
                )

                if symbol:

                    current_price = (
                        self.broker.get_price(
                            symbol
                        )
                    )

                    print(
                        f"Current price   : "
                        f"{current_price}"
                    )

            equity = None

            if account:

                equity = account.get(
                    "equity"
                )

                print(
                    f"Account equity  : "
                    f"${float(equity):.2f}"
                    if equity is not None
                    else
                    "Account equity  : None"
                )

            self.protection_audit(
                positions
            )

            self.stress_test(
                exposure,
                current_price,
                float(equity)
                if equity is not None
                else None
            )

            print("\n" + "=" * 64)
            print("SAFETY BARRIER")
            print("=" * 64)
            print("🟢 READ-ONLY RISK AUDIT COMPLETE")
            print("🟢 NO PATCH REQUEST SENT")
            print("🟢 NO CLOSE REQUEST SENT")
            print("🟢 NO ORDER REQUEST SENT")
            print("🟢 NO POSITION WAS MODIFIED")

        finally:

            self.broker.disconnect()

            print("\n" + "=" * 64)
            print("MT5API DISCONNECTED")
            print("=" * 64)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    guard = PositionRiskGuard()

    guard.run()
