from libs import BaseCommand, MessageClass
import requests
from io import BytesIO

UNSPLASH_ACCESS_KEY = "H2SAvCtNoYn3WRBmLYtnQoyOPdL2oDj8owVJjy1FlUM"  # <-- Your access key

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client, handler,
            {
                "command": "image",
                "category": "media",
                "aliases": ["img", "pic"],
                "description": {"content": "Search image. Usage: #img <query>"},
                "exp": 1,
            }
        )

    def exec(self, M: MessageClass, contex):
        query = contex.text.strip() if contex.text else None
        if not query:
            return self.client.reply_message("⚠️ Usage: #img <query>", M)

        api_url = f"https://api.unsplash.com/photos/random?query={query}&client_id={UNSPLASH_ACCESS_KEY}&orientation=landscape"

        try:
            resp = requests.get(api_url, timeout=10)
            data = resp.json()

            image_url = data.get("urls", {}).get("regular")
            if not image_url:
                return self.client.reply_message(f"❌ No image found for '{query}'", M)

            image_resp = requests.get(image_url, timeout=10)
            image_bytes = BytesIO(image_resp.content).read()  # <-- FIXED HERE

            caption = f"🖼 Image result for '{query}'"
            self.client.send_image(M.gcjid, image_bytes, caption=caption)

        except Exception as e:
            self.client.reply_message(f"❌ Error fetching image: {e}", M)
          
