from threading import Thread
from libs import BaseCommand, MessageClass
import yt_dlp
import os

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "instagram",
                "category": "media",
                "aliases": ["ig", "reel"],
                "description": {
                    "content": "Download Instagram videos or reels. Usage: #instagram <url>"
                },
                "exp": 2,
            },
        )

    def download_video(self, link: str, M: MessageClass):
        try:
            self.client.reply_message(f"*🎬 ⏳ Downloading Instagram video...*\nPlease wait...", M)

            os.makedirs("downloads", exist_ok=True)
            random_filename = self.client.utils.random_alpha_string(10)
            output_path = os.path.join("downloads", f"{random_filename}.%(ext)s")

            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "quiet": True,
                "outtmpl": output_path,
                "noplaylist": True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
                title = info.get("title", "Unknown Title")
                ext = info.get("ext", "mp4")
                downloaded_file = os.path.join("downloads", f"{random_filename}.{ext}")

            if not os.path.exists(downloaded_file):
                self.client.reply_message(f"*❌ Failed to find downloaded video for* {title}", M)
                return

            size = os.path.getsize(downloaded_file)
            if size > 100 * 1024 * 1024:
                os.remove(downloaded_file)
                self.client.reply_message(
                    f"❌ File size exceeds 100MB for: *{title}* ({self.client.utils.format_filesize(size)})",
                    M,
                )
                return

            self.client.send_video(
                M.gcjid,
                file=downloaded_file,
                caption=(
                    f"🎬 *Title:* {title}\n"
                    f"📦 *Size:* {self.client.utils.format_filesize(size)}\n"
                    f"📍 *Link:* {link}\n"
                ),
                quoted=M,
            )
            os.remove(downloaded_file)

        except Exception as e:
            self.client.reply_message(f"❌ Error downloading video:\n{link}", M)
            self.client.log.error(f"[InstagramDownloadError] {e}")

    def exec(self, M: MessageClass, _):
        if not M.urls:
            return self.client.reply_message(
                "*⚠️ Please provide an Instagram video or reel link.*", M
            )

        for link in M.urls:
            # Start download in a separate thread
            Thread(target=self.download_video, args=(link, M)).start()
