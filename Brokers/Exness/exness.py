# ============================================
# Surge-Sniper
# Exness Broker v3.1
# ============================================

import time


class ExnessBroker:

    def __init__(self):
        self.connected = False
        self.name = "Exness"

    def connect(self):

        print("🌍 Connecting to Exness...")

        self.connected = True

        print("✅ Connected to Exness")

        return True


    def disconnect(self):

        print("🔌 Disconnecting from Exness...")

        self.connected = False

        print("✅ Disconnected")


    def get_price(self, symbol):

        if not self.connected:
            print("❌ Exness not connected")
            return None

        print(f"📈 Requesting {symbol} price...")

        # Temporary market data simulation
        prices = {
            "XAUUSD": 3375.50,
            "EURUSD": 1.1650,
            "GBPUSD": 1.3420
        }

        price = prices.get(symbol, 0)

        return price


    def status(self):

        return "ONLINE" if self.connected else "OFFLINE"
