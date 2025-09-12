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
        # Get user EXP
        user = self.client.db.get_user_by_number(getattr(M.sender, "number", ""))
        exp = getattr(user, "exp", 0)

        # Determine JID for proper tagging
        sender_jid = getattr(M.sender, "jid", "")

        # If message is in a group, get the exact participant JID
        if getattr(M, "is_group", False):
            try:
                group_participants = self.client.get_group_members(M.chat)
                for p in group_participants:
                    if getattr(p, "number", "") == getattr(M.sender, "number", ""):
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass  # fallback to original sender_jid

        # Set mentioned_jid so WhatsApp tags properly
        M.mentioned_jid = [sender_jid]

        # **Use placeholder @0 to tag the first JID in mentioned_jid**
        text = f"🎯 Hey @0! Your current EXP is: *{exp}*."

        # Reply message
        self.client.reply_message(text, M)
