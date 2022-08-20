import logging

import spotify.service
import youtube.service
import model

log = logging.getLogger()


def main():
    try:
        for video in youtube.service.get_liked_music_videos():
            log.debug(f"Liked video: '{video.snippet.title}'")
            song = model.Song.from_video_title(video.snippet.title)
    except KeyboardInterrupt:
        log.info("Finishing execution")


if __name__ == "__main__":
    log.info(spotify.service._get_spotify_service().search("lovesick"))
    # main()
