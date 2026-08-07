import websocket
import json
import os
from dotenv import load_dotenv

load_dotenv()


class DerivBroker:
    def __init__(self):
        self.app_id = os.getenv("DERIV_APP_ID")
        self.token = os.getenv("DERIV_API_TOKEN")
        self.ws = None
        self.connected = False

    def connect(self):
        try:
            url = f"wss://ws.derivws.com/websockets/v3?app_id={self.app_id}"

            print("🎲 Connecting to Deriv...")
            print("Using App ID:", self.app_id)

            self.ws = websocket.create_connection(
                url,
                timeout=10
            )

            self.ws.send(json.dumps({
                "authorize": self.token
            }))

            response = json.loads(self.ws.recv())

            if "authorize" in response:
                self.connected = True
                print("✅ Connected to Deriv")
                return True

            if "error" in response:
                print("❌ Deriv API Error:", response["error"]["message"])
                return False

            print("❌ Authorization failed")
            print(response)
            return False

        except Exception as e:
            print("❌ Deriv connection failed:", e)
            return False

    def get_account(self):
        if not self.connected:
            return None

        self.ws.send(json.dumps({
            "balance": 1
        }))

        return json.loads(self.ws.recv())

    def get_price(self, symbol="R_100"):
        if not self.connected:
            return None

        self.ws.send(json.dumps({
            "ticks": symbol
        }))

        data = json.loads(self.ws.recv())

        if "tick" in data:
            return data["tick"]["quote"]

        return None

    def status(self):
        return "ONLINE" if self.connected else "OFFLINE"

    def disconnect(self):
        if self.ws:
            self.ws.close()

        self.connected = False
        print("🔌 Deriv disconnected")
