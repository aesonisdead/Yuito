from libs import BaseCommand, MessageClass
import requests


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "imagine",
                "aliases": ["gen"],
                "category": "ai",
                "description": {"content": "Generate an image from a prompt"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        prompt = M.content.replace(f"{self.client.config.prefix}imagine", "").replace(f"{self.client.config.prefix}gen", "").strip()

        if not prompt:
            return self.client.reply_message(
                f"⚠️ Please provide a prompt.\n\nExample: `{self.client.config.prefix}imagine a sunset over mountains`",
                M
            )

        try:
            self.client.reply_message("🎨 Generating image...", M)

            url = f"https://shizoapi.onrender.com/api/ai/imagine?apikey=shizo&query={requests.utils.quote(prompt)}"
            response = requests.get(url, timeout=30)

            if response.status_code != 200:
                return self.client.reply_message("❌ Image API returned an error.", M)

            # Original bot probably sent URL or bytes using the standard send method
            data = response.content
            self.client.send_message(M.gcjid, data)

        except Exception as e:
            self.client.log.error(f"[ImagineError] {e}")
            self.client.reply_message("❌ Failed to generate image.", M)
