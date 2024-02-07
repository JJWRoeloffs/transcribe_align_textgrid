from __future__ import annotations

from typing import Dict, List, cast

from praatio.data_classes.interval_tier import IntervalTier
from praatio.data_classes.textgrid import Textgrid
from praatio.utilities.constants import Interval

from transcribe_align_textgrid.whisper_schema import WHISPER_VALIDATOR


def _fill_if_empty(entries: List[Interval]) -> List[Interval]:
    """Adds an empty interval from 0.0 to 0.1 when the list inputted is empy"""
    return entries if entries else [Interval(start=0.0, end=0.1, label="")]


def _remove_empty(grid: Textgrid) -> Textgrid:
    """Removes any empty intervals from the textgrid.

    This includes intervals that were created by fill_if_empty.
    At this point, those have done their job at making the textgrid createble, and can be removed
    """
    # Don't itterate over what you plan to modify
    for tiername in grid.tierNames:
        tier = grid.getTier(tiername)
        assert isinstance(tier, IntervalTier)
        empty_intervals = cast(List[Interval], [i for i in tier.entries if not i.label])
        for interval in empty_intervals:
            tier.deleteEntry(interval)
    return grid


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
        return IntervalTier("segments_text", _fill_if_empty(entries))

    def to_segment_confidence_tier(self) -> IntervalTier:
        entries = [x.to_confidence_interval() for x in self.segments]
        return IntervalTier("segments_confidence", _fill_if_empty(entries))

    def to_word_text_tier(self) -> IntervalTier:
        entries = [x.to_text_interval() for y in self.segments for x in y.words]
        return IntervalTier("words_text", _fill_if_empty(entries))

    def to_word_confidence_tier(self) -> IntervalTier:
        entries = [x.to_confidence_interval() for y in self.segments for x in y.words]
        return IntervalTier("words_confidence", _fill_if_empty(entries))


def whisper_to_textgrid(whisper_timestamped_output: Dict) -> Textgrid:
    """Turn the output of Whisper-timestamped into a textgrid

    Input: whisper_timestamped_output: Dict, in the shape of whisper_timestamped.transcribe()
    Returns: praatio TextGrid glass with four interval tiers:
        segments_text: The text containing the continuous speech of one speaker
        segments_confidence: How confident the model was in labeling the above
        words_text: The individually aligned words
        words_confidence: how confident the model was in labeling the above
    """
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

    textgrid = _remove_empty(textgrid)

    if not textgrid.validate():
        raise ValueError("The provided whisper input resulted in an invalid TextGrid")

    return textgrid
