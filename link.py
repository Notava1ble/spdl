from typing import List

from models import Song


class Link:
    def __init__(self, link, id, linkType):
        self.link = link
        self.id = id
        self.linkType = linkType
        self.songs: List[Song] = []
