# ============================================
# Surge-Sniper
# MT5API Execution Bridge v6.0
# ============================================

import os
import uuid
import time
import requests

from dotenv import load_dotenv


load_dotenv()


class MetaApiBroker:

    BASE_URL = "https://api.mt5api.dev/v1"

    def __init__(self):

        self.api_key = os.getenv(
            "MT5API_KEY"
        )

        self.connected = False

        self.accounts = []

        self.account = None

    # ========================================
    # HEADERS
    # ========================================

    def _headers(
        self,
        idempotency_key=None
    ):

        headers = {

            "Authorization":
                f"Bearer {self.api_key}",

            "Content-Type":
                "application/json"

        }

        if idempotency_key:

            headers[
                "Idempotency-Key"
            ] = idempotency_key

        return headers

    # ========================================
    # CONNECT
    # ========================================

    def connect(self):

        # Always begin from a locked/disconnected state.
        self.connected = False

        if not self.api_key:

            print(
                "❌ MT5API_KEY is not configured."
            )

            return False

        try:

            response = requests.get(

                f"{self.BASE_URL}/accounts",

                headers=self._headers(),

                timeout=15
            )

            if response.status_code != 200:

                print(
                    "❌ MT5API connection failed: "
                    f"HTTP {response.status_code}"
                )

                print(
                    response.text[:1000]
                )

                return False

            data = response.json()

            self.accounts = data.get(
                "data",
                []
            )

            if not self.accounts:

                print(
                    "❌ No MT5API accounts found."
                )

                return False

            self.account = (
                self.accounts[0]
            )

            account_status = str(
                self.account.get(
                    "status",
                    ""
                )
            ).strip().lower()

            print(
                "📡 MT5API account connection state: "
                f"{account_status or 'unknown'}"
            )

            # ====================================
            # CONNECTION STATE GUARD
            #
            # HTTP 200 from /accounts only proves
            # that the API request succeeded.
            #
            # It does NOT prove that the MT5
            # broker account is connected.
            # ====================================

            connected_states = (
                "active",
                "connected",
                "online"
            )

            if account_status not in connected_states:

                self.connected = False

                print(
                    "⚠️ MT5API account is NOT connected."
                )

                print(
                    f"Account status: "
                    f"{self.account.get('status', 'Unknown')}"
                )

                print(
                    "🔒 Trading remains locked."
                )

                return False

            self.connected = True

            print(
                "✅ MT5API connection verified."
            )

            print(
                f"Accounts found: "
                f"{len(self.accounts)}"
            )

            print(
                f"Account label: "
                f"{self.account.get('label', 'Unknown')}"
            )

            print(
                f"Account status: "
                f"{self.account.get('status', 'Unknown')}"
            )

            print(
                f"Account mode: "
                f"{self.account.get('mode', 'Unknown')}"
            )

            return True

        except requests.RequestException as e:

            self.connected = False

            print(
                f"❌ MT5API network error: {e}"
            )

            return False

        except ValueError as e:

            self.connected = False

            print(
                f"❌ MT5API returned invalid JSON: {e}"
            )

            return False

    # ========================================
    # ACCOUNT SUMMARY
    # ========================================

    def refresh_account_summary(self):

        if not self.connected:

            return None

        if not self.account:

            return None

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            return None

        try:

            url = (
                f"{self.BASE_URL}/accounts/"
                f"{account_id}/summary"
            )

            response = requests.get(

                url,

                headers=self._headers(),

                timeout=15
            )

            if response.status_code != 200:

                print(
                    "❌ Account summary failed: "
                    f"HTTP {response.status_code}"
                )

                print(
                    response.text[:1000]
                )

                return None

            data = response.json()

            summary = data.get(
                "data",
                {}
            )

            for field in (

                "currency",
                "balance",
                "equity",
                "margin",
                "free_margin",
                "margin_level",
                "credit",
                "profit",
                "leverage"

            ):

                if field in summary:

                    self.account[field] = (
                        summary[field]
                    )

            return summary

        except requests.RequestException as e:

            print(
                "❌ MT5API account summary "
                f"network error: {e}"
            )

            return None

    # ========================================
    # DISCONNECT
    # ========================================

    def disconnect(self):

        self.connected = False

        self.accounts = []

        self.account = None

        print(
            "🔌 MT5API disconnected."
        )

        return True

    # ========================================
    # STATUS
    # ========================================

    def status(self):

        return (
            "ONLINE"
            if self.connected
            else "OFFLINE"
        )

    # ========================================
    # ACCOUNT
    # ========================================

    def get_account(self):

        if not self.connected:

            return None

        self.refresh_account_summary()

        return self.account

    # ========================================
    # ACCOUNTS
    # ========================================

    def get_accounts(self):

        if self.connected:

            return self.accounts

        return []

    # ========================================
    # ACCOUNT SNAPSHOT
    # ========================================

    def get_account_snapshot(self):

        return self.get_account()

    # ========================================
    # POSITIONS
    # ========================================

    def get_positions(self):

        # None means UNKNOWN.
        # [] means API confirmed zero positions.

        if (
            not self.connected
            or not self.account
        ):

            print(
                "⚠️ MT5API position state UNKNOWN: "
                "broker is not connected."
            )

            return None

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            print(
                "⚠️ MT5API position state UNKNOWN: "
                "no account ID."
            )

            return None

        try:

            response = requests.get(

                f"{self.BASE_URL}/accounts/"
                f"{account_id}/positions",

                headers=self._headers(),

                timeout=15
            )

            if response.status_code == 200:

                data = response.json().get(
                    "data",
                    []
                )

                if isinstance(
                    data,
                    list
                ):

                    return data

                print(
                    "⚠️ MT5API position state UNKNOWN: "
                    "invalid positions response."
                )

                return None

            print(
                "❌ Position retrieval failed: "
                f"HTTP {response.status_code}"
            )

            print(
                response.text[:1000]
            )

            print(
                "⚠️ MT5API position state UNKNOWN. "
                "Trading must remain locked."
            )

            return None

        except requests.RequestException as e:

            print(
                "❌ MT5API position "
                f"network error: {e}"
            )

            print(
                "⚠️ MT5API position state UNKNOWN. "
                "Trading must remain locked."
            )

            return None

    # ========================================
    # QUOTES
    # ========================================

    def get_quotes(
        self,
        symbols=None
    ):

        if (
            not self.connected
            or not self.account
        ):

            return []

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            return []

        if symbols is None:

            symbols = [
                "BTCUSDm"
            ]

        if isinstance(
            symbols,
            str
        ):

            symbols = [
                symbols
            ]

        symbol_string = ",".join(
            symbols
        )

        try:

            url = (
                f"{self.BASE_URL}/accounts/"
                f"{account_id}/quotes"
            )

            response = requests.get(

                url,

                headers=self._headers(),

                params={
                    "symbols":
                        symbol_string
                },

                timeout=15
            )

            if response.status_code == 200:

                quotes = response.json().get(
                    "data",
                    []
                )

                print(
                    f"✅ Quotes retrieved: "
                    f"{len(quotes)}"
                )

                return quotes

            print(
                "❌ Quote retrieval failed: "
                f"HTTP {response.status_code}"
            )

            print(
                response.text[:1000]
            )

            return []

        except requests.RequestException as e:

            print(
                "❌ MT5API quote "
                f"network error: {e}"
            )

            return []

    # ========================================
    # PRICE
    # ========================================

    def get_price(
        self,
        symbol
    ):

        quotes = self.get_quotes(
            [symbol]
        )

        if not quotes:

            return None

        quote = quotes[0]

        for field in (

            "price",
            "current_price",
            "bid",
            "ask",
            "last"

        ):

            if quote.get(field) is not None:

                return quote[field]

        return None

    # ========================================
    # GET ORDER / POSITION-BASED VERIFICATION
    # ========================================

    def get_order(
        self,
        order_id,
        submitted_order=None
    ):

        if (
            not self.connected
            or not self.account
        ):

            return None

        if not submitted_order:

            print(
                "⚠️ Position verification requires "
                "the submitted order response."
            )

            return None

        account_id = self.account.get("id")

        if not account_id:

            return None

        expected_ticket = submitted_order.get(
            "ticket"
        )

        expected_symbol = submitted_order.get(
            "symbol"
        )

        expected_side = str(
            submitted_order.get(
                "side",
                ""
            )
        ).lower()

        expected_volume = float(
            submitted_order.get(
                "volume",
                0
            ) or 0
        )

        expected_client_tag = submitted_order.get(
            "client_tag"
        )

        try:

            response = requests.get(

                f"{self.BASE_URL}/accounts/"
                f"{account_id}/positions",

                headers=self._headers(),

                timeout=15
            )

            print(
                "📡 MT5API position verification HTTP: "
                f"{response.status_code}"
            )

            if response.status_code != 200:

                print(
                    "⚠️ Position verification failed."
                )

                print(
                    response.text[:1000]
                )

                return None

            data = response.json().get(
                "data",
                []
            )

            if not isinstance(
                data,
                list
            ):

                print(
                    "⚠️ Position verification returned "
                    "invalid data."
                )

                return None

            for position in data:

                position_ticket = position.get(
                    "ticket"
                )

                # Strongest match: broker position ticket
                if (
                    expected_ticket is not None
                    and position_ticket == expected_ticket
                ):

                    print(
                        "🟢 MATCHED POSITION BY TICKET"
                    )

                    return {
                        **submitted_order,
                        "status": "filled",
                        "filled_volume": position.get(
                            "volume",
                            expected_volume
                        ),
                        "position": position
                    }

                position_symbol = position.get(
                    "symbol"
                )

                position_side = str(
                    position.get(
                        "side",
                        ""
                    )
                ).lower()

                position_volume = float(
                    position.get(
                        "volume",
                        0
                    ) or 0
                )

                position_client_tag = position.get(
                    "client_tag"
                )

                same_symbol = (
                    position_symbol == expected_symbol
                )

                same_side = (
                    position_side == expected_side
                )

                same_volume = (
                    abs(
                        position_volume
                        - expected_volume
                    ) < 0.0000001
                )

                same_tag = (
                    expected_client_tag is None
                    or position_client_tag
                    == expected_client_tag
                )

                if (
                    same_symbol
                    and same_side
                    and same_volume
                    and same_tag
                ):

                    print(
                        "🟢 MATCHED POSITION BY "
                        "SYMBOL/SIDE/VOLUME/TAG"
                    )

                    return {
                        **submitted_order,
                        "status": "filled",
                        "filled_volume": position_volume,
                        "position": position
                    }

            print(
                "🟡 No matching open position found."
            )

            return None

        except requests.RequestException as e:

            print(
                "❌ MT5API position verification "
                f"network error: {e}"
            )

            return None

    # ========================================
    # VERIFY ORDER
    # ========================================

    def verify_order(
        self,
        order_id,
        submitted_order=None,
        attempts=3,
        delay=2
    ):

        if not order_id:

            print(
                "⚠️ Cannot verify order: "
                "missing order ID."
            )

            return None

        print(
            "\n🔎 VERIFYING MT5API ORDER "
            "THROUGH POSITIONS"
        )

        for attempt in range(
            1,
            attempts + 1
        ):

            print(
                f"🔄 Verification "
                f"{attempt}/{attempts}"
            )

            order = self.get_order(
                order_id,
                submitted_order
            )

            if order:

                status = str(
                    order.get(
                        "status",
                        "unknown"
                    )
                ).lower()

                filled_volume = float(
                    order.get(
                        "filled_volume",
                        0
                    ) or 0
                )

                print(
                    f"Order status    : "
                    f"{status.upper()}"
                )

                print(
                    f"Filled volume   : "
                    f"{filled_volume}"
                )

                if (
                    status == "filled"
                    and filled_volume > 0
                ):

                    print(
                        "🟢 ORDER FILL CONFIRMED"
                    )

                    return order

            if attempt < attempts:

                print(
                    "🟡 Position not visible yet; "
                    "waiting before retry."
                )

                time.sleep(
                    delay
                )

        print(
            "⚠️ ORDER FILL NOT CONFIRMED."
        )

        return None

    # ========================================
    # MODIFY POSITION
    # ========================================

    def modify_position(
        self,
        ticket,
        stop_loss=None,
        take_profit=None,
        price=None
    ):

        if (
            not self.connected
            or not self.account
        ):

            print(
                "⚠️ Cannot modify position: "
                "MT5API is not connected."
            )

            return None

        if not ticket:

            print(
                "⚠️ Cannot modify position: "
                "missing ticket."
            )

            return None

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            print(
                "⚠️ Cannot modify position: "
                "missing account ID."
            )

            return None

        payload = {}

        if stop_loss is not None:

            payload[
                "stop_loss"
            ] = float(
                stop_loss
            )

        if take_profit is not None:

            payload[
                "take_profit"
            ] = float(
                take_profit
            )

        if price is not None:

            payload[
                "price"
            ] = float(
                price
            )

        if not payload:

            print(
                "⚠️ No modification values supplied."
            )

            return None

        url = (
            f"{self.BASE_URL}/accounts/"
            f"{account_id}/orders/{ticket}"
        )

        try:

            print(
                "📡 MT5API MODIFY PATCH:",
                url
            )

            response = requests.patch(

                url,

                headers=self._headers(),

                json=payload,

                timeout=20
            )

            print(
                "MT5API modify HTTP:",
                response.status_code
            )

            if response.status_code != 200:

                print(
                    "❌ Position modification failed."
                )

                print(
                    response.text[:3000]
                )

                return None

            return response.json()

        except requests.RequestException as e:

            print(
                "❌ MT5API modify error:",
                e
            )

            return None

        except ValueError:

            print(
                "❌ MT5API modify returned "
                "invalid JSON."
            )

            return None

    # ========================================
    # CLOSE POSITION
    # ========================================

    def close_position(
        self,
        ticket,
        volume=None
    ):

        if (
            not self.connected
            or not self.account
        ):

            print(
                "⚠️ Cannot close position: "
                "MT5API is not connected."
            )

            return None

        if not ticket:

            print(
                "⚠️ Cannot close position: "
                "missing ticket."
            )

            return None

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            print(
                "⚠️ Cannot close position: "
                "missing account ID."
            )

            return None

        payload = {}

        if volume is not None:

            payload[
                "volume"
            ] = float(
                volume
            )

        url = (
            f"{self.BASE_URL}/accounts/"
            f"{account_id}/positions/"
            f"{ticket}/close"
        )

        try:

            print(
                "📡 MT5API CLOSE POST:",
                url
            )

            response = requests.post(

                url,

                headers=self._headers(),

                json=payload,

                timeout=20
            )

            print(
                "MT5API close HTTP:",
                response.status_code
            )

            if response.status_code != 200:

                print(
                    "❌ Position close failed."
                )

                print(
                    response.text[:3000]
                )

                return None

            return response.json()

        except requests.RequestException as e:

            print(
                "❌ MT5API close error:",
                e
            )

            return None

        except ValueError:

            print(
                "❌ MT5API close returned "
                "invalid JSON."
            )

            return None

    # ========================================
    # CLOSE ALL
    # ========================================

    def close_all(self):

        if (
            not self.connected
            or not self.account
        ):

            print(
                "⚠️ Cannot close all: "
                "MT5API is not connected."
            )

            return None

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            print(
                "⚠️ Cannot close all: "
                "missing account ID."
            )

            return None

        url = (
            f"{self.BASE_URL}/accounts/"
            f"{account_id}/positions/close-all"
        )

        try:

            print(
                "📡 MT5API CLOSE-ALL POST:",
                url
            )

            response = requests.post(

                url,

                headers=self._headers(),

                json={},

                timeout=20
            )

            print(
                "MT5API close-all HTTP:",
                response.status_code
            )

            if response.status_code != 200:

                print(
                    "❌ Close-all failed."
                )

                print(
                    response.text[:3000]
                )

                return None

            return response.json()

        except requests.RequestException as e:

            print(
                "❌ MT5API close-all error:",
                e
            )

            return None

        except ValueError:

            print(
                "❌ MT5API close-all returned "
                "invalid JSON."
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

        if not self.connected:

            print(
                "❌ MT5API is not connected."
            )

            return None

        if not self.account:

            print(
                "❌ No MT5API account selected."
            )

            return None

        if signal not in (
            "BUY",
            "SELL"
        ):

            print(
                f"❌ Invalid trade signal: "
                f"{signal}"
            )

            return None

        if not symbol:

            print(
                "❌ Trading symbol is missing."
            )

            return None

        if (
            volume is None
            or volume <= 0
        ):

            print(
                f"❌ Invalid trade volume: "
                f"{volume}"
            )

            return None

        if stop_loss is None:

            print(
                "❌ Stop loss is required."
            )

            return None

        if take_profit is None:

            print(
                "❌ Take profit is required."
            )

            return None

        if stop_loss <= 0:

            print(
                f"❌ Invalid stop loss: "
                f"{stop_loss}"
            )

            return None

        if take_profit <= 0:

            print(
                f"❌ Invalid take profit: "
                f"{take_profit}"
            )

            return None

        account_id = self.account.get(
            "id"
        )

        if not account_id:

            print(
                "❌ Account ID is missing."
            )

            return None

        # ====================================
        # PLACE ORDER
        # ====================================

        payload = {

            "symbol":
                symbol,

            "side":
                signal.lower(),

            "type":
                "market",

            "volume":
                float(volume),

            "stop_loss":
                float(stop_loss),

            "take_profit":
                float(take_profit),

            "client_tag":
                "surge-sniper",

            "comment":
                "Surge-Sniper automated trade"
        }

        print(
            "\n📦 MT5API ORDER PAYLOAD"
        )

        print(
            f"Symbol      : "
            f"{payload['symbol']}"
        )

        print(
            f"Side        : "
            f"{payload['side']}"
        )

        print(
            f"Type        : "
            f"{payload['type']}"
        )

        print(
            f"Volume      : "
            f"{payload['volume']}"
        )

        print(
            f"Stop Loss   : "
            f"{payload['stop_loss']}"
        )

        print(
            f"Take Profit : "
            f"{payload['take_profit']}"
        )

        try:

            response = requests.post(

                f"{self.BASE_URL}/accounts/"
                f"{account_id}/orders",

                headers=self._headers(
                    str(uuid.uuid4())
                ),

                json=payload,

                timeout=15
            )

            print(
                "📡 MT5API order HTTP: "
                f"{response.status_code}"
            )

            print(
                response.text[:2000]
            )

            if response.status_code not in (
                200,
                201
            ):

                print(
                    "❌ MT5API order rejected."
                )

                return None

            data = response.json()

            order = data.get(
                "data"
            )

            if not order:

                print(
                    "❌ MT5API returned no "
                    "order object."
                )

                return None

            order_id = order.get(
                "id"
            )

            initial_status = str(
                order.get(
                    "status",
                    "unknown"
                )
            ).lower()

            initial_filled = float(
                order.get(
                    "filled_volume",
                    0
                ) or 0
            )

            print(
                "\n📋 MT5API ORDER STATE"
            )

            print(
                f"Order ID      : "
                f"{order_id}"
            )

            print(
                f"Initial status: "
                f"{initial_status.upper()}"
            )

            print(
                f"Filled volume : "
                f"{initial_filled}"
            )

            # =================================
            # ALREADY FILLED
            # =================================

            if (
                initial_status in (
                    "filled",
                    "open"
                )
                and
                initial_filled > 0
            ):

                print(
                    "🟢 MT5API ORDER "
                    "ALREADY FILLED"
                )

                return order

            # =================================
            # VERIFY ASYNC ORDER
            # =================================

            if order_id:

                verified = self.verify_order(
                    order_id,
                    order
                )

                if verified:

                    verified_status = str(
                        verified.get(
                            "status",
                            "unknown"
                        )
                    ).lower()

                    verified_filled = float(
                        verified.get(
                            "filled_volume",
                            0
                        ) or 0
                    )

                    if (
                        verified_status in (
                            "filled",
                            "open"
                        )
                        and
                        verified_filled > 0
                    ):

                        return verified

                    # Return the verified state
                    # so main.py can distinguish
                    # PENDING from FILLED.

                    return verified

            # =================================
            # UNVERIFIED
            # =================================

            print(
                "⚠️ MT5API order accepted "
                "but fill is unconfirmed."
            )

            return order

        except requests.RequestException as e:

            print(
                "❌ MT5API order "
                f"network error: {e}"
            )

            return None
