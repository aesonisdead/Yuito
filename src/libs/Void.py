import logging
import os
import sys
from neonize import NewClient
from handlers import Database, Message, Event
from neonize.utils import *
from utils import Utils
from neonize.events import (
    ConnectedEv,
    MessageEv,
    JoinedGroupEv,
    CallOfferEv,
    GroupInfoEv,
    PairStatusEv,
    event,
)

sys.path.insert(0, os.getcwd())


def interrupted(*_):
    event.set()


log.setLevel(logging.INFO)


class Void(NewClient):
    def __init__(self, db_path, config, log):
        super().__init__(db_path)

        self.__msg_id = []

        # Register the methods as event handlers
        self.event(MessageEv)(self.on_message)
        self.event(ConnectedEv)(self.on_connected)
        self.event(GroupInfoEv)(self.on_groupevent)
        self.event(JoinedGroupEv)(self.on_joined)
        self.event(CallOfferEv)(self.on_call)
        self.event(PairStatusEv)(self.on_pair_status)
        self.event.paircode(self.on_paircode)

        # Register all the methods from client utils
        self.extract_text = extract_text
        self.FFmpeg = FFmpeg
        self.save_file_to_temp_directory = save_file_to_temp_directory
        self.get_bytes_from_name_or_url = get_bytes_from_name_or_url
        self.AspectRatioMethod = AspectRatioMethod
        self.build_jid = build_jid
        self.Jid2String = Jid2String
        self.JIDToNonAD = JIDToNonAD
        self.MediaType = MediaType
        self.MediaTypeToMMS = MediaTypeToMMS
        self.BlocklistAction = BlocklistAction
        self.ChatPresence = ChatPresence
        self.ChatPresenceMedia = ChatPresenceMedia
        self.ClientName = ClientName
        self.ClientType = ClientType
        self.ParticipantChange = ParticipantChange
        self.ParticipantRequestChange = ParticipantRequestChange
        self.PrivacySetting = PrivacySetting
        self.PrivacySettingType = PrivacySettingType
        self.ReceiptType = ReceiptType
        self.add_exif = add_exif
        self.validate_link = validate_link
        self.gen_vcard = gen_vcard

        self.config = config
        self.__event = Event(self)
        self.__message = Message(self)
        self.utils = Utils()
        self.db = Database(config.uri)
        self.log = log

    def on_message(self, _: NewClient, message: MessageEv):
        if message.Info.ID not in self.__msg_id:
            from libs import MessageClass

            self.__msg_id.append(message.Info.ID)
            self.__message.handler(MessageClass(self, message).build())

    def on_connected(self, _: NewClient, __: ConnectedEv):
        self.__message.load_commands("src/commands")
        self.log.info(
            f"⚡ Connected to {self.config.name} and prefix is {self.config.prefix}"
        )

    def on_paircode(self, _: NewClient, code: str, connected: bool = True):
        if connected:
            self.log.info("Pair code successfully processed: %s", code)
        else:
            self.log.info("Pair code: %s", code)

    def on_groupevent(self, _, event: GroupInfoEv):
        self.__event.on_groupevent(event)

    def on_joined(self, _, event: JoinedGroupEv):
        self.__event.on_joined(event)

    def on_call(self, _, event: CallOfferEv):
        self.__event.on_call(event)

    @staticmethod
    def detect_message_type(msg) -> str | None:
        message_types = {
            "imageMessage": "IMAGE",
            "audioMessage": "AUDIO",
            "videoMessage": "VIDEO",
            "documentMessage": "DOCUMENT",
            "stickerMessage": "STICKER",
        }
        for attr, desc in message_types.items():
            if msg.HasField(attr):
                return desc
        return None

    def filter_admin_users(self, participants):
        return [
            participant.JID.User
            for participant in participants
            if participant.IsAdmin
        ]

    def on_pair_status(self, _: NewClient, message: PairStatusEv):
        self.log.info(f"logged as {message.ID.User}")

    # --- FIXED reply_message_tag ---
    def reply_message_tag(self, text: str, M):
        """
        Reply to a message with proper tagging of the sender.
        Works in DMs and group chats.
        """
        try:
            # Extract raw number from sender_jid
            raw_number = getattr(M.sender_jid, "user", None) or getattr(M.sender, "number", None)
            if not raw_number:
                raw_number = M.sender.number  # fallback

            # Prepend + to make proper phone format
            proper_number = f"+{raw_number}"

            # Build final text
            final_text = text.replace(str(M.sender.number), proper_number)

            # Determine chat ID
            if getattr(M, "chat", "dm") == "group":
                chat_id = M.gcjid
                context_info = {"mentionedJid": [f"{raw_number}@s.whatsapp.net"]}
                self.send_message(chat_id, final_text, context_info)
            else:
                # DM
                chat_id = self.build_jid(raw_number)
                self.send_message(chat_id, final_text)

        except Exception as e:
            try:
                self.log.error("Error in reply_message_tag: %s", e)
                # fallback
                self.reply_message(text, M)
            except Exception:
                pass
