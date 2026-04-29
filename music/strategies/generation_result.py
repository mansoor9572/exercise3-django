from dataclasses import dataclass, field
from typing import Optional


@dataclass
class GenerationResult:
    """
    Data object returned by a SongGeneratorStrategy.
    Contains the outcome of a generation call (or task reference).
    """
    task_id: str
    status: str                          # e.g. PENDING, SUCCESS, FAILED
    audio_url: Optional[str] = None
    lyrics: Optional[str] = None
    raw_response: dict = field(default_factory=dict)
