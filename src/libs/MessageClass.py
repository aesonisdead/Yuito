from libs import Void
from utils import Utils

class MessageClass:
    def __init__(self, client: Void, message):
        self.client = client
        self.Info = message.Info
        self.raw_message = message
        self.chat_id = str(self.Info.Chat.JID.User) if hasattr(self.Info.Chat.JID, 'User') else str(self.Info.Chat.JID)
        self.is_group = getattr(self.Info.Chat, 'IsGroup', False)

        # Extract sender JID correctly
        try:
            self.sender_jid = str(self.Info.MessageSource.Sender.JID.User)
        except AttributeError:
            self.sender_jid = str(self.Info.MessageSource.Sender.JID)

        # Sender display name
        try:
            self.sender_name = client.contact.get_contact(self.sender_jid).PushName
        except Exception:
            self.sender_name = "User"

        # Message type
        self.msg_type = client.detect_message_type(self.Info.Message)

        # Message content
        self.text = getattr(self.Info.Message, 'conversation', None) or ""
        self.quoted_message = getattr(self.Info.Message, 'contextInfo', None)

    def build(self):
        # Build the dict/object to pass to command handlers
        return self
