# ============================================
# Surge-Sniper
# Live Trading Engine v1.2
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

from Brokers.broker_manager import BrokerManager
from MarketHunter.scanner import MarketHunter


class LiveTrading:

    def __init__(self):

        self.broker = BrokerManager()
        self.scanner = MarketHunter()

    def start(self):

        print("==================================================")
        print("🚀 SURGE-SNIPPER LIVE TRADING ENGINE")
        print("==================================================")

        print("🌍 Connecting to broker...")

        self.broker.connect()

        print(f"Broker Status : {self.broker.status()}")

        price = self.broker.get_price("XAUUSD")

        print(f"📈 Live XAUUSD Price : {price}")

        self.scanner.update_price(price)

        signal = self.scanner.scan_market()

        print("\n==================================================")
        print("🎯 MARKET ANALYSIS")
        print("==================================================")
        print(f"Signal : {signal}")

        self.broker.disconnect()

        print("✅ Live Engine Ready")


if __name__ == "__main__":

    engine = LiveTrading()
    engine.start()
