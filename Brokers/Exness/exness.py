class ExnessBroker:
    def __init__(self):
        self.name = "Exness"
        self.connected = False

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
        else:
            print("❌ Not connected to Exness.")

    def get_price(self, symbol):
        """
        Placeholder for retrieving the latest market price.
        In a future version this will request live data
        from Exness/MetaTrader.
        """
        if self.connected:
            print(f"📈 Requesting latest price for {symbol}...")
            return 3375.50
        else:
            print("❌ Not connected to Exness.")
            return None

    def status(self):
        return "ONLINE" if self.connected else "OFFLINE"
