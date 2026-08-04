from Brokers.Exness.exness import ExnessBroker
from Brokers.Deriv.deriv import DerivBroker
from Brokers.XM.xm import XMBroker


class BrokerManager:
    def __init__(self):
        self.brokers = {
            "Exness": ExnessBroker(),
            "Deriv": DerivBroker(),
            "XM": XMBroker()
        }
        self.active_broker = None

    def select_broker(self, name):
        if name in self.brokers:
            self.active_broker = self.brokers[name]
            print(f"✅ Active broker: {name}")
        else:
            print("❌ Broker not found")

    def connect(self):
        if self.active_broker:
            self.active_broker.connect()
        else:
            print("❌ No broker selected")

    def disconnect(self):
        if self.active_broker:
            self.active_broker.disconnect()
        else:
            print("❌ No broker selected")

    def status(self):
        if self.active_broker:
            return self.active_broker.status()
        return "NO BROKER SELECTED"

    def get_price(self, symbol):
        if self.active_broker:
            return self.active_broker.get_price(symbol)
        else:
            print("❌ No broker selected.")
            return None
