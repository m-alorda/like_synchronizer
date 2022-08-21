import logging
from pathlib import Path
from types import TracebackType
import json
import dataclasses

import dataclasses_json


from like_synchronizer.spotify.model import Track, TracksResults
from like_synchronizer.spotify.service import (
    SPOTIFY_MAX_ALLOWED_BATCH_ITEMS,
    save_user_tracks,
    search_track,
)
from like_synchronizer.spotify.search_result_selector import (
    MINIMUM_RECOMMENDED_SIMILARITY,
    choose_best_search_result,
)
from like_synchronizer.song import Song


log = logging.getLogger("like_synchronizer.spotify.like_processor")


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class MissedLikeFoundTrack:
    artist_and_name: str
    url: str | None = None

    @classmethod
    def from_track(cls, track: Track) -> "MissedLikeFoundTrack":
        return MissedLikeFoundTrack(
            artist_and_name=f"{' '.join(track.artists_names)} {track.name}",
            url=track.external_urls.spotify,
        )


@dataclasses_json.dataclass_json(
    letter_case=dataclasses_json.LetterCase.CAMEL,
    undefined=dataclasses_json.Undefined.EXCLUDE,
)
@dataclasses.dataclass(frozen=True)
class MissedLike(dataclasses_json.DataClassJsonMixin):
    original_song_title: str
    found_tracks: tuple[MissedLikeFoundTrack, ...]


class LikeHandler:
    def __init__(self):
        self._pending_likes: list[str] = []
        self._missed_likes: list[MissedLike] = []
        self._num_requested_likes = 0
        self._num_successful_likes = 0

    def _add_pending_like(self, track_id: str) -> None:
        self._pending_likes.append(track_id)
        self._num_successful_likes += 1
        if len(self._pending_likes) >= SPOTIFY_MAX_ALLOWED_BATCH_ITEMS:
            # TODO Should not happen, but what if
            # `len(self._pending_likes) > SPOTIFY_MAX_ALLOWED_BATCH_ITEMS`?
            self.flush()

    def _add_missed_like(self, song: Song, found_tracks: TracksResults) -> None:
        self._missed_likes.append(
            MissedLike(
                original_song_title=song.original_title,
                found_tracks=tuple(
                    MissedLikeFoundTrack.from_track(track)
                    for track in found_tracks.items
                ),
            )
        )

    def like(self, song: Song) -> None:
        self._num_requested_likes += 1

        search_query = (
            f"{song.artist} {song.title}"
            if song.artist is not None and song.title is not None
            else song.original_title
        )
        found_tracks = search_track(search_query)

        if found_tracks.total <= 0:
            log.warning(f"No results found for search: '{search_query}'")
            self._add_missed_like(song, found_tracks)
            return

        similarity, track = choose_best_search_result(search_query, found_tracks.items)
        if similarity < MINIMUM_RECOMMENDED_SIMILARITY:
            log.warning(f"No viable result found for search: '{search_query}'")
            self._add_missed_like(song, found_tracks)
            return

        log.info(
            f"Liking track '{' '.join(track.artists_names)} {track.name}' from song '{song.original_title}'"
        )
        self._add_pending_like(track.id)

    def flush(self) -> None:
        log.debug(f"Flushing {len(self._pending_likes)} pending likes")
        save_user_tracks(self._pending_likes)
        self._pending_likes = []

    def write_missed_likes(self, not_found_likes_file: Path) -> None:
        log.info(f"Current number of successful likes: {self._num_successful_likes}")
        log.info(f"Current number of missed likes: {len(self._missed_likes)}")
        log.info(f"Current number of requested likes: {self._num_requested_likes}")
        log.info(f"Writing missed likes to file '{not_found_likes_file}'")
        missed_likes_as_dict = tuple(
            map(
                lambda missed_like: missed_like.to_dict(),
                self._missed_likes,
            )
        )
        with not_found_likes_file.open("w") as f:
            json.dump(missed_likes_as_dict, f)


class LikeProcessor:
    def __init__(self, not_found_likes_file: Path | None = None):
        self._not_found_likes_file = not_found_likes_file
        self._like_handler = LikeHandler()

    def __enter__(self) -> LikeHandler:
        return self._like_handler

    def __exit__(
        self,
        exc_type: BaseException | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._like_handler.flush()
        if self._not_found_likes_file is not None:
            self._like_handler.write_missed_likes(self._not_found_likes_file.absolute())
