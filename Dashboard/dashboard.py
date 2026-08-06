# ============================================
# Surge-Sniper
# Dashboard v1.1
# ============================================

import os
import sys

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

import config
from Brokers.broker_manager import BrokerManager


class Dashboard:

    def __init__(self):

        self.broker = BrokerManager()

    def show(self):

        self.broker.connect()

        status = self.broker.status()
        price = self.broker.get_price("XAUUSD")

        print("\n" + "=" * 50)
        print(f"🚀 {config.BOT_NAME}")
        print("AI TRADING COMMAND CENTER")
        print("=" * 50)

        print(f"Version        : {config.VERSION}")
        print(f"Mode           : {config.MODE}")

        print("\n========== MARKET ==========")
        print(f"Broker Status  : {status}")
        print("Broker         : Exness")
        print("Symbol         : XAUUSD")
        print(f"Live Price     : {price}")

        print("\n========== SYSTEM ==========")
        print("Scanner        : READY")
        print("Executor       : READY")
        print("Dashboard      : ONLINE")

        print("=" * 50)
        print("🟢 SURGE-SNIPPER READY")
        print("=" * 50)

        self.broker.disconnect()


if __name__ == "__main__":

    Dashboard().show()
