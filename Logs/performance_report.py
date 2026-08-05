# ============================================
# Surge-Sniper
# Performance Report v1.0
# ============================================


class PerformanceReport:

    def __init__(self, trades):

        self.trades = trades

    def generate(self):

        if not self.trades:

            print("\n==================================================")
            print("📊 PERFORMANCE REPORT")
            print("==================================================")
            print("No completed trades.")
            return

        total = len(self.trades)

        wins = sum(
            1 for trade in self.trades
            if trade["result"] == "WIN"
        )

        losses = total - wins

        win_rate = round((wins / total) * 100, 2)

        profits = [
            trade["profit_loss"]
            for trade in self.trades
        ]

        net_profit = sum(profits)

        best_trade = max(profits)

        worst_trade = min(profits)

        winning_profits = [
            p for p in profits
            if p > 0
        ]

        losing_profits = [
            p for p in profits
            if p < 0
        ]

        average_win = (
            round(
                sum(winning_profits) / len(winning_profits),
                2
            )
            if winning_profits else 0
        )

        average_loss = (
            round(
                sum(losing_profits) / len(losing_profits),
                2
            )
            if losing_profits else 0
        )

        gross_profit = sum(winning_profits)

        gross_loss = abs(sum(losing_profits))

        profit_factor = (
            round(gross_profit / gross_loss, 2)
            if gross_loss > 0 else "∞"
        )

        print("\n==================================================")
        print("📊 PERFORMANCE REPORT")
        print("==================================================")
        print(f"Total Trades : {total}")
        print(f"Wins         : {wins}")
        print(f"Losses       : {losses}")
        print(f"Win Rate     : {win_rate}%")
        print(f"Net Profit   : {round(net_profit, 2)}")
        print(f"Best Trade   : {round(best_trade, 2)}")
        print(f"Worst Trade  : {round(worst_trade, 2)}")
        print(f"Average Win  : {average_win}")
        print(f"Average Loss : {average_loss}")
        print(f"Profit Factor: {profit_factor}")
        print("==================================================")
