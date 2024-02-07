from jsonschema import Draft202012Validator

WHISPER_SCHEMA = {
    "type": "object",
    "properties": {
        "text": {"type": "string"},
        "segments": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer", "minimum": 0},
                    "start": {"type": "number", "minimum": 0},
                    "end": {"type": "number", "minimum": 0},
                    "text": {"type": "string"},
                    "tokens": {
                        "type": "array",
                        "items": {"type": "integer", "minimum": 0, "maximum": 51864},
                    },
                    "temperature": {"type": "number", "minimum": 0, "maximum": 1},
                    "avg_logprob": {"type": "number", "maximum": 0},
                    "compression_ratio": {"type": "number", "minimum": 0},
                    "no_speech_prob": {"type": "number", "minimum": 0, "maximum": 1},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "words": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "text": {"type": "string"},
                                "start": {"type": "number", "minimum": 0},
                                "end": {"type": "number", "minimum": 0},
                                "confidence": {
                                    "type": "number",
                                    "minimum": 0,
                                    "maximum": 1,
                                },
                            },
                        },
                    },
                },
            },
            "minItems": 0,
            "uniqueItems": True,
        },
    },
}

WHISPER_VALIDATOR = Draft202012Validator(schema=WHISPER_SCHEMA)
