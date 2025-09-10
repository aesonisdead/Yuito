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
                "category": "tools",
                "description": {"content": "Convert a sticker to an image"},
                "exp": 1
            },
        )

    def exec(self, M: MessageClass, _):
        try:
            # Get the sticker message
            sticker_msg = None
            if hasattr(M.Message, "stickerMessage"):
                sticker_msg = M.Message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                self.client.reply_message("⚠️ Please reply to a sticker to convert it.", M)
                return

            # Use FileSha256 or Url if available
            file_ref = getattr(sticker_msg, "FileSha256", None) or getattr(sticker_msg, "url", None)
            if not file_ref:
                self.client.reply_message("❌ Sticker data missing.", M)
                return

            # Fetch sticker bytes
            sticker_bytes = self.client.get_bytes_from_name_or_url(file_ref)
            if not sticker_bytes:
                self.client.reply_message("❌ Failed to fetch sticker data.", M)
                return

            # Convert WEBP -> PNG
            image = Image.open(io.BytesIO(sticker_bytes)).convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Send the converted image
            self.client.send_image(M, buffer.read(), caption="✅ Sticker converted to image")

        except Exception as e:
            self.client.reply_message(f"❌ ToImgError: {e}", M)
            self.client.log.error(f"[ToImgError] {e}")
