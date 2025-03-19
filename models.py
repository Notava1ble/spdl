from dataclasses import dataclass
from re import Pattern
from typing import AnyStr, List, TypedDict


@dataclass(init=True, eq=True, frozen=True)
class Song:
    id: str
    title: str
    artists: str
    album: str
    cover: str
    link: str
    track_number: int


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


class LinkType(TypedDict):
    link: str
    type: str
