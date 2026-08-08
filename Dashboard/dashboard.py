# ============================================
# Surge-Sniper
# Dashboard API v5.4
# ============================================

import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, jsonify

from MarketHunter.scanner import MarketHunter
from Brokers.broker_manager_v2 import BrokerManager

app = Flask(__name__)

broker = BrokerManager()
broker.select_broker("Exness")
broker.connect()

hunter = MarketHunter()
hunter.set_market("XAUUSD", "M15")


@app.route("/")
def home():

    return """
    <h1>🚀 Surge-Sniper Dashboard</h1>
    <p>Dashboard API ONLINE</p>
    """


@app.route("/api/status")
def status():

    price = broker.get_price("XAUUSD")

    hunter.update_price(price)

    result = hunter.scan_market()

    return jsonify({
        "price": price,
        "trend": result["trend"],
        "signal": result["signal"],
        "confidence": result["confidence"],
        "broker": "Exness",
        "engine": "ONLINE",
        "mode": "DEMO"
    })


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
