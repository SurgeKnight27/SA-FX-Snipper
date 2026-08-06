# ============================================
# Surge-Sniper
# AI Trading Command Center Dashboard v3.7.3
# ============================================

import sys
import os

from flask import Flask, render_template_string

# Allow Dashboard to access project modules
sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from Monitoring.status import get_status


app = Flask(__name__)


PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))


HTML = """
<!DOCTYPE html>
<html>

<head>

<title>Surge-Sniper Command Center</title>

<style>

body {
    background:#050505;
    color:white;
    font-family:Arial, sans-serif;
    text-align:center;
}

.logo {
    width:180px;
    border-radius:20px;
    margin-top:25px;
    box-shadow:0 0 25px #00ff99;
}

.card {
    background:#111;
    border-radius:20px;
    padding:20px;
    margin:20px auto;
    width:85%;
    box-shadow:0 0 15px #222;
}

.green {
    color:#00ff99;
}

.gold {
    color:#FFD700;
}

.line {
    border-top:1px solid #333;
    margin:15px;
}

</style>

</head>


<body>


<img class="logo" src="/static/logo.jpg">


<h1>🚀 Surge-Sniper</h1>

<h2 class="gold">
AI TRADING COMMAND CENTER
</h2>



<div class="card">

<h2 class="green">
SYSTEM ONLINE ✅
</h2>

<div class="line"></div>

<p>Version: {{status["version"]}}</p>

<p>Broker: {{status["broker"]}}</p>

<p>Market: {{status["market"]}}</p>

<p>Timeframe: {{status["timeframe"]}}</p>

<p>Mode: {{status["mode"]}}</p>

</div>



<div class="card">

<h2>📊 Market Hunter</h2>

<p>Status: READY ✅</p>

<p>Scanner: ACTIVE</p>

<p>Signal Engine: ONLINE</p>

<p>AI Analysis: STANDBY</p>

</div>



<div class="card">

<h2>🛡️ Risk Commander</h2>

<p>Risk Management: READY</p>

<p>Trade Approval: ENABLED</p>

<p>Protection System: ACTIVE</p>

</div>



<div class="card">

<h2>⚡ Mission Status</h2>

<p class="green">
SURGE-SNIPER IS OPERATIONAL
</p>

<p>
Awaiting Market Opportunity...
</p>

</div>



</body>

</html>
"""


@app.route("/")
def dashboard():

    status = get_status()

    return render_template_string(
        HTML,
        status=status
    )


if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )
