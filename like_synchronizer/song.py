import dataclasses
import re
from typing import Iterable

import youtube_title_parse

_BLACKLISTED_WORDS = "|".join(
    (
        "download",
        "official",
        "oficial",
        "audio",
        "performance",
        "live",
        "versi.n",
        "clip",
    )
)
_BRACKETS_PATTERN = re.compile(
    f"(\\s+)?\\(.*({_BLACKLISTED_WORDS}).*\\)(\\s+)?", re.IGNORECASE
)
_VERTICAL_BAR_PATTERN = re.compile("(\\s+)?\\|(.*)?")
_WHITESPACE_PATTERN = re.compile("\\s+")


def _clean_str(value: str, patterns: Iterable[tuple[re.Pattern, str]]) -> str:
    result = value
    for pattern, replace_value in patterns:
        result = pattern.sub(replace_value, result)
    return result


def _clean_song_artist(artist: str) -> str:
    return _clean_str(
        artist,
        patterns=(
            (_BRACKETS_PATTERN, ""),
            (_WHITESPACE_PATTERN, " "),
        ),
    )


def _clean_song_title(title: str) -> str:
    return _clean_str(
        title,
        patterns=(
            (_BRACKETS_PATTERN, ""),
            (_VERTICAL_BAR_PATTERN, ""),
            (_WHITESPACE_PATTERN, " "),
        ),
    )


def _parse_artist_and_title(video_title: str) -> tuple[str | None, str | None]:
    parse_result = youtube_title_parse.get_artist_title(video_title)
    if parse_result is None:
        return None, None
    song_artist, song_title = parse_result
    return (
        _clean_song_artist(song_artist),
        _clean_song_title(song_title),
    )


@dataclasses.dataclass(frozen=True)
class Song:
    original_title: str
    artist: str | None = None
    title: str | None = None

    @classmethod
    def from_video_title(cls, video_title: str) -> "Song":
        song_artist, song_title = _parse_artist_and_title(video_title)
        return Song(original_title=video_title, artist=song_artist, title=song_title)


if __name__ == "__main__":
    print(Song.from_video_title("Coone - Sir Gaga (Official Video) (Free Download)"))
    print(
        Song.from_video_title(
            "Manian - Welcome To The Club (Da Mayh3m Hardstyle Remix) | HQ Lyric Videoclip"
        )
    )
