from libs import BaseCommand, MessageClass
import requests

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "chatgpt",
                "aliases": ["gpt"],
                "category": "ai",
                "description": {"content": "Ask ChatGPT a question"},
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, _):
        query = M.content.replace(f"{self.client.config.prefix}chatgpt", "").replace(f"{self.client.config.prefix}gpt", "").strip()

        if not query:
            return self.client.reply_message(
                f"⚠️ Please provide a question.\nExample: `{self.client.config.prefix}gpt write a basic html code`",
                M,
            )

        try:
            # Notify processing
            self.client.reply_message("🤖 *Thinking...*", M)

            url = f"https://api.dreaded.site/api/chatgpt?text={requests.utils.quote(query)}"
            response = requests.get(url, timeout=60)

            if response.status_code != 200:
                return self.client.reply_message("❌ GPT API returned an error.", M)

            data = response.json()
            answer = data.get("result", {}).get("prompt") if data.get("success") else None

            if not answer:
                return self.client.reply_message("⚠️ ChatGPT did not return a valid response.", M)

            self.client.reply_message(answer, M)

        except Exception as e:
            self.client.reply_message("❌ Failed to get a response from ChatGPT.", M)
            self.client.log.error(f"[ChatGPTError] {e}")
