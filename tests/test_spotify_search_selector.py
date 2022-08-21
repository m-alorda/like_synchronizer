import dataclasses

import dataclasses_json

from like_synchronizer.spotify.model import Track


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class SearchResultTestData(dataclasses_json.DataClassJsonMixin):
    query: str
    tracks_search_results: tuple[Track, ...]
    expected_selected_track: Track | None
