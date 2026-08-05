# ============================================
# Surge-Sniper
# Trailing Stop Engine v1.0
# ============================================


class TrailingStop:

    def __init__(self, distance=5):

        self.distance = distance

    def update(self, position, current_price):

        if position is None:
            return

        if position["status"] != "OPEN":
            return

        if position["direction"] == "BUY":

            new_stop = current_price - self.distance

            if new_stop > position["stop_loss"]:

                old_stop = position["stop_loss"]

                position["stop_loss"] = round(new_stop, 2)

                print("\n==============================")
                print("📈 TRAILING STOP UPDATED")
                print("==============================")
                print(f"Old Stop : {old_stop}")
                print(f"New Stop : {position['stop_loss']}")

        else:

            new_stop = current_price + self.distance

            if new_stop < position["stop_loss"]:

                old_stop = position["stop_loss"]

                position["stop_loss"] = round(new_stop, 2)

                print("\n==============================")
                print("📈 TRAILING STOP UPDATED")
                print("==============================")
                print(f"Old Stop : {old_stop}")
                print(f"New Stop : {position['stop_loss']}")


if __name__ == "__main__":

    print("Trailing Stop Engine Ready.")
