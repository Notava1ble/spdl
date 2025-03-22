import json
import logging
from typing import List
import requests

from models import PlaylistMetadataResponse, PlaylistTracksResponse
from utils import get_id, make_unique_song_objects


class SpotifyClient:
    def __init__(self, app):
        self.app = app
        self.BASE_URL: str = "https://spotidownloader.com"
        self.CUSTOM_HEADER = {
            "Host": "api.spotidownloader.com",
            "Referer": f"{self.BASE_URL}/",
            "Origin": f"{self.BASE_URL}",  # Changed from set to string
        }

    def get(self, sub_url: str):
        try:
            response = requests.get(
                self.BASE_URL + sub_url,
                headers=self.CUSTOM_HEADER,
            )
            if response.status_code == 404:
                logging.error(f"Status code 404, for sub_url ({sub_url})")
                return None
            return json.loads(response.text)
        except requests.exceptions.RequestException as e:
            logging.error(f"Network error: {e}")
            return None

    def get_track_info(self, link: str, token: str):
        track_id: str = get_id(link=link)
        response = self.get(
            sub_url=f"/download/{track_id}?token={token}",
        )

        return response.json()

    def get_from_playlist(self, target: str, playlist_id: str, mode: str, offset=None):
        """Returns the targeted information("tracks" or "metadata") for a playlist/album

        :param target: What do you want to get from the playlist. Valid values: "tracks" or "metadata"
        :type target: str
        :param playlist_id: The playlist id
        :type playlist_id: str
        :param mode: "playlist" or "album"
        :type mode:
        TODO Finish the return type
        :return: The list
        :rtype: _type_
        """
        return self.get(
            sub_url=f"/{target}/{mode}/{playlist_id}{f"?offset={offset}" if offset else ""}"
        )

    def get_playlist_info(self, link: str, trackname_convention: int, mode):
        playlist_id = get_id(link=link)
        metadata: PlaylistMetadataResponse = self.get_from_playlist(
            target="metadata", playlist_id=playlist_id, mode=mode
        )
        playlist_name: str = metadata["title"]
        if metadata["success"]:
            logging.info("-" * 40)
            logging.info(f"Name: {playlist_name} by {metadata['artists']}")

        logging.info(f"Getting songs from {mode} (this might take a while ...)")
        track_list: List[PlaylistTracksResponse] = []
        tracks_data: PlaylistTracksResponse = self.get_from_playlist(
            target="tracks", playlist_id=playlist_id, mode=mode
        )
        track_list.extend(tracks_data["trackList"])
        next_offset = tracks_data["nextOffset"]
        while next_offset:
            tracks_data: PlaylistTracksResponse = self.get_from_playlist(
                target="tracks", playlist_id=playlist_id, mode=mode, offset=next_offset
            )
            track_list.extend(tracks_data["trackList"])
            next_offset = tracks_data["nextOffset"]

        song_list_dict = make_unique_song_objects(
            track_list, trackname_convention, playlist_name, mode
        )
        return song_list_dict, playlist_name, track_list
