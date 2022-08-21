import fire

import like_synchronizer


class LikeSynchronizerProxy:
    def youtube_to_spotify(self) -> None:
        like_synchronizer.youtube_to_spotify()


def main():
    fire.Fire(LikeSynchronizerProxy)


if __name__ == "__main__":
    main()
