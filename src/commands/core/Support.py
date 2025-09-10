from libs import BaseCommand, MessageClass

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "support",
                "category": "core",
                "description": {"content": "Get the support group link."},
                "aliases": ["helpdesk", "group"],
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        # React to the command with 🎋
        try:
            self.client.react_to_message(M, "🎋")
        except Exception:
            pass

        # Send support message with watermark
        support_text = """━━━━━━━━━━━━━━━━
🎋 *SUPPORT GROUP :*
━━━━━━━━━━━━━━━━

✨ Join our community below:

🔗 👉 https://clik.now/NexusCommunity


"""
        self.client.reply_message(support_text, M)
      
