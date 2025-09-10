from libs import BaseCommand, MessageClass
import requests
from io import BytesIO

DEEPSEEK_API_KEY = "d4537624-f85e-45cd-a1d9-eb639eb1dbed"

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "remini",
                "aliases": ["rem"],
                "category": "ai",
                "description": {"content": "Enhance an image using AI"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        img_bytes = None

        # Check if user sent an image attachment
        if hasattr(M.Message, "imageMessage"):
            try:
                img_bytes = self.client.get_bytes_from_name_or_url(M.Message.imageMessage)
            except Exception as e:
                self.client.log.error(f"[ReminiAttachmentError] {e}")

        # Check URLs if no attachment
        if img_bytes is None and M.urls:
            try:
                img_bytes = requests.get(M.urls[0], timeout=30).content
            except Exception as e:
                self.client.log.error(f"[ReminiURLError] {e}")

        if img_bytes is None:
            return self.client.reply_message(
                f"❌ You must send an image or an image URL! Try: *{self.client.config.prefix}remini <image or URL>*",
                M,
            )

        try:
            self.client.reply_message("> *ENHANCING IMAGE... 🔥*", M)

            response = requests.post(
                "https://api.deepseek.ai/v1/image/face-enhance",
                headers={"Authorization": f"Bearer {DEEPSEEK_API_KEY}"},
                files={"image": BytesIO(img_bytes)},
                timeout=60
            )

            if not response or response.status_code != 200:
                return self.client.reply_message("⚠️ Failed to enhance image.", M)

            enhanced_image_bytes = BytesIO(response.content)
            self.client.send_image(M.chat, enhanced_image_bytes, caption="✨ *Remini Result*")

        except Exception as e:
            self.client.reply_message("⚠️ Failed to enhance image.", M)
            self.client.log.error(f"[ReminiError] {e}")
