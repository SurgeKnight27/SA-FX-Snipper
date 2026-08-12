# ============================================
# Surge-Sniper
# Dashboard API v10.2
# PERSISTENT MARKET HUNTER
# BACKGROUND M15 COLLECTOR
# LIVE MT5API + LOCAL M15 ENGINE
# ============================================

import os
import sys
import time
import threading

# ============================================
# PROJECT ROOT
# ============================================

PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

sys.path.insert(0, PROJECT_ROOT)

# ============================================
# IMPORTS
# ============================================

from flask import Flask, jsonify
from MarketHunter.scanner import MarketHunter

# ============================================
# FLASK
# ============================================

app = Flask(__name__)

# ============================================
# MARKET HUNTER
# ============================================

hunter = MarketHunter()

hunter.set_market(
    "BTCUSDm",
    "M15"
)

hunter_loaded = False

# ============================================
# THREAD CONTROL
# ============================================

collector_started = False

hunter_lock = threading.RLock()

COLLECTOR_INTERVAL = 5


# ============================================
# MARKET HUNTER STARTUP
# ============================================

def ensure_hunter():

    global hunter_loaded

    with hunter_lock:

        if hunter_loaded:
            return True

        try:

            hunter_loaded = hunter.load()

            if hunter_loaded:

                print(
                    "✅ Market Hunter Loaded "
                    "and ready for background collection."
                )

            return hunter_loaded

        except Exception as e:

            print(
                f"❌ Market Hunter startup error: {e}"
            )

            hunter_loaded = False

            return False


# ============================================
# BACKGROUND M15 MARKET COLLECTOR
# ============================================

def market_collector():

    print(
        "============================================"
    )

    print(
        "📡 BACKGROUND M15 MARKET COLLECTOR"
    )

    print(
        "============================================"
    )

    while True:

        try:

            if not ensure_hunter():

                print(
                    "⚠️ Market Hunter unavailable. "
                    "Collector retrying..."
                )

                time.sleep(
                    COLLECTOR_INTERVAL
                )

                continue

            with hunter_lock:

                price = (
                    hunter.update_from_broker()
                )

                stream_status = (
                    hunter.data_stream.status()
                )

                samples = stream_status.get(
                    "samples",
                    0
                )

            if price is not None:

                print(
                    "📡 Background quote: "
                    f"{price} | "
                    f"Completed M15 candles: "
                    f"{samples}"
                )

            else:

                print(
                    "⚠️ Background collector "
                    "received no live price."
                )

        except Exception as e:

            print(
                "❌ Background collector error: "
                f"{e}"
            )

        time.sleep(
            COLLECTOR_INTERVAL
        )


# ============================================
# START BACKGROUND COLLECTOR
# ============================================

def start_market_collector():

    global collector_started

    if collector_started:

        return

    collector_started = True

    thread = threading.Thread(
        target=market_collector,
        name="SurgeSniper-M15-Collector",
        daemon=True
    )

    thread.start()

    print(
        "✅ Background M15 collector started."
    )


# ============================================
# MAIN DASHBOARD
# ============================================

@app.route("/")
def home():

    return """
<!DOCTYPE html>

<html lang="en">

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width,
               initial-scale=1.0">

<title>
Surge-Sniper Dashboard
</title>

<style>

* {
    box-sizing: border-box;
}

body {

    margin: 0;

    background: #080c14;

    color: #f8fafc;

    font-family: Arial, sans-serif;
}

.header {

    padding: 20px;

    text-align: center;

    border-bottom: 1px solid #263044;

    background: #0d111a;
}

.header img {

    width: 80px;

    height: 80px;

    object-fit: contain;

    border-radius: 16px;

    margin-bottom: 8px;
}

.header h1 {

    margin: 5px 0;

    font-size: 26px;
}

.header p {

    margin: 5px 0;

    color: #94a3b8;
}

.container {

    width: 94%;

    max-width: 1100px;

    margin: 20px auto;
}

/* =========================================
   NAVIGATION
========================================= */

.navigation {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 10px;

    margin-bottom: 20px;
}

.nav-button {

    display: block;

    text-decoration: none;

    text-align: center;

    padding: 14px 8px;

    border-radius: 12px;

    background: #151b28;

    color: #f8fafc;

    border: 1px solid #293449;

    font-weight: bold;
}

.nav-button:hover {

    background: #20293a;
}

/* =========================================
   ACCOUNT CARDS
========================================= */

.cards {

    display: grid;

    grid-template-columns:
        repeat(3, 1fr);

    gap: 12px;
}

.card {

    background: #111722;

    border: 1px solid #263044;

    border-radius: 14px;

    padding: 18px;
}

.card-title {

    color: #94a3b8;

    font-size: 13px;

    margin-bottom: 8px;
}

.card-value {

    font-size: 24px;

    font-weight: bold;
}

/* =========================================
   SECTIONS
========================================= */

.section {

    margin-top: 15px;
}

.row {

    display: flex;

    justify-content: space-between;

    padding: 10px 0;

    border-bottom:
        1px solid #202838;
}

.label {

    color: #94a3b8;
}

.value {

    font-weight: bold;
}

.signal {

    font-size: 28px;

    font-weight: bold;

    text-align: center;

    padding: 15px;
}

.footer {

    text-align: center;

    padding: 25px;

    color: #64748b;

    font-size: 12px;
}

/* =========================================
   MOBILE
========================================= */

@media (max-width: 700px) {

    .navigation {

        grid-template-columns: 1fr;
    }

    .cards {

        grid-template-columns: 1fr;
    }

}

</style>

</head>

<body>

<!-- ======================================
     HEADER
======================================= -->

<div class="header">

    <img
        src="/static/logo.jpg"
        alt="Surge-Sniper"
    >

    <h1>
        🚀 Surge-Sniper
    </h1>

    <p>
        MT5API Live Trading Dashboard
    </p>

    <p>
        BTCUSDm • M15
    </p>

</div>


<div class="container">


<!-- ======================================
     NAVIGATION
======================================= -->

<div class="navigation">

    <a
        class="nav-button"
        href="#market"
    >
        📊 Charts
    </a>

    <a
        class="nav-button"
        href="#news"
    >
        📰 Newsreel
    </a>

    <a
        class="nav-button"
        href="#account"
    >
        💼 Account
    </a>

</div>


<!-- ======================================
     ACCOUNT
======================================= -->

<div
    class="cards"
    id="account"
>

    <div class="card">

        <div class="card-title">
            💰 BALANCE
        </div>

        <div
            class="card-value"
            id="balance"
        >
            --
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            📊 EQUITY
        </div>

        <div
            class="card-value"
            id="equity"
        >
            --
        </div>

    </div>


    <div class="card">

        <div class="card-title">
            💵 PROFIT
        </div>

        <div
            class="card-value"
            id="profit"
        >
            --
        </div>

    </div>

</div>


<!-- ======================================
     MARKET / CHARTS
======================================= -->

<div
    class="card section"
    id="market"
>

    <h2>
        📈 Market Hunter
    </h2>


    <div class="row">

        <span class="label">
            Price
        </span>

        <span
            class="value"
            id="price"
        >
            --
        </span>

    </div>


    <div class="row">

        <span class="label">
            Symbol
        </span>

        <span
            class="value"
            id="symbol"
        >
            BTCUSDm
        </span>

    </div>


    <div class="row">

        <span class="label">
            Timeframe
        </span>

        <span
            class="value"
            id="timeframe"
        >
            M15
        </span>

    </div>


    <div class="row">

        <span class="label">
            Trend
        </span>

        <span
            class="value"
            id="trend"
        >
            WAITING
        </span>

    </div>


    <div class="row">

        <span class="label">
            Confidence
        </span>

        <span
            class="value"
            id="confidence"
        >
            0%
        </span>

    </div>


    <div class="row">

        <span class="label">
            Broker
        </span>

        <span
            class="value"
            id="broker"
        >
            MT5API
        </span>

    </div>


    <div class="row">

        <span class="label">
            Feed
        </span>

        <span
            class="value"
            id="feed"
        >
            OFFLINE
        </span>

    </div>


    <div class="row">

        <span class="label">
            Engine
        </span>

        <span
            class="value"
            id="engine"
        >
            OFFLINE
        </span>

    </div>


    <div class="row">

        <span class="label">
            M15 Candles
        </span>

        <span
            class="value"
            id="samples"
        >
            0 / 20
        </span>

    </div>


    <div
        class="signal"
        id="signal"
    >
        HOLD
    </div>

</div>


<!-- ======================================
     NEWSREEL
======================================= -->

<div
    class="card section"
    id="news"
>

    <h2>
        📰 Newsreel
    </h2>

    <p>
        Market news integration ready.
    </p>

    <p class="label">
        News feed will appear here when
        the news module is connected.
    </p>

</div>


<!-- ======================================
     FOOTER
======================================= -->

<div class="footer">

    Surge-Sniper v10.2<br>

    MT5API • Market Hunter • M15

</div>


</div>


<!-- ======================================
     JAVASCRIPT
======================================= -->

<script>

function setValue(id, value) {

    const element =
        document.getElementById(id);

    if (element) {

        element.textContent =
            value ?? "--";

    }

}


/* ========================================
   ACCOUNT UPDATE
======================================== */

async function updateAccount() {

    try {

        const response =
            await fetch(
                "/api/account"
            );

        if (!response.ok) {

            return;

        }

        const data =
            await response.json();


        setValue(
            "balance",
            data.balance !== undefined
                ? Number(
                    data.balance
                  ).toFixed(2)
                : "--"
        );


        setValue(
            "equity",
            data.equity !== undefined
                ? Number(
                    data.equity
                  ).toFixed(2)
                : "--"
        );


        setValue(
            "profit",
            data.profit !== undefined
                ? Number(
                    data.profit
                  ).toFixed(2)
                : "--"
        );

    }

    catch (error) {

        console.log(
            "Account update failed"
        );

    }

}


/* ========================================
   STATUS UPDATE
======================================== */

async function updateStatus() {

    try {

        const response =
            await fetch(
                "/api/status"
            );

        const data =
            await response.json();


        setValue(
            "price",
            data.price
        );


        setValue(
            "symbol",
            data.symbol
        );


        setValue(
            "timeframe",
            data.timeframe
        );


        setValue(
            "trend",
            data.trend
        );


        setValue(
            "confidence",
            String(
                data.confidence ?? 0
            ) + "%"
        );


        setValue(
            "broker",
            data.broker
        );


        setValue(
            "feed",
            data.feed
        );


        setValue(
            "engine",
            data.engine
        );


        setValue(
            "samples",
            String(
                data.samples ?? 0
            ) + " / 20"
        );


        setValue(
            "signal",
            data.signal
        );

    }

    catch (error) {

        console.log(
            "Status update failed"
        );

    }

}


/* ========================================
   DASHBOARD REFRESH
======================================== */

async function refreshDashboard() {

    await updateAccount();

    await updateStatus();

}


refreshDashboard();


setInterval(
    refreshDashboard,
    5000
);

</script>

</body>

</html>
"""


# ============================================
# ACCOUNT API
# ============================================

@app.route("/api/account")
def account():

    try:

        if not ensure_hunter():

            return jsonify({
                "balance": None,
                "equity": None,
                "profit": None,
                "status": "OFFLINE"
            })

        with hunter_lock:

            account_data = (
                hunter.data_stream.broker
                .get_account()
            )

        if not isinstance(
            account_data,
            dict
        ):

            return jsonify({
                "balance": None,
                "equity": None,
                "profit": None,
                "status": "UNKNOWN"
            })

        balance = account_data.get(
            "balance"
        )

        equity = account_data.get(
            "equity"
        )

        profit = account_data.get(
            "profit"
        )

        return jsonify({

            "balance": balance,

            "equity": equity,

            "profit": profit,

            "status": "ONLINE"

        })

    except Exception as e:

        print(
            "⚠️ Account dashboard error: "
            f"{e}"
        )

        return jsonify({

            "balance": None,

            "equity": None,

            "profit": None,

            "status": "ERROR"

        })


# ============================================
# STATUS API
# ============================================

@app.route("/api/status")
def status():

    try:

        if not ensure_hunter():

            return jsonify({

                "price": "--",

                "symbol": "BTCUSDm",

                "timeframe": "M15",

                "trend": "OFFLINE",

                "signal": "HOLD",

                "confidence": 0,

                "broker": "MT5API",

                "broker_status": "OFFLINE",

                "feed": "OFFLINE",

                "engine": "OFFLINE",

                "mode": "DEMO",

                "samples": 0,

                "ready": False

            })


        with hunter_lock:

            # ====================================
            # MARKET SCAN
            # ====================================

            result = hunter.scan()


            # ====================================
            # DATA STREAM STATUS
            # ====================================

            stream_status = (
                hunter.data_stream.status()
            )


            connected = (
                stream_status.get(
                    "connected"
                )
                == "ONLINE"
            )


            samples = (
                stream_status.get(
                    "samples",
                    0
                )
            )


            current_price = (
                stream_status.get(
                    "price"
                )
            )


            if current_price is None:

                current_price = hunter.price


        return jsonify({

            "price": (
                current_price
                if current_price is not None
                else "--"
            ),

            "symbol":
                hunter.symbol,

            "timeframe":
                hunter.timeframe,

            "trend":
                result.get(
                    "trend",
                    "WAITING"
                ),

            "signal":
                result.get(
                    "signal",
                    "HOLD"
                ),

            "confidence":
                result.get(
                    "confidence",
                    0
                ),

            "broker":
                "MT5API",

            "broker_status":
                (
                    "ONLINE"
                    if connected
                    else "OFFLINE"
                ),

            "feed":
                (
                    "LIVE"
                    if current_price
                    is not None
                    else "OFFLINE"
                ),

            "engine":
                (
                    "ONLINE"
                    if connected
                    else "OFFLINE"
                ),

            "mode":
                "DEMO",

            "samples":
                samples,

            "ready":
                result.get(
                    "ready",
                    False
                )

        })

    except Exception as e:

        print(
            "❌ Status API error: "
            f"{e}"
        )

        return jsonify({

            "price": "--",

            "symbol": "BTCUSDm",

            "timeframe": "M15",

            "trend": "ERROR",

            "signal": "HOLD",

            "confidence": 0,

            "broker": "MT5API",

            "broker_status": "UNKNOWN",

            "feed": "UNKNOWN",

            "engine": "UNKNOWN",

            "mode": "DEMO",

            "samples": 0,

            "ready": False

        })


# ============================================
# STARTUP
# ============================================

start_market_collector()


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    print(
        "============================================"
    )

    print(
        "🚀 SURGE-SNIPER DASHBOARD v10.2"
    )

    print(
        "============================================"
    )

    print(
        "📡 Feed     : MT5API"
    )

    print(
        "📈 Market   : BTCUSDm"
    )

    print(
        "⏱️ Timeframe: M15"
    )

    print(
        "🏦 Broker   : MT5API"
    )

    print(
        "💰 Account  : API ENABLED"
    )

    print(
        "⚙️ Engine   : ONLINE"
    )

    print(
        "📡 Collector: BACKGROUND"
    )

    print(
        "============================================"
    )

    print(
        "🌐 Dashboard: "
        "http://127.0.0.1:5000"
    )

    print(
        "============================================"
    )

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
