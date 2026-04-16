from abc import ABC, abstractmethod
from dataclasses import dataclass, field
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


class SongGeneratorStrategy(ABC):
    """
    Strategy Interface for song generation.

    All concrete strategies must implement:
      - generate(request)  → start generation, return a GenerationResult
      - get_status(task_id) → poll for the latest status of a task
    """

    @abstractmethod
    def generate(self, request: GenerationRequest) -> GenerationResult:
        """
        Initiate song generation.

        Args:
            request: GenerationRequest with prompt/title/style fields.

        Returns:
            GenerationResult containing at minimum a task_id and initial status.
        """
        ...

    @abstractmethod
    def get_status(self, task_id: str) -> GenerationResult:
        """
        Check the status of an in-progress generation task.

        Args:
            task_id: The identifier returned by generate().

        Returns:
            GenerationResult with the current status and any available output.
        """
        ...
