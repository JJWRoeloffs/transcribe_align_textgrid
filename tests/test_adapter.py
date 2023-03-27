from __future__ import annotations

from transcribe_allign_textgrid import whisper_to_textgrid
from .helpers import get_json_data


class TestAdapterValidation:
    data = get_json_data(["data"])

    def test_adapter_validation(self):
        assert self.data
        for item in self.data:
            whisper_to_textgrid(item)
