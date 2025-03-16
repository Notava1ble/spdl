import json
import logging
import requests

from config import CUSTOM_HEADER


class SpotifyClient:
    def __init__(self):
        self.base_url: str = "https://spotidownloader.com"
        self.CUSTOM_HEADER: object = {
            "Host": "api.spotidownloader.com",
            "Referer": f"{self.base}/",
            "Origin": {self.base},
        }

    def get(self, sub_url: str):
        try:
            response = requests.get(self.base_url + sub_url)
            if response.status_code == 404:
                return None
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return None

    def get_track_info(self, link: str, token: str):
        track_id: str = link.split("/")[-1].split("?")[0]
        response = self.get(
            sub_url=f"/download/{track_id}?token={token}",
            headers=CUSTOM_HEADER,
        )

        return response.json()
