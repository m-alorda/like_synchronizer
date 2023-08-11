import logging
from pathlib import Path

import google_auth_oauthlib.flow
import google.oauth2.credentials


from like_synchronizer.config import PROJECT_DIR, YOUTUBE_SECRET_FILE_PATH, config

_YOUTUBE_API_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
]
_CACHED_CLIENT_CREDS_FILE = (
    PROJECT_DIR / config["secrets"]["path"] / "cached_youtube_client_creds.json"
)


log = logging.getLogger("like_synchronizer.youtube.credentials_handler")


def _request_user_credentials(
    cache_file: Path | None = None,
) -> google.oauth2.credentials.Credentials:
    log.debug("Requesting new user credentials")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=str(YOUTUBE_SECRET_FILE_PATH),
        scopes=_YOUTUBE_API_SCOPES,
    )
    credentials = flow.run_local_server()
    if cache_file is not None:
        with cache_file.open("w") as f:
            f.write(credentials.to_json())
    return credentials


def get_user_credentials() -> google.oauth2.credentials.Credentials:
    if not _CACHED_CLIENT_CREDS_FILE.exists():
        return _request_user_credentials(_CACHED_CLIENT_CREDS_FILE)

    credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(
        filename=str(_CACHED_CLIENT_CREDS_FILE),
        scopes=_YOUTUBE_API_SCOPES,
    )
    if not credentials.valid:
        log.debug("Cached user credentials are invalid or expired. Requesting again")
        return _request_user_credentials(_CACHED_CLIENT_CREDS_FILE)
    log.debug("Returning cached user credentials")
    return credentials
