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
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # Simple text; WhatsApp will highlight/tag correctly in groups
        reply_text = f"🎯 Hey! Your current EXP is: *{exp}*."

        # Send message with proper mention
        self.client.reply_message_tag(reply_text, M)
