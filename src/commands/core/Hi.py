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

        # Build the sender's full JID dynamically (works with your MessageClass)
        sender_jid = self.client.build_jid(M.sender.number)
        sender_number_for_display = M.sender.number

        # Create the reply text
        reply_text = f"🎯 Hey @{sender_number_for_display}! Your current EXP is: *{exp}*."

        # Send the message and mention the user
        self.client.reply_message(
            reply_text,
            M,
            mentions=[sender_jid]
        )
