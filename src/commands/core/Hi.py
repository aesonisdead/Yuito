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
        # Get sender number
        number = getattr(M.sender, "number", "")
        if not number:
            number = "0000000000"  # fallback number

        # Build proper WhatsApp JID
        sender_jid = f"{number}@s.whatsapp.net"

        # Ensure correct group participant JID if in group
        if getattr(M, "is_group", False):
            try:
                participants = self.client.get_group_members(M.chat)
                for p in participants:
                    if getattr(p, "number", "") == number:
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass

        # Set mentioned_jid for Neonize
        M.mentioned_jid = [sender_jid]

        # Use proper <@JID> format
        text = f"🎯 Hey <@{sender_jid}>! Your current EXP is: *0*."

        # Send the message
        self.client.reply_message(text, M)
