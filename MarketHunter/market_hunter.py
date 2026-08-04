# ============================================
# Surge-Sniper
# Market Hunter Module v0.1
# ============================================

class MarketHunter:
    """
    Market Hunter is responsible for observing
    the market and reporting its findings.
    """

    def __init__(self):
        self.symbol = None
        self.timeframe = None

    def set_market(self, symbol, timeframe):
        """Select the market to observe."""
        self.symbol = symbol
        self.timeframe = timeframe

    def scan_market(self):
        """Simulate a market scan."""
        print("\n========== MARKET HUNTER ==========")
        print(f"Symbol      : {self.symbol}")
        print(f"Timeframe   : {self.timeframe}")
        print("Status      : SCANNING...")
        print("Trend       : Unknown")
        print("Price       : Waiting for broker data...")
        print("Signal      : HOLD")
        print("===================================\n")
