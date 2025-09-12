from libs import BaseCommand, MessageClass

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "hi",
                "category": "core",
                "description": {"content": "Say hello to the bot"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        # Get user EXP
        user = self.client.db.get_user_by_number(getattr(M.sender, "number", ""))
        exp = getattr(user, "exp", 0)

        # Safe display name
        display_name = getattr(M.sender, "pushname", None) or getattr(M.sender, "number", "Unknown")
        jid = getattr(M.sender, "jid", "")

        # Set mentions for Neonize internally
        M.mentioned_jid = [jid]

        # Compose message
        text = f"🎯 Hey @{display_name}! Your current EXP is: *{exp}*."

        # Reply (no extra args)
        self.client.reply_message(text, M)
