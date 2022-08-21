import logging
from typing import Collection

import spotipy

from like_synchronizer.config import PROJECT_DIR, config, secret_config
from like_synchronizer.spotify.model import SearchResults, TracksResults

log = logging.getLogger("like_synchronizer.spotify_service")

# See <https://developer.spotify.com/documentation/general/guides/authorization/scopes/>
_SPOTIFY_API_SCOPES = "user-library-read,user-library-modify"
_CACHED_CLIENT_CREDS_FILE = (
    PROJECT_DIR / config["secrets"]["path"] / "cached_spotify_client_creds.json"
)


def _get_spotify_service() -> spotipy.Spotify:
    log.debug("Building spotify service")
    return spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=secret_config["spotify"]["clientId"],
            client_secret=secret_config["spotify"]["clientSecret"],
            redirect_uri=secret_config["spotify"]["redirectURI"],
            scope=_SPOTIFY_API_SCOPES,
            cache_handler=spotipy.CacheFileHandler(
                cache_path=str(_CACHED_CLIENT_CREDS_FILE)
            ),
        )
    )


def search_track(query: str) -> TracksResults:
    log.debug("Searching: '{query}'")
    response = _get_spotify_service().search(query, type="track")
    return SearchResults.from_dict(response).tracks


def save_user_tracks(trackIds: Collection[str]) -> None:
    """Maximum 50 tracks can be saved at a time"""
    log.debug(f"Saving user tracks {trackIds}")
    if len(trackIds) > 50:
        raise ValueError("Cannot save more than 50 tracks at a time")
    _get_spotify_service().current_user_saved_tracks_add(trackIds)
