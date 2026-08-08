# ============================================
# Surge-Sniper
# Dashboard API v6.0
# Market + Account Data
# ============================================

import os
import sys

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, jsonify

from MarketHunter.scanner import MarketHunter
from Brokers.broker_manager_v2 import BrokerManager


app = Flask(__name__)


# ============================================
# BROKER
# ============================================

broker = BrokerManager()

broker.select_broker("Exness")

broker.connect()


# ============================================
# MARKET HUNTER
# ============================================

hunter = MarketHunter()

hunter.set_market("XAUUSD", "M15")


# ============================================
# HOME
# ============================================

@app.route("/")
def home():

    return """
    <html>
        <head>
            <title>Surge-Sniper</title>
        </head>

        <body>
            <h1>🚀 Surge-Sniper Dashboard</h1>
            <p>Dashboard API ONLINE</p>
            <p>Market Hunter ONLINE</p>
            <p>Risk Commander ACTIVE</p>
            <p>Broker: Exness</p>
        </body>
    </html>
    """


# ============================================
# STATUS API
# ============================================

@app.route("/api/status")
def status():

    try:

        price = broker.get_price("XAUUSD")

        if price is not None:

            hunter.update_price(price)

            result = hunter.scan_market()

        else:

            result = {
                "trend": "--",
                "signal": "--",
                "confidence": "--"
            }


        return jsonify({

            "price": price if price is not None else "--",

            "trend": result.get(
                "trend",
                "--"
            ),

            "signal": result.get(
                "signal",
                "--"
            ),

            "confidence": result.get(
                "confidence",
                "--"
            ),

            "broker": "Exness",

            "engine": "ONLINE",

            "mode": "DEMO",

            "broker_status": broker.status()

        })


    except Exception as e:

        return jsonify({

            "price": "--",

            "trend": "--",

            "signal": "--",

            "confidence": "--",

            "broker": "Exness",

            "engine": "OFFLINE",

            "mode": "DEMO",

            "error": str(e)

        }), 500


# ============================================
# ACCOUNT API
# ============================================

@app.route("/api/account")
def account():

    try:

        active_broker = broker.active_broker

        if active_broker is None:

            return jsonify({

                "account_id": "--",
                "currency": "USD",
                "balance": 0.0,
                "equity": 0.0,
                "profit": 0.0,
                "margin": 0.0,
                "free_margin": 0.0,
                "margin_level": 0.0,
                "mode": "OFFLINE"

            })


        if hasattr(active_broker, "get_account"):

            account_data = active_broker.get_account()

            return jsonify(account_data)


        return jsonify({

            "account_id": "--",
            "currency": "USD",
            "balance": 0.0,
            "equity": 0.0,
            "profit": 0.0,
            "margin": 0.0,
            "free_margin": 0.0,
            "margin_level": 0.0,
            "mode": "DEMO"

        })


    except Exception as e:

        return jsonify({

            "account_id": "--",
            "currency": "USD",
            "balance": 0.0,
            "equity": 0.0,
            "profit": 0.0,
            "margin": 0.0,
            "free_margin": 0.0,
            "margin_level": 0.0,
            "mode": "OFFLINE",
            "error": str(e)

        }), 500


# ============================================
# SERVER
# ============================================

if __name__ == "__main__":

    print("============================================")
    print("🚀 SURGE-SNIPER DASHBOARD API")
    print("============================================")
    print("🌍 Host     : 0.0.0.0")
    print("🔌 Port     : 5001")
    print("📈 Market   : XAUUSD")
    print("🏦 Broker   : Exness")
    print("📊 API      : ONLINE")
    print("============================================")

    app.run(
        host="0.0.0.0",
        port=5001,
        debug=False
    )
