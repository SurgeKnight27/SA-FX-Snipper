# ============================================
# Surge-Sniper
# Position Monitor v1.2
# ============================================

from Monitoring.trailing_stop import TrailingStop


class PositionMonitor:

    def __init__(self, executor=None, history=None):

        self.position = None
        self.executor = executor
        self.history = history
        self.trailing_stop = TrailingStop(distance=5)

    def open_position(
        self,
        symbol,
        direction,
        entry,
        stop_loss,
        take_profit,
        lot_size
    ):

        self.position = {
            "symbol": symbol,
            "direction": direction,
            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "lot_size": lot_size,
            "status": "OPEN"
        }

        print("\n==================================================")
        print("📡 POSITION MONITOR")
        print("==================================================")
        print("Position Opened Successfully")
        print(f"Symbol      : {symbol}")
        print(f"Direction   : {direction}")
        print(f"Entry       : {entry}")
        print(f"Stop Loss   : {stop_loss}")
        print(f"Take Profit : {take_profit}")
        print(f"Lot Size    : {lot_size}")
        print("Status      : OPEN")

    def check_position(self, current_price):

        if self.position is None:
            print("No open position.")
            return

        if self.position["status"] != "OPEN":
            print("Position already closed.")
            return

        self.trailing_stop.update(
            self.position,
            current_price
        )

        entry = self.position["entry"]

        if self.position["direction"] == "BUY":
            profit = current_price - entry
        else:
            profit = entry - current_price

        print("\n------------------------------")
        print("📈 POSITION UPDATE")
        print("------------------------------")
        print(f"Current Price : {current_price}")
        print(f"Floating P/L  : {round(profit, 2)}")
        print(f"Stop Loss     : {self.position['stop_loss']}")

        close_reason = None

        if self.position["direction"] == "BUY":

            if current_price >= self.position["take_profit"]:
                close_reason = "TP HIT"

            elif current_price <= self.position["stop_loss"]:
                close_reason = "SL HIT"

        else:

            if current_price <= self.position["take_profit"]:
                close_reason = "TP HIT"

            elif current_price >= self.position["stop_loss"]:
                close_reason = "SL HIT"

        if close_reason:

            print(f"🚨 {close_reason}")

            trade_for_close = {
                "symbol": self.position["symbol"],
                "type": self.position["direction"],
                "entry": self.position["entry"],
                "lot": self.position["lot_size"],
                "stop_loss": self.position["stop_loss"],
                "take_profit": self.position["take_profit"]
            }

            if self.executor:

                print("⚡ Sending close command to Executor...")

                closed_trade = self.executor.close_trade(
                    trade_for_close,
                    current_price
                )

                if self.history and closed_trade:

                    self.history.record_trade(
                        closed_trade["symbol"],
                        closed_trade["type"],
                        closed_trade["entry"],
                        closed_trade["close_price"],
                        closed_trade["lot"],
                        closed_trade["profit_loss"]
                    )

            self.position["status"] = "CLOSED"

            print("✅ Position closed successfully")

        print(f"Status        : {self.position['status']}")

    def status(self):

        if self.position:
            return self.position["status"]

        return "NO POSITION"
