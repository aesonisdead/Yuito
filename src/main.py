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

    # Try to pair device
    try:
        client.PairPhone(phone=number, show_push_notification=True)
    except Exception as e:
        Log.error(f"❌ Failed to pair: {e}")
        sys.exit(1)

    # Keep bot running
    while True:
        try:
            client.loop()  # or your client main loop if it has one
        except Exception as e:
            Log.critical(f"🚨 Unexpected error: {e}")
            Log.info("🔄 Restarting bot after 3s...")
            time.sleep(3)
            os.execv(sys.executable, [sys.executable] + sys.argv)

if __name__ == "__main__":
    main()
