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
        number = getattr(M.sender, "number", "Unknown")
        pushname = getattr(M.sender, "pushname", "User")
        jid = getattr(M.sender, "jid", "")

        # Set internal mentions for Neonize
        M.mentioned_jid = [jid]

        # Compose message with number + pushname for readability
        text = f"🎯 Hey @{number} ({pushname})! Your current EXP is: *{exp}*."

        # Reply
        self.client.reply_message(text, M)
