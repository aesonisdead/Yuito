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

        # Build the message text (display number)
        reply_text = f"🎯 Hey @{M.sender.number}! Your current EXP is: *{exp}*."

        # Use reply_message_tag and pass the actual JID for mentions
        self.client.reply_message_tag(
            text=reply_text,        # message content
            M=M,                    # the original message
            mentions=[M.sender.jid] # pass JID object here for tagging
        )
