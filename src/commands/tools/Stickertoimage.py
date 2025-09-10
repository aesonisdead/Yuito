from libs import BaseCommand, MessageClass
from PIL import Image
import io
import asyncio

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
        # Run async logic in the background so no 'await' is needed
        asyncio.create_task(self.run(M))

    async def run(self, M: MessageClass):
        try:
            # Check if the message is a sticker or is replying to a sticker
            sticker_msg = None
            if hasattr(M.Message, "stickerMessage"):
                sticker_msg = M.Message.stickerMessage
            elif M.quoted and hasattr(M.quoted, "stickerMessage"):
                sticker_msg = M.quoted.stickerMessage

            if not sticker_msg:
                await self.client.reply_message(
                    "⚠️ Please reply to a sticker to convert it.", M
                )
                return

            # Fetch sticker bytes
            sticker_bytes = await self.client.get_bytes_from_name_or_url(sticker_msg)
            if not sticker_bytes or not isinstance(sticker_bytes, (bytes, bytearray)):
                await self.client.reply_message(
                    "❌ Sticker data missing or invalid.", M
                )
                return

            # Convert WEBP -> PNG
            image = Image.open(io.BytesIO(sticker_bytes)).convert("RGBA")
            buffer = io.BytesIO()
            image.save(buffer, format="PNG")
            buffer.seek(0)

            # Send the converted image
            await self.client.send_image(M, buffer.read(), caption="✅ Sticker converted to image")

        except Exception as e:
            await self.client.reply_message(f"❌ ToImgError: {e}", M)
            self.client.log.error(f"[ToImgError] {e}")
