import sys
import os
import time
from config import get_config
from libs import Void
from utils import Log

def main():
    config = get_config()
    number = config.number or input("📱 Enter your phone number: ").strip()

    if not number:
        Log.error("❌ Phone number is required.")
        sys.exit(1)

    if not config.uri:
        Log.error("❌ Mongodb url is required.")
        sys.exit(1)

    client = Void(config.session, config, Log)

    # Keep trying to connect and stay alive
    while True:
        try:
            client.PairPhone(phone=number, show_push_notification=True)
            client.RunLoop()  # Keeps the client running
        except Exception as e:
            Log.critical(f"🚨 Connection error: {e}")
            time.sleep(3)  # wait a bit before retrying
            Log.info("🔄 Attempting to reconnect...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        Log.info("🛑 Bot stopped by user.")
    except Exception as e:
        Log.critical(f"🚨 Fatal error: {e}")
        time.sleep(3)
        os.execv(sys.executable, [sys.executable] + sys.argv)
