import logging

import youtube.service

log = logging.getLogger()


def main():
    try:
        for video in youtube.service.get_liked_music_videos():
            # TODO try to extract video title and artist from the youtube title
            # https://pypi.org/project/youtube-title-parse/
            log.debug(f"Liked video: '{video.snippet.title}'")
    except KeyboardInterrupt:
        log.info("Finishing execution")


if __name__ == "__main__":
    main()
