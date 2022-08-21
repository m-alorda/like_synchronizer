from pathlib import Path
import fire

import like_synchronizer

DEFAULT_MISSED_LIKES_FILE = Path("missed_likes.json")


class LikeSynchronizerProxy:
    def youtube_to_spotify(
        self,
        not_found_likes_file: Path | None = DEFAULT_MISSED_LIKES_FILE,
    ) -> None:
        like_synchronizer.youtube_to_spotify(not_found_likes_file)


def main():
    try:
        fire.Fire(LikeSynchronizerProxy)
    except KeyboardInterrupt:
        print()  # Add new line at the end


if __name__ == "__main__":
    main()
