# ============================================
# Surge-Sniper
# Position Monitor v1.1
# ============================================


class PositionMonitor:


    def __init__(self, executor=None):

        self.position = None
        self.executor = executor



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



        entry = self.position["entry"]


        if self.position["direction"] == "BUY":

            profit = current_price - entry

        else:

            profit = entry - current_price



        print("\n------------------------------")
        print("📈 POSITION UPDATE")
        print("------------------------------")
        print(f"Current Price : {current_price}")
        print(f"Floating P/L  : {round(profit,2)}")



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

            self.position["status"] = close_reason



            if self.executor:

                print("⚡ Sending close command to Executor...")



        print(f"Status        : {self.position['status']}")



    def status(self):


        if self.position:

            return self.position["status"]


        return "NO POSITION"
