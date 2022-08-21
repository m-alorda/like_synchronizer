import dataclasses
import logging
import json
from pathlib import Path

import dataclasses_json
import pytest

from like_synchronizer.spotify.model import Track
from like_synchronizer.spotify.search_result_selector import (
    MINIMUM_RECOMMENDED_SIMILARITY,
    choose_best_search_result,
)


log = logging.getLogger("like_synchronizer.test_song_model")

TESTS_DATA_DIR = Path(__file__).absolute().parent / "data"
SAMPLE_DATA_FILE = TESTS_DATA_DIR / "spotify_search_selector_sample_data.json"


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.SNAKE,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class SearchResultTestData(dataclasses_json.DataClassJsonMixin):
    query: str
    tracks_search_results: tuple[Track, ...]
    expected_selected_track: Track | None


class TestSearchResultSelector:
    def _search_matches_expected(self, test: SearchResultTestData) -> bool:
        similarity, track = choose_best_search_result(
            test.query, test.tracks_search_results
        )
        if similarity < MINIMUM_RECOMMENDED_SIMILARITY:
            if test.expected_selected_track is None:
                return True
            log.warning(
                f"Search result selector failed.\n"
                f"Similarity is below minimum recommended ({similarity:0.4f} < "
                f"{MINIMUM_RECOMMENDED_SIMILARITY:0.4f}), but expected track is not None\n"
                f"Query: '{test.query}'\n"
                f"Expected track: '{test.expected_selected_track}'\n"
                f"Actual track: '{track}'"
            )
            return False
        if track != test.expected_selected_track:
            log.warning(
                f"Search result selector failed\n"
                f"Query: '{test.query}'\n"
                f"Expected track: '{test.expected_selected_track}'\n"
                f"Actual track: '{track}'"
            )
            return False
        return True

    def test_search_result_selector(self):
        max_allowed_error_rate = 0.10

        with SAMPLE_DATA_FILE.open() as f:
            json_test_data = json.load(f)
        test_data = tuple(
            SearchResultTestData.from_dict(json_data) for json_data in json_test_data
        )
        log.info(f"Found {len(test_data)} tests")

        num_total_tests = 0
        num_failed_tests = 0
        for test in test_data:
            if not self._search_matches_expected(test):
                num_failed_tests += 1
            num_total_tests += 1
            if num_total_tests % 10 == 0:
                log.debug(
                    f"Current parse error rate: {num_failed_tests} / {num_total_tests}"
                )
        error_rate_percentage = num_failed_tests / num_total_tests * 100
        log.info(
            f"Parse error rate: {num_failed_tests} / {num_total_tests} ({error_rate_percentage:.2f}%)"
        )
        assert num_failed_tests / num_total_tests < max_allowed_error_rate


if __name__ == "__main__":
    pytest.main()
