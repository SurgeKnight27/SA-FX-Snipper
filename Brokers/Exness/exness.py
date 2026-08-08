# ============================================
# Surge-Sniper
# Exness Broker v6.0
# LIVE XAUUSD MARKET DATA
# ============================================

import requests


class ExnessBroker:

    def __init__(self):

        self.connected = False
        self.name = "Exness"

        self.price_url = "https://api.gold-api.com/price/XAU"

        # ------------------------------------
        # ACCOUNT DATA
        # ------------------------------------
        # Execution remains DEMO until the
        # Exness MT5 bridge is connected.
        #
        # Market price below is LIVE XAU data.
        # ------------------------------------

        self.account_data = {

            "account_id": "--",
            "currency": "USD",
            "balance": 0.00,
            "equity": 0.00,
            "profit": 0.00,
            "margin": 0.00,
            "free_margin": 0.00,
            "margin_level": 0.00,
            "mode": "DEMO"

        }


    # ========================================
    # CONNECTION
    # ========================================

    def connect(self):

        print("🌍 Connecting to Exness...")

        self.connected = True

        print("✅ Exness broker layer ONLINE")
        print("📡 LIVE XAUUSD market feed enabled")

        return True


    def disconnect(self):

        print("🔌 Disconnecting from Exness...")

        self.connected = False

        print("✅ Disconnected")


    # ========================================
    # LIVE MARKET PRICE
    # ========================================

    def get_price(self, symbol):

        if not self.connected:

            print("❌ Exness not connected")

            return None


        if symbol != "XAUUSD":

            print(f"❌ Unsupported symbol: {symbol}")

            return None


        try:

            response = requests.get(
                self.price_url,
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            if "price" not in data:

                print("❌ Live XAU price unavailable")
                print(data)

                return None


            price = float(data["price"])


            print("📡 LIVE XAUUSD")
            print(f"💰 Price: {price}")
            print(
                f"🕒 Updated: "
                f"{data.get('updatedAtReadable', 'unknown')}"
            )


            return price


        except Exception as e:

            print(f"❌ Live XAU price error: {e}")

            return None


    # ========================================
    # ACCOUNT DATA
    # ========================================

    def get_account(self):

        if not self.connected:

            print("❌ Exness not connected")

            return None


        print("💰 Requesting Exness account data...")

        return self.account_data.copy()


    # ========================================
    # BROKER STATUS
    # ========================================

    def status(self):

        return "ONLINE" if self.connected else "OFFLINE"


