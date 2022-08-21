import logging

from like_synchronizer.spotify.search_result_selector import (
    MINIMUM_RECOMMENDED_SIMILARITY,
    choose_best_search_result,
)
from like_synchronizer.spotify.service import search_track, save_user_tracks
from like_synchronizer.youtube.service import get_liked_music_videos
from like_synchronizer.song import Song

log = logging.getLogger("like_synchronizer.core")


def youtube_to_spotify():
    for video in get_liked_music_videos():
        log.debug(f"Processing youtube liked video: '{video.snippet.title}'")
        song = Song.from_video_title(video.snippet.title)

        # TODO  Do all this with a context manager?
        #   with spotify.service.BatchLikeProcessor() as x: ...
        search_query = f"{song.artist} {song.title}"
        found_tracks = search_track(search_query)

        if found_tracks.total <= 0:
            log.warning("No results found for search: '{search_query}'")
            # TODO keep for later to manually check
            continue

        similary, track = choose_best_search_result(search_query, found_tracks.items)
        if similary < MINIMUM_RECOMMENDED_SIMILARITY:
            log.warning(f"No viable result found for search: '{search_query}'")
            # TODO keep for later to manually check
            continue

        log.info(
            f"Liking track '{' '.join(track.artists_names)} {track.name}' from youtube video '{song.original_title}'"
        )
        save_user_tracks((track.id,))
        # TODO Once the method is refined, there should be no need to stop
        # (maybe sleep to prevent exceeding API quotas)
        input("Press enter to process next video: ")
