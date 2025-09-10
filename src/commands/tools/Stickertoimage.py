from libs import BaseCommand, MessageClass
from PIL import Image
import io

class Command(BaseCommand):

    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "toimg",
                "aliases": ["stickertoimage", "s2i"],
                "category": "tools",
                "description": {"content": "Convert a sticker to an image"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        # Check if the message is replying to a sticker
        if not M.quoted or not hasattr(M.quoted, "stickerMessage"):
            return self.client.reply_message(
                "⚠️ Please reply to a sticker to convert it.", M
            )

        try:
            # Get sticker bytes
            sticker_msg = M.quoted.stickerMessage
            sticker_bytes = self.client.get_bytes_from_name_or_url(sticker_msg.FileId)

            # Convert WEBP to PNG
            sticker_img = Image.open(io.BytesIO(sticker_bytes)).convert("RGBA")
            output_buffer = io.BytesIO()
            sticker_img.save(output_buffer, format="PNG")
            output_buffer.seek(0)

            # Send back as image
            self.client.send_image(M, output_buffer.read(), caption="✅ Here’s your sticker as an image!")

        except Exception as e:
            self.client.log.error(f"[ToImgError] {e}")
            self.client.reply_message("❌ Failed to convert sticker to image.", M)
