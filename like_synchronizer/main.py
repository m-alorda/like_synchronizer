import logging

import spotify.service
import youtube.service
import model

log = logging.getLogger()

# TODO Rename this file to core.py and add cli with `fire`
def main():
    try:
        for video in youtube.service.get_liked_music_videos():
            log.debug(f"Processing youtube liked video: '{video.snippet.title}'")
            song = model.Song.from_video_title(video.snippet.title)
            search_query = f"{song.artist} {song.title}"
            # TODO  Do all this with a context manager?
            #   with spotify.service.BatchLikeProcessor() as x: ...
            found_tracks = spotify.service.search_track(search_query)
            if found_tracks.total <= 0:
                log.warning("No results found for search: '{search_query}'")
                # TODO keep for later to manually check
            log.info(f"Found tracks: {found_tracks}")
            # TODO Correlate the search query with the results, and like the
            # one with highest correlation (if max correlation is below a
            # threshold, keep to manually check later)
            return
    except KeyboardInterrupt:
        log.info("Finishing execution")


if __name__ == "__main__":
    main()
