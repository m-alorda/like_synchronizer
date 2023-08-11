import dataclasses

import dataclasses_json

from like_synchronizer.youtube.model.common import PageInfo


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PlaylistItemDetails(dataclasses_json.DataClassJsonMixin):
    video_id: str


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PlaylistItem(dataclasses_json.DataClassJsonMixin):
    content_details: PlaylistItemDetails


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PlaylistItems(dataclasses_json.DataClassJsonMixin):
    items: tuple[PlaylistItem, ...] = tuple()
    page_info: PageInfo = PageInfo(total_results=0, results_per_page=0)
    next_page_token: str | None = None
