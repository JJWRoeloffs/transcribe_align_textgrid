from __future__ import annotations

from typing import Dict, List

from praatio.data_classes.interval_tier import IntervalTier
from praatio.data_classes.textgrid import Textgrid
from praatio.utilities.constants import Interval

from transcribe_allign_textgrid.whisper_schema import WHISPER_VALIDATOR


def fill_if_empty(entries: List[Interval]) -> List[Interval]:
    return entries if entries else [Interval(start=0.0, end=0.1, label="")]


class WhisperWord:
    def __init__(self, whisper_word: Dict) -> None:
        self.text = str(whisper_word["text"])
        self.start = float(whisper_word["start"])
        self.end = float(whisper_word["end"])
        self.confidence = float(whisper_word["confidence"])

    def to_text_interval(self) -> Interval:
        return Interval(start=self.start, end=self.end, label=self.text)

    def to_confidence_interval(self) -> Interval:
        return Interval(start=self.start, end=self.end, label=str(self.confidence))


class WhisperSegment:
    def __init__(self, whisper_segment: Dict) -> None:
        self.text = str(whisper_segment["text"])
        self.start = float(whisper_segment["start"])
        self.end = float(whisper_segment["end"])
        self.confidence = float(whisper_segment["confidence"])
        self.words = [WhisperWord(x) for x in whisper_segment["words"]]

    def to_text_interval(self) -> Interval:
        return Interval(start=self.start, end=self.end, label=self.text)

    def to_confidence_interval(self) -> Interval:
        return Interval(start=self.start, end=self.end, label=str(self.confidence))


class WhisperObject:
    def __init__(self, wt_output: Dict) -> None:
        self.text = str(wt_output["text"])
        self.segments = [WhisperSegment(x) for x in wt_output["segments"]]

    def to_segment_text_tier(self) -> IntervalTier:
        entries = [x.to_text_interval() for x in self.segments]
        return IntervalTier("segments_text", fill_if_empty(entries))

    def to_segment_confidence_tier(self) -> IntervalTier:
        entries = [x.to_confidence_interval() for x in self.segments]
        return IntervalTier("segments_confidence", fill_if_empty(entries))

    def to_word_text_tier(self) -> IntervalTier:
        entries = [x.to_text_interval() for y in self.segments for x in y.words]
        return IntervalTier("words_text", fill_if_empty(entries))

    def to_word_confidence_tier(self) -> IntervalTier:
        entries = [x.to_confidence_interval() for y in self.segments for x in y.words]
        return IntervalTier("words_confidence", fill_if_empty(entries))


def whisper_to_textgrid(whisper_timestamped_output: Dict) -> Textgrid:
    try:
        WHISPER_VALIDATOR.validate(whisper_timestamped_output)
    except Exception as err:
        raise ValueError(f"Error converting Whisper-timestamped to Textgrid: {err}")

    whisper_object = WhisperObject(whisper_timestamped_output)

    textgrid = Textgrid()
    textgrid.addTier(whisper_object.to_segment_text_tier())
    textgrid.addTier(whisper_object.to_segment_confidence_tier())
    textgrid.addTier(whisper_object.to_word_text_tier())
    textgrid.addTier(whisper_object.to_word_confidence_tier())

    if not textgrid.validate():
        raise ValueError("The provided whisper input resulted in an invalid TextGrid")

    return textgrid
