import dataclasses

import dataclasses_json


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
class LikedVideo:
    snippet: VideoSnippet = VideoSnippet(title="")
    topicDetails: VideoTopicDetails = VideoTopicDetails(topicCategories=tuple())


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PageInfo:
    totalResults: int
    resultsPerPage: int


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class VideosData(dataclasses_json.DataClassJsonMixin):
    items: tuple[LikedVideo, ...] = tuple()
    pageInfo: PageInfo = PageInfo(totalResults=0, resultsPerPage=0)
    nextPageToken: str | None = None
