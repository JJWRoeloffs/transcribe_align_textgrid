from __future__ import annotations

from transcribe_align_textgrid import whisper_to_textgrid
from .helpers import get_json_data, get_textgrid_data


class TestAdapterValidation:
    data = get_json_data("data")

    def test_adapter_validation(self):
        assert self.data
        for item in self.data.values():
            whisper_to_textgrid(item)


class TestAdapterGeneration:
    input = get_json_data("data")
    output = get_textgrid_data("expected")

    def test_adapter_generation(self):
        assert self.input
        assert self.output
        textgrids = {k: whisper_to_textgrid(v) for k, v in self.input.items()}
        assert all([grid.validate()] for grid in textgrids.values())
        for name, item in self.output.items():
            assert textgrids[name] == item
