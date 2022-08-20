import logging
from pathlib import Path
from typing import Iterable

import google_auth_oauthlib.flow
import google.oauth2.credentials
import googleapiclient.discovery

import config
import youtube.model


log = logging.getLogger("youtube_service")


_YOUTUBE_API_SCOPES = [
    "https://www.googleapis.com/auth/youtube.readonly",
]
_CACHED_CLIENT_CREDS_FILE = (
    config.PROJECT_DIR / config.config["secrets"]["path"] / "cached_client_creds.json"
)


def _request_user_credentials(
    cache_file: Path | None = None,
) -> google.oauth2.credentials.Credentials:
    log.debug("Requesting new user credentials")
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file=str(config.YOUTUBE_SECRET_FILE_PATH),
        scopes=_YOUTUBE_API_SCOPES,
    )
    credentials = flow.run_local_server()
    if cache_file is not None:
        with cache_file.open("w") as f:
            f.write(credentials.to_json())
    return credentials


def _get_user_credentials() -> google.oauth2.credentials.Credentials:
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


def _get_youtube_service():
    log.debug("Building youtube service")
    return googleapiclient.discovery.build(
        serviceName="youtube",
        version="v3",
        credentials=_get_user_credentials(),
    )


def _request_liked_videos(
    next_page_token: str | None = None,
) -> youtube.model.VideosPage:
    log.debug(f"Requesting videos for page {next_page_token}")
    response = (
        _get_youtube_service()
        .videos()
        .list(
            part="snippet,topicDetails",
            myRating="like",
            fields="items(snippet/title,topicDetails/topicCategories),pageInfo,nextPageToken",
            maxResults=config.config["youtube"]["batchVideoSize"],
            pageToken=next_page_token,
        )
    ).execute()
    return youtube.model.VideosPage.from_dict(response)


def _is_music_video(video: youtube.model.Video) -> bool:
    is_music_video = any(
        category.lower().find("music") > 0
        for category in video.topicDetails.topicCategories
    )
    log.debug(f"Video '{video.snippet.title}' is music video: {is_music_video}")
    return is_music_video


def get_liked_music_videos() -> Iterable[youtube.model.Video]:
    """Returns the titles of the videos liked by the user"""
    log.info("Requesting music videos liked by the user")

    videos = _request_liked_videos()
    processed_videos = 0
    log.info(f"Liked videos found: {videos.pageInfo.totalResults}")
    while processed_videos < videos.pageInfo.totalResults:
        yield from filter(_is_music_video, videos.items)
        processed_videos += videos.pageInfo.resultsPerPage
        log.info(
            f"Processed liked videos {processed_videos}/{videos.pageInfo.totalResults}"
        )
        input(f"Press enter to continue requesting more liked videos: ")
        videos = _request_liked_videos(videos.nextPageToken)


if __name__ == "__main__":
    print(video_title for video_title in get_liked_music_videos())
