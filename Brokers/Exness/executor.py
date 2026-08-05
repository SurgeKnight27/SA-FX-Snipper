# ============================================
# Surge-Sniper
# Exness Trade Executor v1.1
# DEMO Execution Layer
# ============================================


class ExnessExecutor:

    def __init__(self):

        self.mode = "DEMO"
        self.open_trades = []


    def execute_trade(
        self,
        signal,
        symbol,
        entry,
        lot_size,
        stop_loss,
        take_profit
    ):

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
                "close_price": None,
                "profit_loss": 0,
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



    def close_trade(self, trade, close_price):

        trade["close_price"] = close_price


        if trade["type"] == "BUY":
            profit = close_price - trade["entry"]

        else:
            profit = trade["entry"] - close_price


        trade["profit_loss"] = round(profit, 2)
        trade["status"] = "CLOSED"


        print("==================================================")
        print("❌ TRADE CLOSED")
        print("==================================================")
        print(f"Symbol      : {trade['symbol']}")
        print(f"Close Price : {close_price}")
        print(f"P/L         : {trade['profit_loss']}")
        print("Status      : CLOSED")


        return trade



    def status(self):

        return f"Executor ONLINE | Mode: {self.mode}"
