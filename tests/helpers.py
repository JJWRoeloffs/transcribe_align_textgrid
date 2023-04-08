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
    data_files = Path(__file__).parent.resolve().joinpath(*paths).glob("*.json")
    return {path.stem: load_json(path) for path in data_files}


def get_textgrid_data(*paths: str) -> Dict[str, Textgrid]:
    data_files = Path(__file__).parent.resolve().joinpath(*paths).glob("*.TextGrid")
    return {path.stem: load_textgrid(path) for path in data_files}
