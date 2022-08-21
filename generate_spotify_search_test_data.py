import csv
import logging
from pathlib import Path
import json
import time

from like_synchronizer.spotify.service import search_track
from tests.test_song_model import SAMPLE_DATA_FILE
from tests.test_spotify_search_selector import SearchResultTestData

log = logging.getLogger("like_synchronizer.spotify.search_selector.data_generator")

TESTS_DATA_DIR = Path(__file__).absolute().parent / "tests" / "data"
RESULT_DATA_FILE = TESTS_DATA_DIR / "spotify_search_selector_sample_data.json"


def generate_search_result_data(query: str) -> SearchResultTestData:
    found_tracks = search_track(query).items
    return SearchResultTestData(
        query=query,
        tracks_search_results=found_tracks,
        expected_selected_track=None,
    )


def generate_data() -> None:
    output_data: list[SearchResultTestData] = []
    with SAMPLE_DATA_FILE.open(encoding="utf-8") as f:
        num_processed_queries = 0
        for row in csv.DictReader(f):
            query = f"{row['expected_artist']} {row['expected_title']}"
            log.info(f"Generating test data for '{query}'")
            output_data.append(generate_search_result_data(query))
            if num_processed_queries % 10 == 0:
                log.debug(f"Waiting for 500ms to prevent api usage limit")
                time.sleep(0.5)
            num_processed_queries += 1
        log.info(f"Processed {num_processed_queries} searches")
        log.info(f"Output data can be found in file '{RESULT_DATA_FILE}'")
        log.info("Do not forget to edit the expected selected track")
    serializable_output_data = tuple(test_data.to_dict() for test_data in output_data)
    with RESULT_DATA_FILE.open("w") as f:
        json.dump(serializable_output_data, f)


if __name__ == "__main__":
    if RESULT_DATA_FILE.exists():
        log.warning(
            f"Already existent output data is going to be overridden ('{RESULT_DATA_FILE}')\n"
            "Do you want to proceed? [y/N]"
        )
        proceed = input().lower()
        if proceed != "y":
            exit(1)
    generate_data()
