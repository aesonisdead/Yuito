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
        # Get sender JID
        sender_jid = getattr(M.sender, "jid", "")

        # If message is in a group, make sure to get the exact group participant JID
        if getattr(M, "is_group", False):
            try:
                participants = self.client.get_group_members(M.chat)
                for p in participants:
                    if getattr(p, "number", "") == getattr(M.sender, "number", ""):
                        sender_jid = getattr(p, "jid", sender_jid)
                        break
            except Exception:
                pass

        # Create a text that contains the exact JID in brackets — Neonize interprets it for tagging
        text = f"🎯 Hey <@{sender_jid}>! Your current EXP is: *0*."

        # Set mentioned_jid for Neonize to process
        M.mentioned_jid = [sender_jid]

        # Send the message
        self.client.reply_message(text, M)
