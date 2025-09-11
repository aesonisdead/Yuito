import sys
import os
import time
from config import get_config
from libs import Void
from utils import Log
from neonize.events import Event

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

    # Auto-reconnect if connection lost
    @Event.on('connection_lost')
    def reconnect(client, *args):
        client.log.info("⚠️ Connection lost. Attempting to reconnect...")
        try:
            client.connect()
        except Exception as e:
            client.log.error(f"❌ Reconnect failed: {e}")

    client.PairPhone(phone=number, show_push_notification=True)


if __name__ == "__main__":
    while True:
        try:
            main()
            break
        except Exception as e:
            Log.critical(f"🚨 Unexpected error occurred: {e}")
            time.sleep(1)
            Log.info("🔄 Restarting script due to error...")
            os.execv(sys.executable, [sys.executable] + sys.argv)
