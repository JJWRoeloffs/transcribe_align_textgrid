from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List


def load_json(data_file: Path) -> Dict:
    with data_file.open(encoding="utf-8") as d:
        return json.load(d)


def get_json_data(path: List[str]) -> List[Dict]:
    data_dir = Path(__file__).parent.resolve().joinpath(*path)
    data_files = [x for x in data_dir.iterdir() if x.is_file() and x.suffix == ".json"]
    return [load_json(x) for x in data_files]
