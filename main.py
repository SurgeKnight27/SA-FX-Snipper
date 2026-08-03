import config


def startup():
    print("=" * 50)
    print(f"        {config.BOT_NAME} v{config.VERSION}")
    print("      AI TRADING COMMAND CENTER")
    print("=" * 50)

    print("\n🟢 System Status : ONLINE\n")

    print("🧠 AI Engine.................READY")
    print("📈 Market Hunter............READY")
    print("🛡️ Risk Commander..........READY")
    print("🌍 Broker Manager...........READY")
    print("🎨 3D Dashboard............READY")

    print("\n" + "=" * 50)

    print(f"MODE : {config.MODE}")
    print(f"BROKER : {config.BROKER}")
    print(f"RISK : {config.RISK_PERCENT}%")

    print("\nWELCOME, COMMANDER! 🫡")
    print("MISSION STATUS : ACTIVE")
    print("Initializing future systems...")
    print("=" * 50)


if __name__ == "__main__":
    startup()
