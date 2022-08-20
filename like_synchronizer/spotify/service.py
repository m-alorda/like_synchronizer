import logging

import spotipy

import config

log = logging.getLogger("spotify_service")


_SPOTIFY_API_SCOPE = "user-library-read"
_CACHED_CLIENT_CREDS_FILE = (
    config.PROJECT_DIR
    / config.config["secrets"]["path"]
    / "cached_spotify_client_creds.json"
)


def _get_spotify_service() -> spotipy.Spotify:
    log.debug("Building spotify service")
    return spotipy.Spotify(
        auth_manager=spotipy.SpotifyOAuth(
            client_id=config.secret_config["spotify"]["clientId"],
            client_secret=config.secret_config["spotify"]["clientSecret"],
            redirect_uri=config.secret_config["spotify"]["redirectURI"],
            scope=_SPOTIFY_API_SCOPE,
            cache_handler=spotipy.CacheFileHandler(
                cache_path=str(_CACHED_CLIENT_CREDS_FILE)
            ),
        )
    )
