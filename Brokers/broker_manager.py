class BrokerManager:
    def __init__(self):
        self.available_brokers = [
            "Exness",
            "Deriv",
            "XM"
        ]
        self.active_broker = None

    def list_brokers(self):
        return self.available_brokers

    def set_active_broker(self, broker_name):
        if broker_name in self.available_brokers:
            self.active_broker = broker_name
            print(f"✅ Active Broker: {broker_name}")
        else:
            print("❌ Broker not supported.")

    def get_active_broker(self):
        return self.active_broker

    def status(self):
        return "ONLINE"
