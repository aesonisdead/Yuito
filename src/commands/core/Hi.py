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
        # Get user from database
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # Build the reply text with @number for tagging
        reply_text = f"🎯 Hey @{M.sender.number}! Your current EXP is: *{exp}*."

        # Send the reply using reply_message_tag, which handles mentions
        self.client.reply_message_tag(reply_text, M)
