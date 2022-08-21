import logging
from pathlib import Path
import time

from like_synchronizer.spotify.like_processor import LikeProcessor
from like_synchronizer.youtube.service import get_liked_music_videos
from like_synchronizer.song import Song

log = logging.getLogger("like_synchronizer.core")

MILLIS_TO_WAIT = 1_000


def youtube_to_spotify(not_found_likes_file: Path | None = None):
    with LikeProcessor(not_found_likes_file) as like_processor:
        num_processed_videos = 0
        for video in get_liked_music_videos():
            log.debug(f"Processing youtube liked video: '{video.snippet.title}'")
            song = Song.from_video_title(video.snippet.title)
            like_processor.like(song)
            if num_processed_videos % 10 == 0:
                log.debug(f"Waiting for {MILLIS_TO_WAIT} ms due to API quotas")
                time.sleep(MILLIS_TO_WAIT / 1_000)
            num_processed_videos += 1
