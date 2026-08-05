# ============================================
# Surge-Sniper
# Exness Trade Executor v1.0
# DEMO Execution Layer
# ============================================


class ExnessExecutor:

    def __init__(self):
        self.mode = "DEMO"
        self.open_trades = []

    def execute_trade(self, signal, symbol, entry, lot_size, stop_loss, take_profit):

        print("==================================================")
        print("⚡ TRADE EXECUTION ENGINE")
        print("==================================================")

        if self.mode == "DEMO":

            trade = {
                "symbol": symbol,
                "type": signal,
                "entry": entry,
                "lot": lot_size,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "status": "OPEN"
            }

            self.open_trades.append(trade)

            print("🟢 DEMO TRADE EXECUTED")
            print(f"Symbol      : {symbol}")
            print(f"Direction   : {signal}")
            print(f"Entry       : {entry}")
            print(f"Lot Size    : {lot_size}")
            print(f"Stop Loss   : {stop_loss}")
            print(f"Take Profit : {take_profit}")

            return trade

        print("🔴 LIVE EXECUTION LOCKED")
        return None


    def close_trade(self, trade):

        trade["status"] = "CLOSED"

        print("❌ TRADE CLOSED")
        print(trade)

        return trade


    def status(self):

        return f"Executor ONLINE | Mode: {self.mode}"
