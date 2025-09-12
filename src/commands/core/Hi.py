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

    async def exec(self, M: MessageClass, _):
        # Get user EXP from database
        user = self.client.db.get_user_by_number(getattr(M.sender, "number", ""))
        exp = getattr(user, "exp", 0)

        # Safe display name
        number = getattr(M.sender, "number", "Unknown")
        pushname = getattr(M.sender, "pushname", "User")

        # Determine JID for proper tagging
        sender_jid = getattr(M.sender, "jid", "")

        # If message is in a group, fetch actual group participant JID
        if getattr(M, "is_group", False):
            group_jids = [p.jid for p in await self.client.get_group_members(M.chat)]
            # Match the sender number to get the exact participant JID
            sender_jid = next((jid for jid in group_jids if number in jid), sender_jid)

        # Set mentioned_jid so WhatsApp tags properly
        M.mentioned_jid = [sender_jid]

        # Compose message
        text = f"🎯 Hey @{pushname}! Your current EXP is: *{exp}*."

        # Reply (Neonize handles the tagging internally)
        await self.client.reply_message(text, M)
