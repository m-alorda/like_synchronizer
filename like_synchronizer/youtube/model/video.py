import dataclasses

import dataclasses_json

from like_synchronizer.youtube.model.common import PageInfo


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class VideoTopicDetails:
    topicCategories: tuple[str, ...]


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
    topicDetails: VideoTopicDetails = VideoTopicDetails(topicCategories=tuple())


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class VideosPage(dataclasses_json.DataClassJsonMixin):
    items: tuple[Video, ...] = tuple()
    pageInfo: PageInfo = PageInfo(totalResults=0, resultsPerPage=0)
    nextPageToken: str | None = None
