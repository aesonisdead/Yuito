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

        # Register client utils
        self.extract_text = extract_text
        self.build_jid = build_jid
        self.utils = Utils()
        self.db = Database(config.uri)
        self.log = log
        self.__message = Message(self)
        self.__event = Event(self)
        self.config = config

    def on_message(self, _: NewClient, message):
        if message.Info.ID not in self.__msg_id:
            from libs import MessageClass
            self.__msg_id.append(message.Info.ID)
            self.__message.handler(MessageClass(self, message).build())

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
            self.reply_message(text, M)
