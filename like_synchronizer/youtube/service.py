import logging
from typing import Iterable

import googleapiclient.discovery

from like_synchronizer.config import config
from like_synchronizer.youtube.credentials_handler import get_user_credentials
from like_synchronizer.youtube.model.video import VideosPage, Video
from like_synchronizer.youtube.model.channel import ChannelsPage
from like_synchronizer.youtube.model.playlist import PlaylistItems


log = logging.getLogger("like_synchronizer.youtube.service")


def _get_youtube_service():
    log.debug("Building youtube service")
    return googleapiclient.discovery.build(
        serviceName="youtube",
        version="v3",
        credentials=get_user_credentials(),
    )


def _request_playlist_videos(
    playlist_id: str,
    page_token: str | None = None,
) -> PlaylistItems:
    log.debug(f"Requesting playlist videos {playlist_id} for page {page_token}")
    response = (
        _get_youtube_service()
        .playlistItems()
        .list(
            playlistId=playlist_id,
            part="contentDetails",
            fields="items(contentDetails/videoId),pageInfo,nextPageToken",
            maxResults=config["youtube"]["batchVideoSize"],
            pageToken=page_token,
        )
        .execute()
    )
    return PlaylistItems.from_dict(response)


def _request_videos(ids: Iterable[str]) -> VideosPage:
    log.debug(f"Requesting videos {ids}")
    response = (
        _get_youtube_service()
        .videos()
        .list(
            part="snippet,topicDetails",
            id=list(ids),
            fields="items(snippet/title,topicDetails/topicCategories)",
            maxResults=config["youtube"]["batchVideoSize"],
        )
        .execute()
    )
    return VideosPage.from_dict(response)


def _is_music_video(video: Video) -> bool:
    suspiciousTitleLength = config["youtube"]["suspiciousTitleLength"]
    if len(video.snippet.title) > suspiciousTitleLength:
        shortened_title = f"{video.snippet.title[:suspiciousTitleLength-1]}..."
        log.warning(
            f"Found suspiciously large video title. Ignoring it: '{shortened_title}'"
        )
        return False

    is_music_video = any(
        category.lower().find("music") > 0
        for category in video.topicDetails.topicCategories
    )
    log.debug(f"Video '{video.snippet.title}' is music video: {is_music_video}")
    return is_music_video


def _request_liked_videos_playlist_id() -> str:
    response = (
        _get_youtube_service()
        .channels()
        .list(
            part="contentDetails",
            mine=True,
            fields="items(contentDetails/relatedPlaylists)",
        )
        .execute()
    )
    channels = ChannelsPage.from_dict(response)
    user_channel = channels.items[0]
    return user_channel.contentDetails.relatedPlaylists["likes"]


def get_liked_music_videos() -> Iterable[Video]:
    """Returns the titles of the videos liked by the user"""
    log.info("Requesting music videos liked by the user")
    playlist_id = _request_liked_videos_playlist_id()
    playlist_videos = _request_playlist_videos(playlist_id)
    processed_videos = 0
    log.info(f"Liked videos found: {playlist_videos.pageInfo.totalResults}")
    while processed_videos < playlist_videos.pageInfo.totalResults:
        videos = _request_videos(
            video.contentDetails.videoId for video in playlist_videos.items
        )
        yield from (video for video in videos.items if _is_music_video(video))
        processed_videos += len(playlist_videos.items)
        log.info(
            f"Processed liked videos {processed_videos}/{playlist_videos.pageInfo.totalResults}"
        )
        if (
            playlist_videos.nextPageToken is None
            and processed_videos < playlist_videos.pageInfo.totalResults
        ):
            log.warn(f"The API is not returning any more results")
            break
        playlist_videos = _request_playlist_videos(
            playlist_id, playlist_videos.nextPageToken
        )
