# ============================================
# Surge-Sniper
# Risk Commander v1.0
# ============================================

class RiskCommander:

    def __init__(self):
        self.risk_percent = 1.0
        self.max_risk = 2.0

    def status(self):
        return "ONLINE"

    def set_risk(self, risk):
        if risk <= self.max_risk:
            self.risk_percent = risk
            return True

        return False

    def calculate_position(self, balance, stop_loss_points):

        if stop_loss_points <= 0:
            return 0

        risk_amount = balance * (self.risk_percent / 100)

        lot_size = risk_amount / stop_loss_points

        return round(lot_size, 2)

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

    def approve_trade(self, signal, confidence):

        if signal in ["BUY", "SELL"] and confidence >= 70:
            return True

        return False
