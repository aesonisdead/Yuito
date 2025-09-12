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
    GroupInfoEv,
    CallOfferEv,
    PairStatusEv,
    event,
)

sys.path.insert(0, os.getcwd())

log = logging.getLogger("Void")
log.setLevel(logging.INFO)

class Void(NewClient):
    def __init__(self, db_path, config, log):
        super().__init__(db_path)

        self.__msg_id = []

        # Register events
        self.event(MessageEv)(self.on_message)
        self.event(ConnectedEv)(self.on_connected)
        self.event(GroupInfoEv)(self.on_groupevent)
        self.event(JoinedGroupEv)(self.on_joined)
        self.event(CallOfferEv)(self.on_call)
        self.event(PairStatusEv)(self.on_pair_status)
        self.event.paircode(self.on_paircode)

        # Utils
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
        self.log.info(f"⚡ Connected to {self.config.name} | Prefix: {self.config.prefix}")

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

    def on_pair_status(self, _: NewClient, message: PairStatusEv):
        self.log.info(f"Logged in as {message.ID.User}")

    def filter_admin_users(self, participants):
        return [p.JID.User for p in participants if p.IsAdmin]

    # --- FIXED TAGGING METHOD ---
    def reply_message_tag(self, text: str, M):
    """
    Send a message tagging the sender properly in groups.
    """
    try:
        to_jid = M.gcjid if M.chat == "group" else M.sender.number + "@s.whatsapp.net"

        ghost_mentions = None
        if M.chat == "group":
            ghost_mentions = M.sender.number + "@s.whatsapp.net"

        self.send_message(
            to=self.build_jid(to_jid),
            message=text,
            ghost_mentions=ghost_mentions,
        )
    except Exception as e:
        self.log.error(f"SendMessage failed: {e}")
