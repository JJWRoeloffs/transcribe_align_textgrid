"""
A small wrapper package around whisper-timestamped.
Create force-aligned transcription TextGrids from raw audio!

Copyright (c) 2025 JJW Roeloffs

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not see LICENSE for more details.
"""

__title__ = "transcribe_align_textgrid"
__author__ = "JJWRoeloffs"
__license__ = "AGPL-3.0"
__version__ = "0.2.3"


from transcribe_align_textgrid.adapter import (
    whisper_to_textgrid as whisper_to_textgrid,
)
