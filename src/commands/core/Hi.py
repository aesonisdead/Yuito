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

        # CLEAN the number
        sender_number = str(M.sender.number).replace('User: ', '').replace('"', '').strip()

        # Compose message
        reply_text = f"🎯 Hey @{sender_number}! Your current EXP is: *{exp}*."

        # Determine target JID
        to_jid = M.gcjid if M.chat == "group" else sender_number
        to_jid = str(to_jid).replace('User: ', '').replace('"', '').strip()

        # Send message — don't put ghost_mentions as list if message contains @
        self.client.send_message(
            to=self.client.build_jid(to_jid),
            message=reply_text
        )
