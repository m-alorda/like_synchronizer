import dataclasses

import dataclasses_json


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class PageInfo:
    totalResults: int
    resultsPerPage: int
