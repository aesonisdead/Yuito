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
                "exp": 1,
            },
        )

    async def exec(self, M: MessageClass, _):
        try:
            # Check if the message itself is a sticker or reply to a sticker
            sticker_msg = None
            if hasattr(M.Message, "stickerMessage"):
                sticker_msg = M.Message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                return await self.client.reply_message(
                    "⚠️ Please reply to a sticker to convert it.", M
                )

            # Extract sticker URL or DirectPath
            sticker_bytes = None
            if hasattr(sticker_msg, "URL") and sticker_msg.URL:
                sticker_bytes = await self.client.get_bytes_from_name_or_url(sticker_msg.URL)
            elif hasattr(sticker_msg, "DirectPath") and sticker_msg.DirectPath:
                sticker_bytes = await self.client.get_bytes_from_name_or_url(sticker_msg.DirectPath)

            if not sticker_bytes:
                return await self.client.reply_message(
                    "❌ Failed to fetch sticker data.", M
                )

            # Convert WEBP -> PNG
            image = Image.open(io.BytesIO(sticker_bytes)).convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Send the converted image back
            await self.client.send_image(M, buffer.read(), caption="✅ Sticker converted to image")

        except Exception as e:
            await self.client.reply_message(f"❌ ToImgError: {e}", M)
            self.client.log.error(f"[ToImgError] {e}")
