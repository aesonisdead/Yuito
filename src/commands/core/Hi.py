from libs import BaseCommand, MessageClass
import re


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

        # raw values
        raw_sender_number = str(getattr(M.sender, "number", ""))
        # digits-only candidate
        digits_candidate = re.sub(r"\D+", "", raw_sender_number)

        # try to get alternate source from the raw message Info if available
        alt_candidate = None
        try:
            alt_candidate = str(M.Info.MessageSource.Sender.User)
        except Exception:
            alt_candidate = None

        # build list of candidates (prefer digits_candidate then alt)
        candidates = []
        if digits_candidate:
            candidates.append(digits_candidate)
        if alt_candidate and alt_candidate not in candidates:
            candidates.append(alt_candidate)

        # choose a candidate: prefer one that starts with 212 (Morocco) if present
        chosen_number = None
        for c in candidates:
            if c.startswith("212"):
                chosen_number = c
                break
        if not chosen_number:
            chosen_number = candidates[0] if candidates else raw_sender_number

        # build the JID from the chosen number
        try:
            sender_jid = self.client.build_jid(chosen_number)
        except Exception:
            # fallback to building from raw sender number if build_jid fails
            sender_jid = self.client.build_jid(raw_sender_number)

        # pick a human-friendly display name: prefer username (set in MessageClass), else PushName, else number
        sender_display = getattr(M.sender, "username", None)
        if not sender_display:
            try:
                contact = self.client.contact.get_contact(sender_jid)
                sender_display = getattr(contact, "PushName", None)
            except Exception:
                sender_display = None
        if not sender_display:
            sender_display = chosen_number

        # sanitize/display cleanup
        sender_display = re.sub(r"[\u2066-\u2069\u200E\u200F]", "", str(sender_display)).strip()

        # reply text using the friendly display (WhatsApp will still render mention from mentionedJid)
        reply_text = f"🎯 Hey @{sender_display}! Your current EXP is: *{exp}*."

        # send with explicit mentionedJid built from our chosen_jid (use positional args as NewClient expects)
        try:
            if getattr(M, "chat", "dm") == "group":
                context_info = {"mentionedJid": [sender_jid]}
                chat_id = M.gcjid
                # send_message(chat_id, text, context_info)
                self.client.send_message(chat_id, reply_text, context_info)
            else:
                # DM
                dm_jid = sender_jid
                self.client.send_message(dm_jid, reply_text)
        except Exception as e:
            # fallback: try the helper (older behavior) and log the exception
            try:
                self.client.log.error("Direct send with mentionedJid failed: %s", e)
            except Exception:
                pass
            # fallback to the helper method (should still work)
            try:
                self.client.reply_message_tag(reply_text, M)
            except Exception:
                # last resort: plain reply without mention
                self.client.reply_message(reply_text, M)

        # debug log for verification (will appear in your bot logs)
        try:
            dbg = (
                f"DBG HiCmd: raw_sender_number={repr(raw_sender_number)} | "
                f"digits_candidate={digits_candidate} | "
                f"alt_candidate={repr(alt_candidate)} | "
                f"chosen_number={chosen_number} | sender_jid={sender_jid}"
            )
            self.client.log.info(dbg)
        except Exception:
            pass
