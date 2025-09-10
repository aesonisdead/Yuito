from libs import BaseCommand, MessageClass


class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "github",
                "category": "search",
                "aliases": ["gh"],
                "description": {
                    "content": "Get GitHub profile info of a user.",
                    "usage": "<username>",
                },
                "exp": 1,
            },
        )

    def exec(self, M: MessageClass, contex):
        prefix = self.client.config.prefix
        if not contex.text:
            return self.client.reply_message(
                f"⚠️ Oops! You didn’t define a username — Use `{prefix}github <Username>` to look up users.",
                M,
            )

        username = contex.text.strip()
        url = f"https://api.github.com/users/{username}"

        try:
            data = self.client.utils.fetch(url)

            if not data or "message" in data and data["message"] == "Not Found":
                return self.client.reply_message(
                    "❌ GitHub *user* not found with that username.", M
                )

            name = data.get("name", "Not set")
            bio = data.get("bio", "No bio")
            public_repos = data.get("public_repos", 0)
            followers = data.get("followers", 0)
            following = data.get("following", 0)
            profile = data.get("html_url")
            location = data.get("location", "Unknown")
            company = data.get("company", "Not listed")
            image = self.client.utils.fetch_buffer(
                data.get(
                    "avatar_url",
                    "https://www.pngall.com/wp-content/uploads/5/Profile-PNG-File.png",
                )
            )

            message = f"""\
👤 *GitHub Profile:* [{username}]({profile})

👨‍💻 *Name:* {name}
🏢 *Company:* {company}
🌍 *Location:* {location}
📦 *Public Repos:* {public_repos}
👥 *Followers:* {followers}
👣 *Following:* {following}
📝 *Bio:* {bio}
"""
            self.client.send_image(M.gcjid, image, message, M)

        except Exception as e:
            self.client.reply_message(
                "⚠️ An error occurred while fetching GitHub info.", M
            )
            self.client.log.error(f"[GitHubError] {e}")
