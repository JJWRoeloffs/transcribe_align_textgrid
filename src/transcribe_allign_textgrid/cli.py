from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from importlib.util import find_spec
from pathlib import Path
from typing import List, Optional

from transcribe_allign_textgrid import whisper_to_textgrid


# Preprocessing: Managing imports that are not in requirements.txt
def check_cli_dependencies() -> bool:
    if shutil.which("ffmpeg") is None:
        print(
            """Dependency ffmpeg is not installed.
            Please install if following the instructions on whisper's documentation:
            https://github.com/openai/whisper-timestamped
            """
        )
        return False

    if find_spec("whisper_timestamped") is None:
        print(
            """Dependency whisper-timestamped is not installed.
            This needs to be installed sperately, as it cannot be installed via pypi
            Please read the requirement documentation on:
            https://github.com/JJWRoeloffs/transcribe_allign_textgrid
            """
        )
        return False
    if find_spec("whisper") is None:
        print(
            """Dependency whisper is not installed.
            This should have been installed as a dependency of whisper-timestamped, but was not.
            It might be wise to reinstall whisper-timestamped, as something clearly went wrong.
            Else, if you want simply want this error to go away, install whisper manually.
            """
        )
        return False

    return True


@dataclass
class Args:
    paths: List[Path]
    model: str
    language: Optional[str]


def get_files(path: Path) -> List[Path]:
    return [path] if path.is_file() else [x for x in path.iterdir() if x.is_file()]


def parse_args(args: List[str]) -> Args:
    parser = argparse.ArgumentParser(
        prog="transcribe_allign_textgrid",
        description="""
            A small wrapper cli around whisper-timestamped.
            Create force-alligned transcription TextGrids from raw audio!
            """,
    )

    if not check_cli_dependencies():
        parser.error("Could not resolve all cli dependencies")

    from whisper import _MODELS
    from whisper.tokenizer import LANGUAGES

    parser.add_argument(
        "paths",
        help="The File(s) or Directory of the to-transcribe audio",
        nargs="+",
    )
    parser.add_argument(
        "--model",
        choices=_MODELS.keys(),
        help="The model size to use for the transcription. Default tiny",
        default="tiny",
        nargs="?",
        required=False,
    )
    parser.add_argument(
        "--language",
        choices=LANGUAGES.values(),
        help="Language size to use for the transcription, Default automatic",
        nargs="?",
        required=False,
    )
    arguments = parser.parse_args(args)
    paths = [Path(x).resolve() for x in arguments.paths]

    for path in paths:
        if not path.exists():
            parser.error(f"Passed path does not exist: {path}")

    paths = [file for path in paths for file in get_files(path)]

    return Args(paths=paths, model=arguments.model, language=arguments.language)


def run(args: Args) -> None:
    if not check_cli_dependencies():
        raise ImportError

    print("Loading Model...")
    import whisper_timestamped

    model = whisper_timestamped.load_model(args.model)

    for path in args.paths:
        print(f"Processing: {str(path.name)}")
        audio = whisper_timestamped.load_audio(str(path))
        result = whisper_timestamped.transcribe(model, audio, language=args.language)
        textgrid = whisper_to_textgrid(result)

        new_name = str(path.with_suffix(".TextGrid"))
        print(f"Saving: {new_name}")
        textgrid.save(new_name, format="long_textgrid", includeBlankSpaces=True)


def main(args: List[str]) -> None:
    run(parse_args(args))
