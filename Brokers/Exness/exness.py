# ============================================
# Surge-Sniper
# Exness Broker v1.1
# ============================================


class ExnessBroker:

    def __init__(self):

        self.name = "Exness"
        self.connected = False
        self.balance = 1000.00


    def connect(self):

        print("🌍 Connecting to Exness...")

        self.connected = True

        print("✅ Connected to Exness")


    def disconnect(self):

        print("🔌 Disconnecting from Exness...")

        self.connected = False

        print("✅ Disconnected")


    def get_account(self):

        if self.connected:

            print("📊 Retrieving Exness account information...")

            return {
                "balance": self.balance,
                "currency": "USD"
            }

        else:

            print("❌ Not connected to Exness.")

            return None


    def get_price(self, symbol):

        if self.connected:

            print(f"📈 Requesting latest price for {symbol}...")

            return 3375.50

        else:

            print("❌ Not connected to Exness.")

            return None


    def status(self):

        return "ONLINE" if self.connected else "OFFLINE"
