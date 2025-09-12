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

        # --- START OF FIX ---

        # 1. Get the sender's full JID. This is more reliable than .number in groups.
        sender_jid = M.sender.jid
        
        # 2. Get the number part of the JID to display in the text.
        #    This splits '212605186422@s.whatsapp.net' and takes the first part.
        sender_number_for_display = sender_jid.split('@')[0]
        
        # 3. Create the message text. We will mention the user by their number.
        reply_text = f"🎯 Hey @{sender_number_for_display}! Your current EXP is: *{exp}*."

        # 4. Call reply_message WITH the 'mentions' parameter.
        #    This is the crucial part that tells WhatsApp who to actually tag.
        #    The library expects a list of JIDs.
        self.client.reply_message(
            reply_text,
            M,
            mentions=[sender_jid]
        )

        # --- END OF FIX ---
