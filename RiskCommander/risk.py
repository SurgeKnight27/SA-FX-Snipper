# ============================================
# Surge-Sniper
# Risk Commander v1.2
# ============================================

class RiskCommander:

    def __init__(self):

        self.risk_percent = 1.0
        self.max_risk = 2.0

        # XAUUSD settings
        self.contract_size = 100
        self.max_lot = 5.0


    def status(self):

        return "ONLINE"


    def set_risk(self, risk):

        if risk <= self.max_risk:

            self.risk_percent = risk
            return True

        return False


    def calculate_risk_amount(self, balance):

        return round(
            balance * (self.risk_percent / 100),
            2
        )


    def calculate_position(self, balance, stop_loss_points):

        if stop_loss_points <= 0:
            return 0


        risk_amount = self.calculate_risk_amount(balance)


        lot_size = (
            risk_amount /
            (stop_loss_points * self.contract_size)
        )


        lot_size = round(lot_size, 2)


        if lot_size > self.max_lot:

            lot_size = self.max_lot


        return lot_size


    def calculate_targets(self, entry, direction):

        if direction == "BUY":

            stop_loss = entry - 10
            take_profit = entry + 20


        elif direction == "SELL":

            stop_loss = entry + 10
            take_profit = entry - 20


        else:

            stop_loss = None
            take_profit = None


        return {

            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": "1:2"

        }


    def risk_report(self, balance, stop_loss_points):

        risk_amount = self.calculate_risk_amount(balance)

        lot_size = self.calculate_position(
            balance,
            stop_loss_points
        )


        return {

            "balance": balance,
            "risk_percent": self.risk_percent,
            "risk_amount": risk_amount,
            "lot_size": lot_size

        }


    def approve_trade(self, signal, confidence):

        if signal in ["BUY", "SELL"] and confidence >= 70:

            return True


        return False
