# ============================================
# Surge-Sniper
# Exness Broker v4.1
# DEMO Market Tick Stream
# ============================================


class ExnessBroker:

    def __init__(self):

        self.connected = False
        self.name = "Exness"

        self.tick_index = 0

        self.market_ticks = {

            "XAUUSD": [
                3375.50,
                3375.80,
                3376.20,
                3375.90,
                3377.10,
                3377.80,
                3378.40,
                3377.60,
                3379.20,
                3380.10,
                3379.70,
                3381.00
            ],

            "EURUSD": [
                1.1650,
                1.1652,
                1.1655,
                1.1653,
                1.1658
            ],

            "GBPUSD": [
                1.3420,
                1.3423,
                1.3426,
                1.3424,
                1.3430
            ]

        }


    def connect(self):

        print("🌍 Connecting to Exness...")

        self.connected = True

        print("✅ Connected to Exness")

        return True



    def disconnect(self):

        print("🔌 Disconnecting from Exness...")

        self.connected = False

        print("✅ Disconnected")



    def get_price(self, symbol):

        if not self.connected:

            print("❌ Exness not connected")

            return None


        print(f"📈 Requesting {symbol} price...")


        if symbol not in self.market_ticks:

            return None


        prices = self.market_ticks[symbol]


        price = prices[self.tick_index]


        self.tick_index += 1


        if self.tick_index >= len(prices):

            self.tick_index = 0


        return price



    def status(self):

        return "ONLINE" if self.connected else "OFFLINE"
