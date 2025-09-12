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

        reply_text = f"🎯 Hey! Your current EXP is: *{exp}*."

        # --- CLEAN numeric strings ---
        to_jid = M.gcjid if M.chat == "group" else M.sender.number
        # Remove any extra text, spaces, or prefixes
        to_jid = str(to_jid).replace('User: ', '').replace('"', '').strip()
        sender_jid = str(M.sender.number).replace('User: ', '').replace('"', '').strip()

        # Send message
        self.client.send_message(
            to=self.client.build_jid(to_jid),
            message=reply_text,
            ghost_mentions=[sender_jid]
        )
