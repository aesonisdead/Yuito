from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "weather",
                "category": "search",
                "aliases": ["wthr"],
                "description": {
                    "content": "Get current weather of a city.",
                    "usage": "<city>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        prefix = self.client.config.prefix
        city = contex.text.strip() if contex.text else None

        if not city:
            return self.client.reply_message(
                f"⚠️ You didn’t specify a city — use `{prefix}weather casablanca`.",
                M,
            )

        API_KEY = "060a6bcfa19809c2cd4d97a212b19273"
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}&language=tr"

        try:
            res = self.client.utils.fetch(url)

            if res.get("cod") != 200:
                return self.client.reply_message(
                    f"🌍 City *{city.title()}* not found.", M
                )

            name = res["name"]
            country = res["sys"]["country"]
            weather = res["weather"][0]["description"].capitalize()
            temp = res["main"]["temp"]
            feels_like = res["main"]["feels_like"]
            humidity = res["main"]["humidity"]
            wind_speed = res["wind"]["speed"]

            reply = f"""🌤️ *Weather in {name}, {country}*

🌡️ *Temperature:* {temp}°C
🤗 *Feels like:* {feels_like}°C
💧 *Humidity:* {humidity}%
💨 *Wind Speed:* {wind_speed} m/s
🌥️ *Condition:* {weather}
"""
            self.client.reply_message(reply.strip(), M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ Could not retrieve weather info. Please try again later.", M
            )
            self.client.log.error(f"[WeatherError] {e}")
