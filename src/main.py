import sys
import os
import time
from config import get_config
from libs import Void
from utils import Log
import threading

def start_bot():
    config = get_config()

    number = config.number or input("📱 Enter your phone number: ").strip()
    if not number:
        Log.error("❌ Phone number is required.")
        sys.exit(1)

    if not config.uri:
        Log.error("❌ Mongodb url is required.")
        sys.exit(1)

    client = Void(config.session, config, Log)

    try:
        # Pair phone only if session not valid
        client.PairPhone(phone=number, show_push_notification=True)
    except Exception as e:
        Log.critical(f"🚨 Failed to pair phone: {e}")
        return None

    return client

def run_bot_loop():
    while True:
        client = None
        try:
            client = start_bot()
            if not client:
                Log.error("❌ Client failed to start. Retrying in 5s...")
                time.sleep(5)
                continue

            Log.info("✅ Bot is running...")

            # Keep main thread alive
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            Log.info("🛑 Stopping bot by user.")
            if client:
                client.disconnect()
            break

        except Exception as e:
            Log.critical(f"🚨 Unexpected error occurred: {e}")
            if client:
                try:
                    client.disconnect()
                except:
                    pass
            Log.info("🔄 Restarting bot due to error...")
            time.sleep(5)
            continue

if __name__ == "__main__":
    run_bot_loop()
