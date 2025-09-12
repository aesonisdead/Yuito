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
        # Get user and EXP
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # Prepare reply text
        reply_text = f"🎯 Hey @{M.sender.number}! Your current EXP is: *{exp}*."

        # Send message with proper tagging
        self.client.reply_message_tag(reply_text, M)
