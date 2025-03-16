from dataclasses import dataclass
from typing import List, TypedDict


@dataclass(init=True, eq=True, frozen=True)
class Song:
    title: str
    artists: str
    album: str
    cover: str
    link: str
    track_number: int

    # def __eq__(self, other):
    #     if not isinstance(other, Song):
    #         return False
    #     return self.title == other.title and self.artists == other.artists and self.album == other.album

    # def __hash__(self):
    #     print("Hello 2")
    #     return hash((self.title, self.artists, self.album))


class TrackMetadataResponse(TypedDict):
    id: str
    title: str
    artists: str
    cover: str
    album: str
    releaseDate: str


class PlaylistMetadataResponse(TypedDict):
    success: bool
    statusCode: int
    artists: str
    title: str
    cover: str


class PlaylistTracksResponse(TypedDict):
    success: bool
    trackList: List[TrackMetadataResponse]
    nextOffset: str | None
    statusCode: 200
