import fire

import like_synchronizer


class LikeSynchronizerProxy:
    def youtube_to_spotify(self) -> None:
        like_synchronizer.youtube_to_spotify()


def main():
    try:
        fire.Fire(LikeSynchronizerProxy)
    except KeyboardInterrupt:
        print()  # Add new line at the end


if __name__ == "__main__":
    main()
