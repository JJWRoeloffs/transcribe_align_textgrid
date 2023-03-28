"""
A small wrapper package around whisper-timestamped.
Create force-alligned transcription TextGrids from raw audio!

:license: MIT, see LICENSE for more details.
"""

__title__ = "transcribe_allign_textgrid"
__author__ = "JJWRoeloffs"
__license__ = "MIT"
__version__ = "0.1.2"


from transcribe_allign_textgrid.adapter import (
    whisper_to_textgrid as whisper_to_textgrid,
)
