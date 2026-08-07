# ============================================
# Surge-Sniper
# AI Trading Command Center v4.0
# DEMO Trading Loop
# ============================================

import time
import config

from AI.engine import AIEngine
from MarketHunter.scanner import MarketHunter
from RiskCommander.risk import RiskCommander

from Brokers.broker_manager_v2 import BrokerManager
from Brokers.Exness.executor import ExnessExecutor

from Logs.trade_logger import TradeLogger
from Monitoring.position_monitor import PositionMonitor


def startup():

    ai = AIEngine()
    hunter = MarketHunter()
    risk = RiskCommander()
    broker = BrokerManager()
    executor = ExnessExecutor()
    logger = TradeLogger()
    monitor = PositionMonitor(executor)

    broker.select_broker("Exness")
    broker.connect()

    hunter.set_market("XAUUSD", "M15")

    print("=" * 50)
    print(f"        {config.BOT_NAME} v4.0")
    print("      AI TRADING COMMAND CENTER")
    print("=" * 50)

    print("\n🟢 System Status : ONLINE\n")

    cycles = 5

    for cycle in range(1, cycles + 1):

        print("\n==================================================")
        print(f"🔄 DEMO MARKET CYCLE {cycle}/{cycles}")
        print("==================================================")

        price = broker.get_price("XAUUSD")

        if price is None:
            print("❌ No market price")
            continue

        hunter.update_price(price)

        signal_data = hunter.scan_market()

        signal = signal_data["signal"]
        confidence = signal_data["confidence"]

        print("\n🛡️ RISK COMMANDER")
        print(f"Signal     : {signal}")
        print(f"Confidence : {confidence}%")

        approved = risk.approve_trade(
            signal,
            confidence
        )

        if approved:

            targets = risk.calculate_targets(
                price,
                signal
            )

            balance = 1000

            stop_loss_points = abs(
                targets["entry"] -
                targets["stop_loss"]
            )

            risk_report = risk.risk_report(
                balance,
                stop_loss_points
            )

            trade = executor.execute_trade(
                signal,
                "XAUUSD",
                targets["entry"],
                risk_report["lot_size"],
                targets["stop_loss"],
                targets["take_profit"]
            )

            if trade:

                monitor.open_position(
                    "XAUUSD",
                    signal,
                    targets["entry"],
                    targets["stop_loss"],
                    targets["take_profit"],
                    risk_report["lot_size"]
                )

                logger.log_trade(
                    "XAUUSD",
                    signal,
                    targets["entry"],
                    risk_report["lot_size"],
                    targets["stop_loss"],
                    targets["take_profit"]
                )

        else:

            print("Trade Status : REJECTED ❌")


        time.sleep(2)


    print("\n==================================================")
    print("DEMO LOOP COMPLETE")
    print("MODE :", config.MODE)
    print("BROKER :", config.BROKER)
    print("==================================================")


if __name__ == "__main__":
    startup()
