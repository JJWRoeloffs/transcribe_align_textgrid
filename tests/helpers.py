from __future__ import annotations

from praatio.data_classes.textgrid import Textgrid
from praatio.textgrid import openTextgrid

import json
from pathlib import Path
from typing import Dict


def load_json(data_file: Path) -> Dict:
    with data_file.open(encoding="utf-8") as d:
        return json.load(d)


def load_textgrid(data_file: Path) -> Textgrid:
    return openTextgrid(str(data_file), includeEmptyIntervals=False)


def get_json_data(*paths: str) -> Dict[str, Dict]:
    dir = Path(__file__).parent.resolve().joinpath(*paths)
    data_files = [x for x in dir.iterdir() if x.is_file() and x.suffix == ".json"]
    return {path.stem: load_json(path) for path in data_files}


def get_textgrid_data(*paths: str) -> Dict[str, Dict]:
    dir = Path(__file__).parent.resolve().joinpath(*paths)
    data_files = [x for x in dir.iterdir() if x.is_file() and x.suffix == ".TextGrid"]
    return {path.stem: load_textgrid(path) for path in data_files}
