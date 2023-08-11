import dataclasses

import dataclasses_json

from like_synchronizer.youtube.model.common import PageInfo


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class VideoTopicDetails:
    topic_categories: tuple[str, ...]


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class VideoSnippet:
    title: str


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class Video:
    snippet: VideoSnippet = VideoSnippet(title="")
    topic_details: VideoTopicDetails = VideoTopicDetails(topic_categories=tuple())


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class VideosPage(dataclasses_json.DataClassJsonMixin):
    items: tuple[Video, ...] = tuple()
    page_info: PageInfo = PageInfo(total_results=0, results_per_page=0)
    next_page_token: str | None = None
