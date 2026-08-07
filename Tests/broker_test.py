import sys
import os

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

sys.path.append(PROJECT_DIR)

from Brokers.broker_manager_v2 import BrokerManager


print("🚀 Surge-Sniper Broker Test")
print("==========================")

manager = BrokerManager()

print("\n🔹 Testing Exness...")
manager.select_broker("Exness")
manager.connect()
print("Status:", manager.status())
print("Price:", manager.get_price("XAUUSD"))

print("\n🔹 Testing Deriv...")
manager.select_broker("Deriv")
manager.connect()
print("Status:", manager.status())
print("Price:", manager.get_price("XAUUSD"))
