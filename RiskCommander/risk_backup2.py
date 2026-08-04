import config


class RiskCommander:
    def __init__(self):
        self.risk_per_trade = config.RISK_PERCENT

    def load(self):
        print("🛡️ Loading Risk Commander...")
        print(f"✅ Risk Per Trade: {self.risk_per_trade}%")

    def status(self):
        return "ONLINE"
