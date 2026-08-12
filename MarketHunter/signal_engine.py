# ============================================
# Surge-Sniper
# Signal Engine v2.0
# Multi-Factor BTCUSDm Decision Engine
# ============================================


class SignalEngine:

    def __init__(self):

        self.minimum_confidence = 70


    # ========================================
    # GENERATE SIGNAL
    # ========================================

    def generate(
        self,
        trend,
        confidence,
        rsi=None
    ):

        # ------------------------------------
        # SAFETY CHECK
        # ------------------------------------

        if trend not in [
            "BULLISH",
            "BEARISH",
            "SIDEWAYS"
        ]:

            return "HOLD"


        if confidence < self.minimum_confidence:

            return "HOLD"


        # ------------------------------------
        # BULLISH
        # ------------------------------------

        if trend == "BULLISH":

            # Avoid buying extreme overbought
            if rsi is not None and rsi >= 75:

                return "HOLD"

            return "BUY"


        # ------------------------------------
        # BEARISH
        # ------------------------------------

        if trend == "BEARISH":

            # Avoid selling extreme oversold
            if rsi is not None and rsi <= 25:

                return "HOLD"

            return "SELL"


        # ------------------------------------
        # SIDEWAYS
        # ------------------------------------

        return "HOLD"


    # ========================================
    # DECISION DETAILS
    # ========================================

    def decision(
        self,
        trend,
        confidence,
        rsi=None
    ):

        signal = self.generate(
            trend,
            confidence,
            rsi
        )


        reason = "No confirmed setup."


        if signal == "BUY":

            reason = (
                "Bullish trend with sufficient "
                "confidence."
            )


        elif signal == "SELL":

            reason = (
                "Bearish trend with sufficient "
                "confidence."
            )


        elif trend == "BULLISH" and rsi is not None:

            if rsi >= 75:

                reason = (
                    "Bullish trend but RSI is "
                    "extremely overbought."
                )


        elif trend == "BEARISH" and rsi is not None:

            if rsi <= 25:

                reason = (
                    "Bearish trend but RSI is "
                    "extremely oversold."
                )


        return {

            "signal": signal,
            "confidence": confidence,
            "trend": trend,
            "rsi": rsi,
            "reason": reason

        }


    # ========================================
    # STATUS
    # ========================================

    def status(self):

        return (
            "ONLINE | "
            f"Minimum Confidence: "
            f"{self.minimum_confidence}%"
        )
