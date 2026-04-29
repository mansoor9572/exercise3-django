from abc import ABC, abstractmethod
from .generation_request import GenerationRequest
from .generation_result import GenerationResult


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
