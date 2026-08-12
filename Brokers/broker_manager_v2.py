# ============================================
# Surge-Sniper
# Broker Manager v2.0
# MT5API Execution Bridge
# ============================================

from Brokers.MetaApi.metaapi import MetaApiBroker


class BrokerManager:

    # ========================================
    # INITIALIZATION
    # ========================================

    def __init__(self):

        self.active_broker = None
        self.active_broker_name = None

        self.brokers = {
            "MT5API": MetaApiBroker()
        }

    # ========================================
    # SELECT BROKER
    # ========================================

    def select_broker(self, broker_name):

        broker_name = str(
            broker_name
        ).upper()

        if broker_name not in self.brokers:

            print(
                f"❌ Unsupported broker: "
                f"{broker_name}"
            )

            return False

        self.active_broker_name = broker_name
        self.active_broker = self.brokers[
            broker_name
        ]

        print(
            f"✅ Broker selected: "
            f"{broker_name}"
        )

        return True

    # ========================================
    # CONNECT
    # ========================================

    def connect(self):

        if not self.active_broker:

            print(
                "❌ No broker selected."
            )

            return False

        return self.active_broker.connect()

    # ========================================
    # DISCONNECT
    # ========================================

    def disconnect(self):

        if self.active_broker:

            return self.active_broker.disconnect()

        return True

    # ========================================
    # STATUS
    # ========================================

    def status(self):

        if self.active_broker:

            return self.active_broker.status()

        return "OFFLINE"

    # ========================================
    # ACCOUNT
    # ========================================

    def get_account(self):

        if self.active_broker:

            return self.active_broker.get_account()

        print(
            "❌ No broker selected."
        )

        return None

    # ========================================
    # ACCOUNTS
    # ========================================

    def get_accounts(self):

        if self.active_broker and hasattr(
            self.active_broker,
            "get_accounts"
        ):

            return self.active_broker.get_accounts()

        return []

    # ========================================
    # ACCOUNT SNAPSHOT
    # ========================================

    def get_account_snapshot(self):

        if self.active_broker and hasattr(
            self.active_broker,
            "get_account_snapshot"
        ):

            return (
                self.active_broker
                .get_account_snapshot()
            )

        return self.get_account()

    # ========================================
    # POSITIONS
    # ========================================

    def get_positions(self):

        if self.active_broker and hasattr(
            self.active_broker,
            "get_positions"
        ):

            return (
                self.active_broker
                .get_positions()
            )

        # Position state is UNKNOWN if the broker cannot provide it.
        # Never convert UNKNOWN into an empty position list.
        print(
            "⚠️ Position state UNKNOWN: "
            "broker does not support position retrieval."
        )

        return None

    # ========================================
    # QUOTES
    # ========================================

    def get_quotes(
        self,
        symbols=None
    ):

        if self.active_broker and hasattr(
            self.active_broker,
            "get_quotes"
        ):

            return (
                self.active_broker
                .get_quotes(symbols)
            )

        return []

    # ========================================
    # PRICE
    # ========================================

    def get_price(self, symbol):

        if self.active_broker and hasattr(
            self.active_broker,
            "get_price"
        ):

            return (
                self.active_broker
                .get_price(symbol)
            )

        return None

    # ========================================
    # EXECUTE TRADE
    # ========================================

    def execute_trade(
        self,
        signal,
        symbol,
        volume,
        stop_loss=None,
        take_profit=None
    ):

        if not self.active_broker:

            print(
                "❌ No broker selected."
            )

            return None

        if not hasattr(
            self.active_broker,
            "execute_trade"
        ):

            print(
                f"❌ {self.active_broker_name} "
                "does not support execution."
            )

            return None

        return self.active_broker.execute_trade(
            signal,
            symbol,
            volume,
            stop_loss,
            take_profit
        )
