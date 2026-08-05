# ============================================
# Surge-Sniper
# Trade History v2.0
# ============================================

from datetime import datetime


class TradeHistory:

    def __init__(self):

        self.trades = []

    def record_trade(
        self,
        symbol,
        direction,
        entry,
        exit_price,
        lot_size,
        profit_loss
    ):

        trade = {

            "time": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "symbol": symbol,
            "direction": direction,
            "entry": entry,
            "exit": exit_price,
            "lot_size": lot_size,
            "profit": profit_loss,

            "result":
                "WIN" if profit_loss > 0 else "LOSS"

        }

        self.trades.append(trade)

        print("\n==================================================")
        print("📚 TRADE HISTORY")
        print("==================================================")
        print(f"Time        : {trade['time']}")
        print(f"Symbol      : {trade['symbol']}")
        print(f"Direction   : {trade['direction']}")
        print(f"Entry       : {trade['entry']}")
        print(f"Exit        : {trade['exit']}")
        print(f"Lot Size    : {trade['lot_size']}")
        print(f"P/L         : {trade['profit']}")
        print(f"Result      : {trade['result']}")

        return trade

    def statistics(self):

        total = len(self.trades)

        if total == 0:

            return {

                "total_trades": 0,
                "wins": 0,
                "losses": 0,
                "win_rate": 0,
                "net_profit": 0,
                "best_trade": 0,
                "worst_trade": 0,
                "average_win": 0,
                "average_loss": 0

            }

        wins = len(
            [
                trade
                for trade in self.trades
                if trade["result"] == "WIN"
            ]
        )

        losses = total - wins

        profits = [
            trade["profit"]
            for trade in self.trades
        ]

        net_profit = sum(profits)

        best_trade = max(profits)
        worst_trade = min(profits)

        winning = [p for p in profits if p > 0]
        losing = [p for p in profits if p < 0]

        average_win = (
            sum(winning) / len(winning)
            if winning else 0
        )

        average_loss = (
            sum(losing) / len(losing)
            if losing else 0
        )

        win_rate = round(
            (wins / total) * 100,
            2
        )

        return {

            "total_trades": total,
            "wins": wins,
            "losses": losses,
            "win_rate": win_rate,
            "net_profit": round(net_profit, 2),
            "best_trade": round(best_trade, 2),
            "worst_trade": round(worst_trade, 2),
            "average_win": round(average_win, 2),
            "average_loss": round(average_loss, 2)

        }

    def show_statistics(self):

        stats = self.statistics()

        print("\n==================================================")
        print("📊 PERFORMANCE REPORT")
        print("==================================================")
        print(f"Total Trades : {stats['total_trades']}")
        print(f"Wins         : {stats['wins']}")
        print(f"Losses       : {stats['losses']}")
        print(f"Win Rate     : {stats['win_rate']}%")
        print(f"Net P/L      : {stats['net_profit']}")
        print(f"Best Trade   : {stats['best_trade']}")
        print(f"Worst Trade  : {stats['worst_trade']}")
        print(f"Average Win  : {stats['average_win']}")
        print(f"Average Loss : {stats['average_loss']}")

    def show_history(self):

        print("\n==================================================")
        print("📚 COMPLETE TRADE HISTORY")
        print("==================================================")

        if not self.trades:

            print("No trades recorded.")
            return

        for index, trade in enumerate(self.trades, start=1):

            print(f"\nTrade #{index}")
            print(f"Time      : {trade['time']}")
            print(f"Symbol    : {trade['symbol']}")
            print(f"Direction : {trade['direction']}")
            print(f"Entry     : {trade['entry']}")
            print(f"Exit      : {trade['exit']}")
            print(f"P/L       : {trade['profit']}")
            print(f"Result    : {trade['result']}")
