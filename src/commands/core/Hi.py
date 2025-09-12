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
        # get user and exp
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # Prefer the already-provided username ( MessageClass sets this ),
        # otherwise try to fetch the contact PushName, fallback to number.
        sender_display = getattr(M.sender, "username", None)
        if not sender_display:
            try:
                contact = self.client.contact.get_contact(
                    self.client.build_jid(M.sender.number)
                )
                sender_display = getattr(contact, "PushName", None) or M.sender.number
            except Exception:
                sender_display = M.sender.number

        # sanitize some direction/control characters that sometimes break rendering
        import re

        sender_display = re.sub(r"[\u2066-\u2069\u200E\u200F]", "", sender_display).strip()

        # build reply using the human-friendly display name (WhatsApp will resolve the actual mention
        # because reply_message_tag adds mentionedJid)
        reply_text = f"🎯 Hey @{sender_display}! Your current EXP is: *{exp}*."

        # send using the Void helper that attaches mentionedJid correctly
        self.client.reply_message_tag(reply_text, M)
