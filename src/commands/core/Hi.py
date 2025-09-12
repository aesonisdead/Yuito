from libs import BaseCommand, MessageClass
from libs.tag_utils import format_mention

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

        # Safe display name
        display_name = getattr(M.sender, "pushname", None) or getattr(M.sender, "number", "Unknown")
        mention_data = format_mention(getattr(M.sender, "jid", ""), display_name)

        # Compose message
        text = f"🎯 Hey {mention_data['text']}! Your current EXP is: *{exp}*."

        # Send message with proper tagging
        self.client.reply_message(
            text,
            M,
            context_info=mention_data["context_info"]
        )
