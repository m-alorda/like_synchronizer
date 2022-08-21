import logging

from like_synchronizer.spotify.service import search_track
from like_synchronizer.youtube.service import get_liked_music_videos
from like_synchronizer.model import Song

log = logging.getLogger("like_synchronizer.core")


def youtube_to_spotify():
    for video in get_liked_music_videos():
        log.debug(f"Processing youtube liked video: '{video.snippet.title}'")
        song = Song.from_video_title(video.snippet.title)
        search_query = f"{song.artist} {song.title}"
        # TODO  Do all this with a context manager?
        #   with spotify.service.BatchLikeProcessor() as x: ...
        found_tracks = search_track(search_query)
        if found_tracks.total <= 0:
            log.warning("No results found for search: '{search_query}'")
            # TODO keep for later to manually check
        log.info(f"Found tracks: {found_tracks}")
        # TODO Correlate the search query with the results, and like the
        # one with highest correlation (if max correlation is below a
        # threshold, keep to manually check later)
        # return
