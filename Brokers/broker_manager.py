# ============================================
# Surge-Sniper
# Broker Manager v3.1
# ============================================

from Brokers.Exness.exness import ExnessBroker
from Brokers.Deriv.deriv import DerivBroker
from Brokers.XM.xm import XMBroker
from Brokers.MetaApi.metaapi import MetaApiBroker


class BrokerManager:

    def __init__(self):

        self.brokers = {
            "Exness": ExnessBroker(),
            "Deriv": DerivBroker(),
            "XM": XMBroker(),
            "MetaApi": MetaApiBroker()
        }

        # MT5API is the active broker
        self.active_broker_name = "MetaApi"
        self.active_broker = self.brokers[self.active_broker_name]

    def list_brokers(self):

        return list(self.brokers.keys())

    def set_active_broker(self, broker_name):

        if broker_name not in self.brokers:
            print("❌ Broker not supported.")
            return False

        self.active_broker_name = broker_name
        self.active_broker = self.brokers[broker_name]

        print(f"✅ Active Broker: {broker_name}")

        return True

    def get_active_broker(self):

        return self.active_broker

    def get_active_broker_name(self):

        return self.active_broker_name

    def connect(self):

        print(
            f"🔌 Connecting to active broker: "
            f"{self.active_broker_name}"
        )

        return self.active_broker.connect()

    def disconnect(self):

        return self.active_broker.disconnect()

    def get_price(self, symbol):

        return self.active_broker.get_price(symbol)

    def get_account(self):

        return self.active_broker.get_account()

    def get_positions(self):

        if hasattr(self.active_broker, "get_positions"):
            return self.active_broker.get_positions()

        print(
            f"⚠️ {self.active_broker_name} "
            "does not support position retrieval."
        )

        # None means the position state is UNKNOWN.
        # Never convert this into an empty position list.
        return None

    def get_position_count(self):

        positions = self.get_positions()

        if positions is None:
            return None

        return len(positions)

    def status(self):

        return self.active_broker.status()
