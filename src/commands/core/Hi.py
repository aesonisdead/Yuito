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
        # Get sender EXP from DB
        user = self.client.db.get_user_by_number(getattr(M.sender, "number", ""))
        exp = getattr(user, "exp", 0)

        # Get sender JID
        sender_jid = getattr(M.sender, "jid", "")

        # If in a group, ensure we use the correct participant JID
        if getattr(M, "is_group", False):
            try:
                participants = self.client.get_group_members(M.chat)
                for p in participants:
                    if getattr(p, "number", "") == getattr(M.sender, "number", ""):
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass

        # Compose message
        text = f"🎯 Hey! Your current EXP is: *{exp}*."

        # Use Neonize's built-in method for tagging
        # This ensures WhatsApp highlights the sender properly
        self.client.tag(
            chat_id=M.chat,
            text=text,
            mentioned_jid=[sender_jid]
        )
