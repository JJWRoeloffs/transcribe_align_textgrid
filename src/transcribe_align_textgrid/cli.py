from __future__ import annotations

import argparse
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

from whisper import _MODELS
from whisper.tokenizer import LANGUAGES
import whisper_timestamped

from transcribe_align_textgrid import whisper_to_textgrid


@dataclass
class Args:
    paths: List[Path]
    model: str
    language: Optional[str]
    continue_on_err: bool


def parse_path(path: Path) -> List[Path]:
    return [path] if path.is_file() else [x for x in path.iterdir() if x.is_file()]


def parse_glob(pathstr: str) -> List[Path]:
    return list(Path().glob(pathstr))


def parse_pathstr(ctx: argparse.ArgumentParser, pathstr: str) -> List[Path]:
    pathspec = Path(pathstr)
    paths = parse_path(pathspec) if pathspec.exists() else parse_glob(pathstr)
    if not paths:
        ctx.error(f"Could not resolve to filepaths: {pathspec}")
    return [path.resolve() for path in paths]


def parse_args(args: List[str]) -> Args:
    parser = argparse.ArgumentParser(
        prog="transcribe_align_textgrid",
        description="""
            A small wrapper cli around whisper-timestamped.
            Create force-aligned transcription TextGrids from raw audio!
            """,
    )

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
    parser.add_argument(
        "--skip",
        action="store_true",
        help="If passed, any non-audio files passed are skipped.",
        default=False,
        required=False,
    )

    if shutil.which("ffmpeg") is None:
        parser.error(
            """Dependency ffmpeg is not installed.
            Please install if following the instructions on whisper's documentation:
            https://github.com/openai/whisper-timestamped
            """
        )

    arguments = parser.parse_args(args)

    paths = [file for path in arguments.paths for file in parse_pathstr(parser, path)]

    return Args(
        paths=paths,
        model=arguments.model,
        language=arguments.language,
        continue_on_err=arguments.skip,
    )


def run(args: Args) -> None:
    if shutil.which("ffmpeg") is None:
        raise ImportError("Could not find ffmpeg.")

    model = whisper_timestamped.load_model(args.model)

    for path in args.paths:
        print(f"Processing: {str(path.name)}")
        try:
            audio = whisper_timestamped.load_audio(str(path))
        except RuntimeError:
            if args.continue_on_err:
                print(f"Could not process {path}, as audio, skipping")
                continue
            raise

        result = whisper_timestamped.transcribe(model, audio, language=args.language)
        textgrid = whisper_to_textgrid(result)

        new_name = str(path.with_suffix(".TextGrid"))
        print(f"Saving: {new_name}")
        textgrid.save(new_name, format="long_textgrid", includeBlankSpaces=True)


def main(args: List[str]) -> None:
    run(parse_args(args))
