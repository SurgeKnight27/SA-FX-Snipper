# ============================================
# Surge-Sniper App Launcher
# Version 3.7.3
# ============================================

import subprocess
import time
import webbrowser
import os
import json
import socket


BASE_DIR = os.path.dirname(__file__)
CONFIG_FILE = os.path.join(BASE_DIR, "config.json")


def load_config():
    with open(CONFIG_FILE, "r") as file:
        return json.load(file)


def dashboard_running():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect(("127.0.0.1", 5000))
        return True
    except:
        return False
    finally:
        sock.close()


def banner(config):
    print("=" * 50)
    print(f"        🚀 {config['app_name'].upper()}")
    print("             APP LAUNCHER ONLINE")
    print("=" * 50)
    print(f"Version: {config['version']}")
    print(f"Broker: {config['broker']}")
    print(f"Market: {config['symbol']}")
    print(f"Timeframe: {config['timeframe']}")
    print(f"Mode: {config['mode']}")
    print("=" * 50)


def start_dashboard(config):

    if dashboard_running():
        print("✅ Dashboard already running.")
    else:
        print("🌐 Starting Dashboard...")

        dashboard_path = os.path.join(
            BASE_DIR,
            "../../Dashboard/dashboard.py"
        )

        subprocess.Popen(
            ["python", dashboard_path]
        )

        time.sleep(4)

    print("📱 Opening Command Center...")
    webbrowser.open(config["dashboard"])


def main():
    config = load_config()
    banner(config)
    start_dashboard(config)
    print("✅ Surge-Sniper is running.")


if __name__ == "__main__":
    main()
