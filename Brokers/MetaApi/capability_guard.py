# ============================================
# Surge-Sniper
# MT5API Capability Guard v2.0
# READ + VERIFIED EXECUTION DISCOVERY
# ============================================

import requests


class MT5APICapabilityGuard:
    """
    MT5API capability detector.

    READ operations are verified directly.

    WRITE operations are enabled only when the
    documented endpoint exists. Actual trading
    requests remain controlled by metaapi.py.
    """

    def __init__(self, broker):
        self.broker = broker

        self.capabilities = {
            "read": {
                "positions": "UNKNOWN",
                "quotes": "UNKNOWN",
                "account": "UNKNOWN",
            },
            "management": {
                "modify_sl_tp": "UNKNOWN",
                "close": "UNKNOWN",
                "close_all": "UNKNOWN",
            },
            "execution": {
                "place_order": "UNKNOWN",
            },
        }

        self.openapi_loaded = False
        self.openapi = None

    # ========================================
    # OPENAPI DISCOVERY
    # ========================================

    def load_openapi(self):
        try:
            response = requests.get(
                self.broker.BASE_URL.rstrip("/") + "/openapi.json",
                headers=self.broker._headers(),
                timeout=20,
            )

            if response.status_code != 200:
                print(
                    "❌ OpenAPI discovery failed: "
                    f"HTTP {response.status_code}"
                )
                return False

            self.openapi = response.json()
            self.openapi_loaded = True

            print("🟢 OpenAPI specification loaded.")
            return True

        except requests.RequestException as e:
            print(
                "❌ OpenAPI discovery network error: "
                f"{e}"
            )
            return False

        except ValueError as e:
            print(
                "❌ Invalid OpenAPI response: "
                f"{e}"
            )
            return False

    # ========================================
    # PATH CHECK
    # ========================================

    def has_endpoint(self, path, method):
        if not self.openapi_loaded:
            return False

        spec = self.openapi.get("paths", {}).get(path)

        if not spec:
            return False

        return method.lower() in spec

    # ========================================
    # SAFE READ CAPABILITY CHECK
    # ========================================

    def check_read_capabilities(self):
        account_ok = bool(
            self.broker.connected
            and self.broker.account
        )

        self.capabilities["read"]["account"] = (
            "SUPPORTED"
            if account_ok
            else "UNKNOWN"
        )

        if not account_ok:
            return

        try:
            positions = self.broker.get_positions()

            self.capabilities["read"]["positions"] = (
                "SUPPORTED"
                if positions is not None
                else "UNKNOWN"
            )

        except Exception:
            self.capabilities["read"]["positions"] = "UNKNOWN"

        try:
            quotes = self.broker.get_quotes(["BTCUSDm"])

            self.capabilities["read"]["quotes"] = (
                "SUPPORTED"
                if quotes
                else "UNKNOWN"
            )

        except Exception:
            self.capabilities["read"]["quotes"] = "UNKNOWN"

    # ========================================
    # MANAGEMENT CAPABILITY DISCOVERY
    # ========================================

    def check_management_capabilities(self):
        modify_path = (
            "/v1/accounts/{accountId}/orders/{ticket}"
        )

        close_path = (
            "/v1/accounts/{accountId}/positions/"
            "{ticket}/close"
        )

        close_all_path = (
            "/v1/accounts/{accountId}/positions/"
            "close-all"
        )

        modify_exists = self.has_endpoint(
            modify_path,
            "patch",
        )

        close_exists = self.has_endpoint(
            close_path,
            "post",
        )

        close_all_exists = self.has_endpoint(
            close_all_path,
            "post",
        )

        # IMPORTANT:
        #
        # We previously received HTTP 501
        # feature_unavailable for the modification
        # backend.
        #
        # Therefore modification remains blocked.

        if modify_exists:
            self.capabilities["management"]["modify_sl_tp"] = (
                "UNSUPPORTED"
            )

        if close_exists:
            self.capabilities["management"]["close"] = (
                "SUPPORTED"
            )

        if close_all_exists:
            self.capabilities["management"]["close_all"] = (
                "SUPPORTED"
            )

    # ========================================
    # EXECUTION CAPABILITY
    # ========================================

    def check_execution_capability(self):
        order_path = (
            "/v1/accounts/{accountId}/orders"
        )

        order_exists = self.has_endpoint(
            order_path,
            "post",
        )

        if order_exists:
            self.capabilities["execution"]["place_order"] = (
                "SUPPORTED"
            )

    # ========================================
    # FULL AUDIT
    # ========================================

    def audit(self):
        print("=" * 64)
        print("SURGE-SNIPER MT5API CAPABILITY GUARD")
        print("=" * 64)

        if not self.load_openapi():
            print()
            print("🔴 CAPABILITY AUDIT FAILED")
            return self.capabilities

        self.check_read_capabilities()
        self.check_management_capabilities()
        self.check_execution_capability()

        self.print_report()

        return self.capabilities

    # ========================================
    # REPORT
    # ========================================

    def print_report(self):
        print()
        print("=" * 64)
        print("READ")
        print("=" * 64)

        for name, status in self.capabilities["read"].items():
            print(
                f"{name:<15}: {status}"
            )

        print()
        print("=" * 64)
        print("MANAGEMENT")
        print("=" * 64)

        for name, status in self.capabilities["management"].items():
            print(
                f"{name:<15}: {status}"
            )

        print()
        print("=" * 64)
        print("EXECUTION")
        print("=" * 64)

        for name, status in self.capabilities["execution"].items():
            print(
                f"{name:<15}: {status}"
            )

        print()
        print("=" * 64)
        print("CAPABILITY AUDIT COMPLETE")
        print("=" * 64)
