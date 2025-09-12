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

        # Get sender JID (needed for tagging)
        sender_jid = getattr(M.sender, "jid", "")

        # If message is in a group, fetch the exact group participant JID
        if getattr(M, "is_group", False):
            try:
                group_participants = self.client.get_group_members(M.chat)
                for p in group_participants:
                    if getattr(p, "number", "") == getattr(M.sender, "number", ""):
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass  # fallback to original sender_jid

        # Build context_info for proper WhatsApp tagging
        context_info = {"mentionedJid": [sender_jid]}

        # Compose the message
        text = f"🎯 Hey! Your current EXP is: *{exp}*."

        # Reply with context_info so the sender gets properly tagged
        self.client.reply_message(text, M, context_info=context_info)
