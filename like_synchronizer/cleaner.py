"""Allows cleaning strings (removing punctuation, stop words, convert to ascii...)"""

import logging
import string
from typing import Protocol

from nltk.corpus import stopwords
from unidecode import unidecode

log = logging.getLogger("like_synchronizer.cleaner")


class TextCleaner(Protocol):
    def clean(self, text: str) -> str:
        ...


class TextCleanerWrapper:
    def __init__(self, *cleaners: TextCleaner):
        self._cleaners = cleaners

    def clean(self, text: str) -> str:
        result = text
        for cleaner in self._cleaners:
            result = cleaner.clean(result)
        return result


class PunctuationRemover:
    def clean(self, text: str) -> str:
        return "".join(char for char in text if char not in string.punctuation)


class AsciiConverter:
    def clean(self, text: str) -> str:
        return unidecode(text)


class LowerCaseConverter:
    def clean(self, text: str) -> str:
        return text.lower()


class StopWordRemover:
    @staticmethod
    def _create_stop_words() -> set[str]:
        stop_word_cleaner = TextCleanerWrapper(
            AsciiConverter(),
            LowerCaseConverter(),
            PunctuationRemover(),
        )
        return set(map(stop_word_cleaner.clean, stopwords.words()))

    try:
        _STOP_WORDS = _create_stop_words()
    except LookupError:
        import nltk

        log.debug("Stop words not found. Downloading them...")
        nltk.download("stopwords")
        _STOP_WORDS = _create_stop_words()

    def clean(self, text: str) -> str:
        return " ".join(word for word in text.split() if word not in self._STOP_WORDS)
