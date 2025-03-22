import logging
import os
import re
from typing import Dict, List

from link import Link
from models import Song
from spotify_client import SpotifyClient
from utils import get_id


class App:
    SPOTIFY_PATTERNS: Dict[str, re.Pattern[str]] = {
        "track": re.compile(r".*spotify\.com\/(?:intl-[a-zA-Z]{2}\/)?track\/"),
        "playlist": re.compile(r".*spotify\.com\/playlist\/"),
        "album": re.compile(r".*spotify\.com\/album\/"),
    }

    NAME_SANITIZE_REGEX = re.compile(r"[<>:\"\/\\|?*]")

    def __init__(self, outpath: str = os.path.join(os.getcwd(), "songs")):
        self.client = SpotifyClient(self)
        self.links: List[Link] = []
        self.outpath: str = outpath

    def set_links(self, links: List[str]) -> None:
        for link in links:
            if not any(
                pattern.match(link) for pattern in self.SPOTIFY_PATTERNS.values()
            ):
                logging.error(f"The given link is not a correct spotify link: {link}")
                continue
            id = get_id(link)

            # Returns the fisrt key that has a pattern that matches the link
            linkType = next(
                key
                for key, pattern in self.SPOTIFY_PATTERNS.items()
                if pattern.match(link)
            )
            self.links.append(Link(link=link, id=id, linkType=linkType))

        logging.debug(f"Set links: {[link.link for link in self.links]}")
