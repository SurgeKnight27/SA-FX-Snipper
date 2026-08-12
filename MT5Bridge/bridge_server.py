# ============================================
# Surge-Sniper
# MT5 Bridge Server v1.2
# DEMO GATE
# ============================================

from flask import Flask, jsonify


app = Flask(__name__)


BRIDGE_STATUS = "ONLINE"
MT5_STATUS = "NOT_CONNECTED"
TRADING_MODE = "DEMO"
TRADING_UNLOCKED = False


@app.route("/")
def home():

    return jsonify({
        "service": "Surge-Sniper MT5 Bridge",
        "version": "1.2",
        "bridge": BRIDGE_STATUS,
        "mt5": MT5_STATUS,
        "mode": TRADING_MODE,
        "trading_unlocked": TRADING_UNLOCKED
    })


@app.route("/api/status")
def status():

    return jsonify({
        "bridge": BRIDGE_STATUS,
        "mt5": MT5_STATUS,
        "mode": TRADING_MODE,
        "trading": "UNLOCKED" if TRADING_UNLOCKED else "LOCKED"
    })


@app.route("/api/unlock-demo", methods=["POST"])
def unlock_demo():

    global TRADING_UNLOCKED

    if MT5_STATUS != "CONNECTED":

        return jsonify({
            "success": False,
            "message": "MT5 is not connected. DEMO execution remains locked."
        }), 409

    TRADING_UNLOCKED = True

    return jsonify({
        "success": True,
        "message": "DEMO execution unlocked.",
        "trading": "UNLOCKED",
        "mode": "DEMO"
    })


@app.route("/api/lock", methods=["POST"])
def lock_trading():

    global TRADING_UNLOCKED

    TRADING_UNLOCKED = False

    return jsonify({
        "success": True,
        "message": "Trading locked.",
        "trading": "LOCKED"
    })


if __name__ == "__main__":

    print("==================================================")
    print("      SURGE-SNIPPER MT5 BRIDGE v1.2")
    print("==================================================")
    print("Bridge Status : ONLINE")
    print("MT5 Status    : NOT CONNECTED")
    print("Trading       : LOCKED")
    print("Mode          : DEMO")
    print("Port          : 5002")
    print("==================================================")

    app.run(
        host="0.0.0.0",
        port=5002,
        debug=False
    )
