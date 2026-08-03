class DerivBroker:
    def __init__(self):
        self.name = "Deriv"
        self.connected = False
        self.app_id = None
        self.api_token = None

    def connect(self):
        print("🎲 Connecting to Deriv...")
        self.connected = True
        print("✅ Connected to Deriv")

    def disconnect(self):
        print("🔌 Disconnecting from Deriv...")
        self.connected = False
        print("✅ Disconnected")

    def set_credentials(self, app_id, api_token):
        self.app_id = app_id
        self.api_token = api_token
        print("🔑 Deriv credentials configured.")

    def get_account(self):
        if self.connected:
            print("📊 Retrieving Deriv account information...")
        else:
            print("❌ Not connected to Deriv.")

    def status(self):
        return "ONLINE" if self.connected else "OFFLINE"
