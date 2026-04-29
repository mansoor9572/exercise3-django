from dataclasses import dataclass
from typing import Optional


@dataclass
class GenerationRequest:
    """
    Data object passed to a SongGeneratorStrategy.
    Contains all inputs needed to generate a song.
    """
    prompt: str
    title: Optional[str] = None
    style: Optional[str] = None
