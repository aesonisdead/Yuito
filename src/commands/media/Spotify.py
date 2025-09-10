from libs import BaseCommand, MessageClass
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import requests
from io import BytesIO

# Replace these with your Spotify API credentials
SPOTIFY_CLIENT_ID = "5cefebb672fc4c3a8aa8018090b77ed1"
SPOTIFY_CLIENT_SECRET = "49d7ec0a73aa48288a2ffde993a545e9"

class Command(BaseCommand):
    def __init__(self, client, handler):
        super().__init__(
            client,
            handler,
            {
                "command": "spotify",
                "category": "media",
                "aliases": ["sp"],
                "description": {
                    "content": "Get Spotify track info and preview link.",
                    "usage": "<spotify_track_url>",
                },
                "exp": 2,
            },
        )
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=SPOTIFY_CLIENT_ID,
            client_secret=SPOTIFY_CLIENT_SECRET
        ))

    def exec(self, M: MessageClass, contex):
        if not contex.text:
            return self.client.reply_message(
                "⚠️ Please provide a Spotify track URL.", M
            )

        try:
            track = self.sp.track(contex.text.strip())
            name = track['name']
            artists = ", ".join([a['name'] for a in track['artists']])
            album = track['album']['name']
            preview_url = track.get('preview_url', "No preview available")
            image_url = track['album']['images'][0]['url']

            # Download album art
            resp = requests.get(image_url, timeout=10)
            image_bytes = BytesIO(resp.content).read() if resp.status_code == 200 else None

            caption = f"""🎵 *{name}*
👤 *Artists:* {artists}
💿 *Album:* {album}
🎧 *Preview:* {preview_url if preview_url else 'Not available'} """

            if image_bytes:
                self.client.send_image(M.gcjid, image_bytes, caption=caption)
            else:
                self.client.reply_message(caption, M)

        except Exception as e:
            self.client.reply_message(f"❌ Failed to fetch track info.\nError: {e}", M)
