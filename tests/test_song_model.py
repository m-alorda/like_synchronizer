import logging
import csv
from pathlib import Path


import pytest

from like_synchronizer import model

log = logging.getLogger("like_synchronizer.test_song_model")

TESTS_DATA_DIR = Path(__file__).absolute().parent / "data"


class TestSongModel:
    def _title_matches_expected(
        self,
        video_title: str,
        expected_artist: str,
        expected_title: str,
    ) -> bool:
        log.debug(
            f"Checking video '{video_title}'. Expected result '{expected_artist}' - '{expected_title}'"
        )
        song = model.Song.from_video_title(video_title)
        log.debug(f"Parsed song: '{song.artist}' - '{song.title}'")
        matches = expected_artist == song.artist and expected_title == song.title
        if not matches:
            log.warning(
                f"Parsing failed for song title '{video_title}'.\n"
                f"    Expected: '{expected_artist}' - '{expected_title}'\n"
                f"    But got '{song.artist}' - '{song.title}'"
            )
        return matches

    def test_from_video_title(self):
        max_allowed_error_rate = 0.15
        sample_data_file = TESTS_DATA_DIR / "youtube_music_video_sample_data.csv"
        num_checked_titles = 0
        num_failed_parses = 0
        with sample_data_file.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if not self._title_matches_expected(
                    video_title=row["video_title"],
                    expected_artist=row["expected_artist"],
                    expected_title=row["expected_title"],
                ):
                    num_failed_parses += 1
                num_checked_titles += 1
                if num_checked_titles % 10 == 0:
                    log.debug(
                        f"Current parse error rate: {num_failed_parses} / {num_checked_titles}"
                    )
        error_rate_percentage = num_failed_parses / num_checked_titles * 100
        log.info(
            f"Parse error rate: {num_failed_parses} / {num_checked_titles} ({error_rate_percentage:.2f}%)"
        )
        assert num_failed_parses / num_checked_titles < max_allowed_error_rate


if __name__ == "__main__":
    pytest.main()
