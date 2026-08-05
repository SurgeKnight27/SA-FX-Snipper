# ============================================
# Surge-Sniper
# Trade Logger v1.0
# ============================================

from datetime import datetime


class TradeLogger:

    def __init__(self):
        self.trades = []

    def log_trade(
        self,
        symbol,
        direction,
        entry,
        lot_size,
        stop_loss,
        take_profit,
        status="OPEN"
    ):

        trade = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "symbol": symbol,
            "direction": direction,
            "entry": entry,
            "lot_size": lot_size,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "status": status
        }

        self.trades.append(trade)

        print("\n==================================================")
        print("📚 TRADE LOGGER")
        print("==================================================")
        print(f"Time         : {trade['time']}")
        print(f"Symbol       : {trade['symbol']}")
        print(f"Direction    : {trade['direction']}")
        print(f"Entry        : {trade['entry']}")
        print(f"Lot Size     : {trade['lot_size']}")
        print(f"Stop Loss    : {trade['stop_loss']}")
        print(f"Take Profit  : {trade['take_profit']}")
        print(f"Status       : {trade['status']}")

        return trade

    def total_trades(self):
        return len(self.trades)

    def show_history(self):

        print("\n==================================================")
        print("📚 TRADE HISTORY")
        print("==================================================")

        if not self.trades:
            print("No trades recorded.")
            return

        for index, trade in enumerate(self.trades, start=1):
            print(f"\nTrade #{index}")
            print(f"Time       : {trade['time']}")
            print(f"Symbol     : {trade['symbol']}")
            print(f"Direction  : {trade['direction']}")
            print(f"Entry      : {trade['entry']}")
            print(f"Status     : {trade['status']}")
