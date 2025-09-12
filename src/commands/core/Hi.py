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
        # Get user EXP from database
        user = self.client.db.get_user_by_number(getattr(M.sender, "number", ""))
        exp = getattr(user, "exp", 0)

        # Safe display name
        number = getattr(M.sender, "number", "Unknown")
        pushname = getattr(M.sender, "pushname", "User")
        sender_jid = getattr(M.sender, "jid", "")

        # If message is in a group, fetch participants synchronously
        if getattr(M, "is_group", False):
            try:
                group_participants = self.client.get_group_members(M.chat)  # synchronous call
                # Match the sender number to get exact participant JID
                for p in group_participants:
                    if number in getattr(p, "number", ""):
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass  # fallback to original sender_jid

        # Set mentioned_jid so WhatsApp tags properly
        M.mentioned_jid = [sender_jid]

        # Compose message
        text = f"🎯 Hey @{pushname}! Your current EXP is: *{exp}*."

        # Reply (synchronous)
        self.client.reply_message(text, M)
