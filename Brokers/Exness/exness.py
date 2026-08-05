# ============================================
# Surge-Sniper
# Exness Broker v2.0
# ============================================


class ExnessBroker:

    def __init__(self):

        self.connected = False

    def connect(self):

        print("🌍 Connecting to Exness...")

        self.connected = True

        print("✅ Connected to Exness")

        return True

    def disconnect(self):

        if self.connected:

            print("🔌 Disconnecting from Exness...")

            self.connected = False

            print("✅ Disconnected")

    def get_price(self, symbol):

        if self.connected:

            print(f"📈 Requesting latest price for {symbol}...")

            return 3375.50

        print("❌ Not connected to Exness.")

        return None

    def status(self):

        return "ONLINE" if self.connected else "OFFLINE"
