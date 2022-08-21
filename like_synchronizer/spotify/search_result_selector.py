"""Allows selecting the closest search result from the initial query

Based on <https://towardsdatascience.com/calculating-string-similarity-in-python-276e18a7d33a>
"""
import logging
from typing import Collection

from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

from like_synchronizer.spotify.model import Track
from like_synchronizer.cleaner import (
    TextCleaner,
    TextCleanerWrapper,
    AsciiConverter,
    LowerCaseConverter,
    PunctuationRemover,
    StopWordRemover,
)

MINIMUM_RECOMMENDED_SIMILARITY = 0.8


log = logging.getLogger("like_synchronizer.spotify.search_selector")


_TEXT_CLEANER: TextCleaner = TextCleanerWrapper(
    AsciiConverter(),
    LowerCaseConverter(),
    PunctuationRemover(),
    StopWordRemover(),
)


def _clean_text(text: str) -> str:
    log.debug(f"Cleaning: '{text}'")
    result = _TEXT_CLEANER.clean(text)
    log.debug(f"Cleaned: '{result}'")
    return result


def _to_vector_space(similar_texts: Collection[str]) -> np.matrix:
    return CountVectorizer().fit_transform(similar_texts).toarray()


def _calculate_similarities(
    reference_value: np.matrix, values: Collection[np.matrix]
) -> tuple[float]:
    return tuple(
        _cosine_similarity_of_vectors(reference_value, value) for value in values
    )


def _cosine_similarity_of_vectors(v1: np.matrix, v2: np.matrix) -> float:
    reshaped_v1 = v1.reshape(1, -1)
    reshaped_v2 = v2.reshape(1, -1)
    return cosine_similarity(reshaped_v1, reshaped_v2)[0][0]


def _extract_artist_and_title(track: Track) -> str:
    artists = " ".join(map(lambda artist: artist.name, track.artists))
    return f"{artists} {track.name}"


def choose_best_search_result(
    search_query: str, tracks: tuple[Track]
) -> tuple[float, Track]:
    """Find the best search result from the given query

    Returns:
        highest_similarity (in range [0,1])
        Track with highest_similarity
    """
    text_tuple = (
        search_query,
        *map(_extract_artist_and_title, tracks),
    )
    cleaned_text = tuple(map(_clean_text, text_tuple))
    text_vectors = _to_vector_space(cleaned_text)
    similarities = _calculate_similarities(text_vectors[0], text_vectors[1:])
    highest_similarity = max(similarities)
    index_of_highest_similarity = similarities.index(highest_similarity)
    search_result = tracks[index_of_highest_similarity]
    return highest_similarity, search_result
