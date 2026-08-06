# ============================================
# Surge-Sniper
# Monitoring Status Engine v3.7.3
# ============================================

from datetime import datetime


def get_status():

    status = {
        "system": "ONLINE",
        "broker": "Exness",
        "market": "XAUUSD",
        "timeframe": "M15",
        "mode": "DEMO",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    return status
