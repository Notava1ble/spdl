import logging
import os
import re
from typing import Dict, List

from models import LinkType, Song
from utils import get_id


class App:
    SPOTIFY_PATTERNS: Dict[str, re.Pattern[str]] = {
        "track": re.compile(r".*spotify\.com\/(?:intl-[a-zA-Z]{2}\/)?track\/"),
        "playlist": re.compile(r".*spotify\.com\/playlist\/"),
        "album": re.compile(r".*spotify\.com\/album\/"),
    }

    NAME_SANITIZE_REGEX = re.compile(r"[<>:\"\/\\|?*]")

    def __init__(self):
        self.links: List[LinkType] = []
        self.songs: List[Song] = []
        self.outpath: str = os.path.join(os.getcwd(), "songs")

    def set_links(self, links: List[LinkType]) -> None:
        for link in links:
            if not any(
                pattern.match(link["link"])
                for pattern in self.SPOTIFY_PATTERNS.values()
            ):
                logging.error(
                    f"The given link is not a correct spotify link: {link['link']}"
                )
                continue
            id = get_id(link["link"])

            # Returns the fisrt key that has a pattern that matches the link
            type = next(
                key
                for key, pattern in self.SPOTIFY_PATTERNS.items()
                if pattern.match(link["link"])
            )
            self.links.append({"link": id, "type": type})

        logging.debug(f"Set links: {self.links}")
