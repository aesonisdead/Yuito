from threading import Thread
from queue import Queue
from libs import BaseCommand, MessageClass
import yt_dlp
import os

MAX_THREADS = 3  # Max videos downloading at the same time
COOKIES_FILE = "cookies.txt"  # Your Instagram cookies (optional)

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
        # Initialize download queue
        self.download_queue = Queue()
        for _ in range(MAX_THREADS):
            t = Thread(target=self.worker)
            t.daemon = True
            t.start()

    def worker(self):
        while True:
            link, M = self.download_queue.get()
            try:
                self.download_video(link, M)
            except Exception as e:
                self.client.reply_message(f"❌ Error downloading video:\n{link}", M)
                self.client.log.error(f"[InstagramDownloadError] {e}")
            self.download_queue.task_done()

    def download_video(self, link: str, M: MessageClass):
        self.client.reply_message(f"*🎬 ⏳ Downloading Instagram video...*\nPlease wait...", M)
        os.makedirs("downloads", exist_ok=True)

        random_filename = self.client.utils.random_alpha_string(10)
        output_path = os.path.join("downloads", f"{random_filename}.%(ext)s")

        # Base options
        ydl_opts = {
            "format": "best[height<=720]",
            "quiet": True,
            "outtmpl": output_path,
            "noplaylist": True,
            "concurrent_fragment_downloads": 4,
            "postprocessors_threads": 2,
        }

        # First try **without cookies** (public video)
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=True)
        except yt_dlp.utils.DownloadError as e:
            # Check if it’s restricted/private
            if "Restricted" in str(e) or "login_required" in str(e):
                if os.path.exists(COOKIES_FILE):
                    ydl_opts["cookiefile"] = COOKIES_FILE
                    try:
                        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(link, download=True)
                    except Exception as e2:
                        self.client.reply_message(f"❌ Cannot download restricted/private video:\n{link}", M)
                        self.client.log.error(f"[InstagramDownloadError] {e2}")
                        return
                else:
                    self.client.reply_message(
                        "❌ Video is restricted/private. Provide a valid cookies.txt file.", M
                    )
                    return
            else:
                self.client.reply_message(f"❌ Failed to download video:\n{link}", M)
                self.client.log.error(f"[InstagramDownloadError] {e}")
                return

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

    def exec(self, M: MessageClass, _):
        if not M.urls:
            return self.client.reply_message(
                "*⚠️ Please provide an Instagram video or reel link.*", M
            )

        for link in M.urls:
            self.download_queue.put((link, M))
