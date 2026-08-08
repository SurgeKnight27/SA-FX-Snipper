# ============================================
# Surge-Sniper
# Market Data Stream v4.0
# LIVE PRICE STREAM
# ============================================

import requests
import time


class DataStream:

    def __init__(self):

        self.symbol = "XAUUSD"

        self.current_price = None

        self.last_update = 0

        self.api_url = (
            "https://api.twelvedata.com/price"
            "?symbol=XAU/USD"
            "&apikey=demo"
        )


    # ========================================
    # LIVE PRICE
    # ========================================

    def get_live_price(self):

        try:

            response = requests.get(
                self.api_url,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if "price" not in data:

                print("❌ Live price unavailable")
                print(data)

                return None

            price = float(data["price"])

            self.current_price = price

            self.last_update = time.time()

            print(
                f"📡 LIVE {self.symbol}: "
                f"{price}"
            )

            return price

        except Exception as e:

            print(
                f"❌ Live price error: {e}"
            )

            return None


    # ========================================
    # PRICE HISTORY
    # ========================================

    def get_prices(self):

        price = self.get_live_price()

        if price is None:

            return []

        return [price]


    # ========================================
    # NEXT PRICE
    # ========================================

    def next_price(self):

        return self.get_live_price()
