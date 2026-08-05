# ============================================
# Surge-Sniper
# AI Trading Command Center v3.7.0-alpha
# ============================================

import config
from AI.engine import AIEngine
from MarketHunter.scanner import MarketHunter
from RiskCommander.risk import RiskCommander
from Brokers.broker_manager_v2 import BrokerManager


def startup():

    ai = AIEngine()
    hunter = MarketHunter()
    risk = RiskCommander()
    broker = BrokerManager()

    broker.select_broker("Exness")
    broker.connect()

    price = broker.get_price("XAUUSD")

    print("=" * 50)
    print(f"        {config.BOT_NAME} v{config.VERSION}")
    print("      AI TRADING COMMAND CENTER")
    print("=" * 50)

    print("\n🟢 System Status : ONLINE\n")

    print("🧠 AI Engine.................READY")
    print("📈 Market Hunter............READY")
    print("🛡️ Risk Commander..........READY")
    print("🌍 Broker Manager...........READY")
    print("🎨 3D Dashboard............READY")

    hunter.set_market("XAUUSD", "M15")
    hunter.update_price(price)

    signal_data = hunter.scan_market()

    signal = signal_data["signal"]
    confidence = signal_data["confidence"]

    print("\n==================================================")
    print("🛡️ RISK COMMANDER")
    print("==================================================")

    approved = risk.approve_trade(signal, confidence)

    print(f"Signal        : {signal}")
    print(f"Confidence    : {confidence}%")

    if approved:

        targets = risk.calculate_targets(price, signal)

        print("Trade Status  : APPROVED ✅")
        print(f"Entry         : {targets['entry']}")
        print(f"Stop Loss     : {targets['stop_loss']}")
        print(f"Take Profit   : {targets['take_profit']}")
        print(f"Risk Reward   : {targets['risk_reward']}")

    else:

        print("Trade Status  : REJECTED ❌")


    print("\n==================================================")
    print(f"MODE : {config.MODE}")
    print(f"BROKER : {config.BROKER}")
    print(f"RISK : {config.RISK_PERCENT}%")

    print("\nWELCOME, COMMANDER! 🫡")
    print("MISSION STATUS : ACTIVE")
    print("Initializing future systems...")
    print("=" * 50)


if __name__ == "__main__":
    startup()
