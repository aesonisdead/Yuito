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

    async def exec(self, M: MessageClass, _):
        try:
            # 1. Detect sticker from message or quoted
            sticker_msg = None
            if hasattr(M.message, "stickerMessage"):
                sticker_msg = M.message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                return await self.client.reply_message(
                    "⚠️ Please reply to a sticker to convert it.", M
                )

            # 2. Get sticker bytes using client's downloader
            sticker_bytes = await self.client.get_bytes_from_name_or_url(sticker_msg)
            if not sticker_bytes:
                return await self.client.reply_message(
                    "❌ Failed to fetch sticker data.", M
                )

            # 3. Convert from WEBP -> PNG
            image = Image.open(io.BytesIO(sticker_bytes)).convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # 4. Send the PNG back
            await self.client.send_image(
                M,
                buffer.read(),
                caption="✅ Sticker converted to image"
            )

        except Exception as e:
            await self.client.reply_message(f"❌ ToImgError: {e}", M)
            self.client.log.error(f"[ToImgError] {e}")
