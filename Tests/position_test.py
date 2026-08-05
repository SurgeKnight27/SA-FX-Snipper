# ============================================
# Surge-Sniper
# Position Management Test v1.1
# DEMO TP/SL Simulation
# ============================================

import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

from Brokers.Exness.executor import ExnessExecutor
from Monitoring.position_monitor import PositionMonitor
from Logs.trade_history import TradeHistory


def run_test():

    print("\n🚀 POSITION MANAGEMENT TEST")
    print("=" * 50)

    executor = ExnessExecutor()
    history = TradeHistory()

    monitor = PositionMonitor(
        executor=executor,
        history=history
    )

    executor.execute_trade(
        "BUY",
        "XAUUSD",
        3375.5,
        0.01,
        3365.5,
        3395.5
    )

    monitor.open_position(
        "XAUUSD",
        "BUY",
        3375.5,
        3365.5,
        3395.5,
        0.01
    )

    print("\n📈 TEST 1: TAKE PROFIT")
    print("=" * 50)

    monitor.check_position(3396)

    print("\n📉 TEST 2: STOP LOSS")
    print("=" * 50)

    monitor.open_position(
        "XAUUSD",
        "BUY",
        3375.5,
        3365.5,
        3395.5,
        0.01
    )

    monitor.check_position(3365)

    print("\n📚 TRADE HISTORY")
    print("=" * 50)

    if hasattr(history, "show_history"):
        history.show_history()

    if hasattr(history, "performance_report"):
        history.performance_report()


if __name__ == "__main__":
    run_test()
