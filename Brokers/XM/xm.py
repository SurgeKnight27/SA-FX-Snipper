class XMBroker:
    def __init__(self):
        self.name = "XM"
        self.connected = False

    def connect(self):
        print("🟦 Connecting to XM...")
        self.connected = True
        print("✅ Connected to XM")

    def disconnect(self):
        print("🔌 Disconnecting from XM...")
        self.connected = False
        print("✅ Disconnected")

    def get_account(self):
        if self.connected:
            print("📊 Retrieving XM account information...")
        else:
            print("❌ Not connected to XM.")

    def status(self):
        return "ONLINE" if self.connected else "OFFLINE"
