import regex as re
from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "emojimix",
                "category": "tools",
                "description": {
                    "content": "Will merged two given emojis as new sticker",
                    "usage": "<emoji> + <emoji>",
                },
                "aliases": ["emix"],
                "exp": 2,
            },
        )

    def is_emoji(self, s: str) -> bool:
        return bool(re.fullmatch(r"\p{Emoji}", s))

    def exec(self, M: MessageClass, contex):
        text = (contex.text or "").strip()
        if "+" not in text:
            return self.client.reply_message(
                f"❌ Please provide two emojis separated by *+* — Use {self.client.config.prefix}emojimix 😕+😢",
                M,
            )

        emoji1, emoji2 = map(str.strip, text.split("+", 1))

        if not (self.is_emoji(emoji1) and self.is_emoji(emoji2)):
            return self.client.reply_message(
                "😕 Please provide *valid emojis* only!", M
            )

        q = f"{emoji1}_{emoji2}"
        url = f"https://tenor.googleapis.com/v2/featured?key=AIzaSyAyimkuYQYF_FXVALexPuGQctUWRURdCYQ&contentfilter=high&media_filter=png_transparent&component=proactive&collection=emoji_kitchen_v5&q={q}"

        data = self.client.utils.fetch(url)
        if not data or not data.get("results"):
            return self.client.reply_message(
                "😢 No emoji mix found for this combination.", M
            )

        try:
            png_url = data["results"][0]["media_formats"]["png_transparent"][
                "url"
            ]
            buffer = self.client.utils.fetch_buffer(png_url)
            self.client.send_sticker(
                M.gcjid, buffer, quoted=M, name="Created by", packname="Yuito"
            )
        except Exception as e:
            self.client.reply_message(
                "⚠️ Failed to send sticker. Try again later.", M
            )
            self.client.log.error(f"[EmojiMix] Sticker send error: {e}")
