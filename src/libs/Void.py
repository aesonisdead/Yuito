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

log = logging.getLogger()
log.setLevel(logging.INFO)


class Void(NewClient):
    def __init__(self, db_path, config, log):
        super().__init__(db_path)

        self.__msg_id = []

        # Register event handlers
        self.event(MessageEv)(self.on_message)
        self.event(ConnectedEv)(self.on_connected)
        self.event(GroupInfoEv)(self.on_groupevent)
        self.event(JoinedGroupEv)(self.on_joined)
        self.event(CallOfferEv)(self.on_call)
        self.event(PairStatusEv)(self.on_pair_status)
        self.event.paircode(self.on_paircode)

        # Utils
        self.extract_text = extract_text
        self.build_jid = build_jid
        self.utils = Utils()
        self.db = Database(config.uri)
        self.log = log
        self.__message = Message(self)
        self.__event = Event(self)
        self.config = config

    # --- Event handlers ---
    def on_message(self, _: NewClient, message):
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

    def on_pair_status(self, _: NewClient, message):
        self.log.info(f"logged as {message.ID.User}")

    # --- Messaging utilities ---
    def reply_message_tag(self, text: str, M):
        """
        Reply to a message with proper tagging of the sender.
        Works in DMs and group chats.
        """
        try:
            sender_jid = M.sender.jid  # <-- use the JID stored in MessageClass
            mentions = [sender_jid]

            chat_id = M.gcjid if getattr(M, "chat", "dm") == "group" else sender_jid

            # Some libraries require "text=" param
            self.send_message(chat_id, text=text, mentions=mentions)

        except Exception as e:
            self.log.error(f"Error in reply_message_tag: {e}")
            # fallback
            self.reply_message(text, M)

    # --- Other utilities ---
    def filter_admin_users(self, participants):
        return [
            participant.JID.User
            for participant in participants
            if participant.IsAdmin
        ]
