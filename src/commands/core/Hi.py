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
        # Get sender EXP
        user = self.client.db.get_user_by_number(getattr(M.sender, "number", ""))
        exp = getattr(user, "exp", 0)

        # Get sender JID
        sender_jid = getattr(M.sender, "jid", "")
        if getattr(M, "is_group", False):
            try:
                participants = self.client.get_group_members(M.chat)
                for p in participants:
                    if getattr(p, "number", "") == getattr(M.sender, "number", ""):
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass

        # **Set the mentions argument correctly**
        text = f"🎯 Hey! Your current EXP is: *{exp}*."
        self.client.reply_message(
            text,
            M,
            mentions=[sender_jid]  # <-- this is the key
        )
