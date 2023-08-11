import dataclasses

import dataclasses_json


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class ChannelDetails(dataclasses_json.DataClassJsonMixin):
    relatedPlaylists: dict[str, str] = dataclasses.field(default_factory=dict)


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class Channel(dataclasses_json.DataClassJsonMixin):
    contentDetails: ChannelDetails = ChannelDetails()


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class ChannelsPage(dataclasses_json.DataClassJsonMixin):
    items: tuple[Channel, ...] = tuple()
