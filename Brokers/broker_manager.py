# ============================================
# Surge-Sniper
# Broker Manager v2.0
# ============================================

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

        self.active_broker = self.brokers["Exness"]

    def list_brokers(self):

        return list(self.brokers.keys())

    def set_active_broker(self, broker_name):

        if broker_name in self.brokers:

            self.active_broker = self.brokers[broker_name]

            print(f"✅ Active Broker: {broker_name}")

        else:

            print("❌ Broker not supported.")

    def get_active_broker(self):

        return self.active_broker

    def connect(self):

        return self.active_broker.connect()

    def disconnect(self):

        return self.active_broker.disconnect()

    def get_price(self, symbol):

        return self.active_broker.get_price(symbol)

    def status(self):

        return self.active_broker.status()
