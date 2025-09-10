from libs import BaseCommand, MessageClass
import requests

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "gemini",
                "aliases": ["gem"],
                "category": "ai",
                "description": {"content": "Ask Gemini AI a question"},
                "exp": 1,
            },
        )

        # Free Gemini APIs to try
        self.apis = [
            "https://vapis.my.id/api/gemini?q={}",
            "https://api.siputzx.my.id/api/ai/gemini-pro?content={}",
            "https://api.ryzendesu.vip/api/ai/gemini?text={}",
            "https://api.dreaded.site/api/gemini2?text={}",
            "https://api.giftedtech.my.id/api/ai/geminiai?apikey=gifted&q={}",
            "https://api.giftedtech.my.id/api/ai/geminiaipro?apikey=gifted&q={}"
        ]

    def exec(self, M: MessageClass, _):
        query = M.content.replace(f"{self.client.config.prefix}gemini", "").replace(f"{self.client.config.prefix}gem", "").strip()

        if not query:
            return self.client.reply_message(
                f"⚠️ Please provide a question.\nExample: `{self.client.config.prefix}gem How do airplanes fly?`",
                M,
            )

        self.client.reply_message("🤖 Asking Gemini AI...", M)

        answer = None
        for api in self.apis:
            try:
                url = api.format(requests.utils.quote(query))
                resp = requests.get(url, timeout=30)
                if resp.status_code != 200:
                    continue

                data = resp.json()
                # Check multiple possible keys in response
                answer = data.get("message") or data.get("data") or data.get("answer") or data.get("result")
                if answer:
                    break
            except Exception:
                continue

        if not answer:
            self.client.reply_message("❌ Gemini AI failed to respond. Try again later.", M)
        else:
            self.client.reply_message(answer, M)
