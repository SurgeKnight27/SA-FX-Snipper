# ============================================
# Surge-Sniper
# Risk Commander v2.1
# Symbol-Aware Risk Engine
# MT5API / BTCUSDm
# ACCOUNT-SAFE VERSION
# ============================================


class RiskCommander:

    def __init__(self):

        self.risk_percent = 1.0
        self.max_risk = 2.0

        # ========================================
        # SYMBOL SETTINGS
        # ========================================

        self.symbol_settings = {

            "BTCUSDm": {
                "contract_size": 1.0,
                "max_lot": 1.0,
                "default_stop": 100.0,
                "risk_reward": 2.0
            },

            "XAUUSD": {
                "contract_size": 100.0,
                "max_lot": 5.0,
                "default_stop": 10.0,
                "risk_reward": 2.0
            }

        }


    # ========================================
    # STATUS
    # ========================================

    def status(self):

        return "ONLINE"


    # ========================================
    # RISK SETTINGS
    # ========================================

    def set_risk(self, risk):

        if risk <= 0:
            return False

        if risk <= self.max_risk:

            self.risk_percent = risk

            return True

        return False


    # ========================================
    # ACCOUNT VALIDATION
    # ========================================

    def valid_balance(self, balance):

        if balance is None:
            return False

        try:

            balance = float(balance)

        except (TypeError, ValueError):

            return False

        return balance > 0


    # ========================================
    # RISK AMOUNT
    # ========================================

    def calculate_risk_amount(self, balance):

        if not self.valid_balance(balance):

            return 0.0

        return round(
            float(balance) *
            (self.risk_percent / 100),
            2
        )


    # ========================================
    # POSITION SIZE
    # ========================================

    def calculate_position(
        self,
        balance,
        stop_loss_points,
        symbol="BTCUSDm"
    ):

        if not self.valid_balance(balance):

            print(
                "🚫 Risk calculation blocked: "
                "account balance unavailable."
            )

            return 0.0


        if stop_loss_points <= 0:

            return 0.0


        settings = self.symbol_settings.get(
            symbol
        )


        if settings is None:

            print(
                f"⚠️ No risk settings for {symbol}"
            )

            return 0.0


        risk_amount = self.calculate_risk_amount(
            balance
        )


        contract_size = settings[
            "contract_size"
        ]


        lot_size = (
            risk_amount /
            (
                stop_loss_points *
                contract_size
            )
        )


        lot_size = round(
            lot_size,
            2
        )


        max_lot = settings[
            "max_lot"
        ]


        if lot_size > max_lot:

            lot_size = max_lot


        return lot_size


    # ========================================
    # TARGET CALCULATION
    # ========================================

    def calculate_targets(
        self,
        entry,
        direction,
        symbol="BTCUSDm"
    ):

        settings = self.symbol_settings.get(
            symbol
        )


        if settings is None:

            print(
                f"⚠️ No target settings for {symbol}"
            )

            return {

                "entry": entry,
                "stop_loss": None,
                "take_profit": None,
                "risk_reward": None

            }


        stop_distance = settings[
            "default_stop"
        ]


        reward_distance = (
            stop_distance *
            settings["risk_reward"]
        )


        if direction == "BUY":

            stop_loss = (
                entry -
                stop_distance
            )

            take_profit = (
                entry +
                reward_distance
            )


        elif direction == "SELL":

            stop_loss = (
                entry +
                stop_distance
            )

            take_profit = (
                entry -
                reward_distance
            )


        else:

            stop_loss = None
            take_profit = None


        return {

            "entry": entry,
            "stop_loss": stop_loss,
            "take_profit": take_profit,
            "risk_reward": "1:2"

        }


    # ========================================
    # RISK REPORT
    # ========================================

    def risk_report(
        self,
        balance,
        stop_loss_points,
        symbol="BTCUSDm"
    ):

        if not self.valid_balance(balance):

            return {

                "symbol": symbol,
                "balance": None,
                "risk_percent": self.risk_percent,
                "risk_amount": 0.0,
                "stop_loss_points": stop_loss_points,
                "lot_size": 0.0,
                "status": "ACCOUNT_BALANCE_UNAVAILABLE"

            }


        risk_amount = (
            self.calculate_risk_amount(
                balance
            )
        )


        lot_size = self.calculate_position(
            balance,
            stop_loss_points,
            symbol
        )


        return {

            "symbol": symbol,
            "balance": float(balance),
            "risk_percent": self.risk_percent,
            "risk_amount": risk_amount,
            "stop_loss_points": stop_loss_points,
            "lot_size": lot_size,
            "status": "READY"

        }


    # ========================================
    # TRADE APPROVAL
    # ========================================

    def approve_trade(
        self,
        signal,
        confidence
    ):

        if signal not in ["BUY", "SELL"]:

            return False


        if confidence < 70:

            return False


        return True


    # ========================================
    # SYMBOL EXPOSURE LIMIT
    # ========================================

    def exposure_allowed(
        self,
        current_volume,
        new_volume,
        max_volume=0.50
    ):

        try:

            current_volume = float(
                current_volume
            )

            new_volume = float(
                new_volume
            )

        except (TypeError, ValueError):

            print(
                "🚫 Invalid exposure values."
            )

            return False


        projected_volume = (
            current_volume +
            new_volume
        )


        if projected_volume > max_volume:

            print(
                "🚫 Exposure limit exceeded."
            )

            print(
                f"Current volume : {current_volume}"
            )

            print(
                f"New volume     : {new_volume}"
            )

            print(
                f"Maximum volume : {max_volume}"
            )

            return False


        return True
