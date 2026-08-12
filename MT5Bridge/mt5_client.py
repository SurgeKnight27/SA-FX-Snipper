# ============================================
# Surge-Sniper
# MT5 Bridge Client v1.1
# SAFE CLIENT - NO ORDER EXECUTION
# ============================================

import requests


class MT5Client:

    def __init__(self, bridge_url="http://127.0.0.1:5002"):

        self.bridge_url = bridge_url.rstrip("/")
        self.connected = False

    def connect(self):

        try:

            response = requests.get(
                f"{self.bridge_url}/api/status",
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            if data.get("bridge") == "ONLINE":

                self.connected = True

                print("✅ MT5 Bridge reachable")

                return True

            print("❌ MT5 Bridge unavailable")

            return False

        except requests.RequestException as error:

            print(f"❌ MT5 Bridge connection error: {error}")

            return False

    def status(self):

        if not self.connected:

            return "DISCONNECTED"

        try:

            response = requests.get(
                f"{self.bridge_url}/api/status",
                timeout=5
            )

            response.raise_for_status()

            data = response.json()

            return (
                f"Bridge={data.get('bridge')} | "
                f"MT5={data.get('mt5')} | "
                f"Trading={data.get('trading')} | "
                f"Mode={data.get('mode')}"
            )

        except requests.RequestException as error:

            return f"ERROR: {error}"

    def get_account(self):

        if not self.connected:

            print("❌ MT5 Bridge not connected")

            return None

        try:

            response = requests.get(
                f"{self.bridge_url}/api/account",
                timeout=5
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:

            print(f"❌ Account request failed: {error}")

            return None
