from libs import BaseCommand, MessageClass

# Import the mention utility
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
        user = self.client.db.get_user_by_number(M.sender.number)
        exp = getattr(user, "exp", 0)

        # Prepare proper mention using pushname if available
        display_name = M.sender.pushname or M.sender.number
        mention_data = format_mention(M.sender.jid, display_name)

        # Compose the message
        text = f"🎯 Hey {mention_data['text']}! Your current EXP is: *{exp}*."

        # Send message with correct context_info for tagging
        self.client.reply_message(
            text,
            M,
            context_info=mention_data["context_info"]
        )
