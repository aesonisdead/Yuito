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

        # --- FIX: extract string JID ---
        recipient_jid_str = M.gcjid if M.chat == "group" else M.sender.jid
        if hasattr(recipient_jid_str, "User"):
            recipient_jid_str = recipient_jid_str.User  # get raw string from JID object

        sender_jid_str = M.sender.jid
        if hasattr(sender_jid_str, "User"):
            sender_jid_str = sender_jid_str.User

        self.client.send_message(
            to=self.client.build_jid(recipient_jid_str),
            message=reply_text,
            ghost_mentions=[self.client.build_jid(sender_jid_str)]
        )
