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

    # Wrap pairing and start in try-except to prevent crashing
    try:
        client.PairPhone(phone=number, show_push_notification=True)
    except Exception as e:
        Log.critical(f"🚨 Failed to start WhatsApp client: {e}")
        time.sleep(2)
        return False  # signal main loop to restart
    return True


if __name__ == "__main__":
    while True:
        try:
            success = main()
            if success:
                break  # exit loop if client started successfully
            else:
                Log.info("🔄 Restarting due to failed startup...")
                time.sleep(1)
        except KeyboardInterrupt:
            Log.info("🛑 Exiting by user")
            sys.exit(0)
        except Exception as e:
            Log.critical(f"🚨 Unexpected error occurred: {e}")
            time.sleep(2)
            Log.info("🔄 Restarting script due to unexpected error...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
