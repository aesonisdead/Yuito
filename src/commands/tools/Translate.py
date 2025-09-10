from libs import BaseCommand, MessageClass
from deep_translator import GoogleTranslator

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "translate",
                "category": "tools",
                "aliases": ["tr"],
                "description": {
                    "content": "Translate text from one language to another.",
                    "usage": "<target_lang> <text>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                f"⚠️ Usage: {self.client.config.prefix}translate <target_lang> <text>", M
            )

        args = contex.text.strip().split(" ", 1)
        if len(args) < 2:
            return self.client.reply_message(
                "⚠️ Please provide target language and text to translate.", M
            )

        target_lang, text = args[0].lower(), args[1]

        try:
            translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
            reply = f"🌐 *Translation ({target_lang}):*\n{translated_text} "
            self.client.reply_message(reply, M)
        except Exception as e:
            self.client.reply_message(
                f"❌ Translation failed. Make sure the language code is correct.\nError: {e}", M
            )
          
