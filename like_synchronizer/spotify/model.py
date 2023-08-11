import dataclasses

import dataclasses_json


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class ExternalUrls:
    spotify: str | None = None


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class Artist:
    name: str
    id: str
    external_urls: ExternalUrls


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class Track:
    name: str
    id: str
    artists: tuple[Artist, ...]
    duration_ms: int
    external_urls: ExternalUrls
    popularity: int | None = None
    preview_url: str | None = None

    @property
    def artists_names(self) -> tuple[str, ...]:
        return tuple(artist.name for artist in self.artists)


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class TracksResults(dataclasses_json.DataClassJsonMixin):
    items: tuple[Track, ...] = tuple()
    limit: int = 0
    total: int = 0


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class SearchResults(dataclasses_json.DataClassJsonMixin):
    tracks: TracksResults = TracksResults()
