# src/commands/core/Hi.py

from libs import BaseCommand

class HiCmd(BaseCommand):
    name = "hi"
    category = "Core"
    description = "Say hi and show EXP"

    def exec(self, M, contex):
        try:
            exp = contex.get_user_exp(M.sender.number)  # assuming you have a method to get user EXP
            reply_text = f"🎯 Hey! Your current EXP is: *{exp}*."

            # Send the reply using the proper tagging
            self.client.reply_message_tag(reply_text, M)

        except Exception as e:
            self.client.log.error(f"Hi command failed: {e}")
