import config


class RiskCommander:
    def __init__(self):
        self.risk_percent = config.RISK_PERCENT

    def load(self):
        print("🛡️ Loading Risk Commander...")
        print(f"✅ Risk Per Trade: {self.risk_percent}%")

    def calculate_risk_amount(self, account_balance):
        """Calculate the maximum amount to risk on a trade."""
        return account_balance * (self.risk_percent / 100)

    def approve_trade(self, account_balance, stop_loss_amount):
        """Check if the trade is within the allowed risk."""
        max_risk = self.calculate_risk_amount(account_balance)

        if stop_loss_amount <= max_risk:
            return True, "Trade Approved ✅"
        else:
            return False, "Trade Rejected ❌ - Risk Too High"

    def status(self):
        return "ONLINE"
