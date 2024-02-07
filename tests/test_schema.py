from jsonschema import Draft202012Validator
from transcribe_align_textgrid.whisper_schema import WHISPER_SCHEMA


class TestSchema:
    def test_schema(self):
        Draft202012Validator.check_schema(schema=WHISPER_SCHEMA)
