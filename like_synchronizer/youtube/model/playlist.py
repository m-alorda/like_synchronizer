import dataclasses

import dataclasses_json

from like_synchronizer.youtube.model.common import PageInfo


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PlaylistItemDetails(dataclasses_json.DataClassJsonMixin):
    videoId: str


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PlaylistItem(dataclasses_json.DataClassJsonMixin):
    contentDetails: PlaylistItemDetails


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PlaylistItems(dataclasses_json.DataClassJsonMixin):
    items: tuple[PlaylistItem, ...] = tuple()
    pageInfo: PageInfo = PageInfo(totalResults=0, resultsPerPage=0)
    nextPageToken: str | None = None
