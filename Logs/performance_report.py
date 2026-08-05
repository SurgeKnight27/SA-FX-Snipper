# ============================================
# Surge-Sniper
# Performance Report v1.0
# ============================================


class PerformanceReport:

    def __init__(self, trades):

        self.trades = trades

    def generate(self):

        print("\n==================================================")
        print("📊 PERFORMANCE REPORT")
        print("==================================================")

        if not self.trades:

            print("No completed trades.")
            return

        total = len(self.trades)

        wins = sum(
            1
            for trade in self.trades
            if trade["result"] == "WIN"
        )

        losses = total - wins

        win_rate = round(
            (wins / total) * 100,
            2
        )

        profits = [
            trade["profit"]
            for trade in self.trades
        ]

        net_profit = round(
            sum(profits),
            2
        )

        best_trade = round(
            max(profits),
            2
        )

        worst_trade = round(
            min(profits),
            2
        )

        winning_profits = [
            p for p in profits
            if p > 0
        ]

        losing_profits = [
            p for p in profits
            if p < 0
        ]

        average_win = round(
            sum(winning_profits) / len(winning_profits),
            2
        ) if winning_profits else 0

        average_loss = round(
            sum(losing_profits) / len(losing_profits),
            2
        ) if losing_profits else 0

        gross_profit = sum(
            p for p in profits
            if p > 0
        )

        gross_loss = abs(
            sum(
                p for p in profits
                if p < 0
            )
        )

        if gross_loss == 0:
            profit_factor = "∞"
        else:
            profit_factor = round(
                gross_profit / gross_loss,
                2
            )

        print(f"Total Trades : {total}")
        print(f"Wins         : {wins}")
        print(f"Losses       : {losses}")
        print(f"Win Rate     : {win_rate}%")
        print(f"Net Profit   : {net_profit}")
        print(f"Best Trade   : {best_trade}")
        print(f"Worst Trade  : {worst_trade}")
        print(f"Average Win  : {average_win}")
        print(f"Average Loss : {average_loss}")
        print(f"Profit Factor: {profit_factor}")
        print("==================================================")
