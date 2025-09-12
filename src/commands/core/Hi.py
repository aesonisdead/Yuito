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
        # Get user from the database
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # Display sender number
        sender_number_for_display = M.sender.number

        # Create the reply text
        reply_text = f"🎯 Hey @{sender_number_for_display}! Your current EXP is: *{exp}*."

        # Send the message with proper group tagging
        self.client.reply_message_tag(reply_text, M)
