from __future__ import annotations

from typing import Dict

from praatio.data_classes.textgrid_tier import TextgridTier

from transcribe_allign_textgrid.whisper_schema import WHISPER_VALIDATOR


def whisper_to_textgrid(whisper_timestamped_output: Dict) -> TextgridTier:
    WHISPER_VALIDATOR.validate(whisper_timestamped_output)
