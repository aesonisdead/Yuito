from libs import BaseCommand, MessageClass
import time

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client, handler,
            {
                "command": "yuito",
                "category": "core",
                "description": {"content": "Check bot latency"},
                "exp": 1,
            }
        )

    def exec(self, M: MessageClass, _):
        start = time.time()
        # Send the latency message directly
        latency = round((time.time() - start) * 1000)
        self.client.reply_message(f"Yuito is alive! latency: {latency}ms 🟢", M)
      
