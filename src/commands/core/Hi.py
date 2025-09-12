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

        # --- FIX ---
        # Get numeric strings for JIDs
        to_jid = M.gcjid if M.chat == "group" else M.sender.number
        sender_jid = M.sender.number

        # Send the message with proper ghost_mentions
        self.client.send_message(
            to=self.client.build_jid(to_jid),
            message=reply_text,
            ghost_mentions=[sender_jid]  # numeric string, NOT JID object
        )
