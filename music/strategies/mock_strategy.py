import uuid
import logging
from .base import SongGeneratorStrategy, GenerationRequest, GenerationResult

logger = logging.getLogger(__name__)

class MockSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Strategy A: Mock Song Generator
    Produces deterministic output for offline dev/testing.
    """

    MOCK_AUDIO_URL = "https://mock-music-server.example.com/audio/mock-song.mp3"

    def generate(self, request: GenerationRequest) -> GenerationResult:
        task_id = f"mock-{uuid.uuid4().hex[:12]}"

        lyrics = (
            f"[Verse 1]\n"
            f"This is a mock song about: {request.prompt}\n"
            f"Generated offline, no API key needed\n\n"
            f"[Chorus]\n"
            f"Mock mode is fast, mock mode is free!\n"
        )

        logger.info(f"[MockStrategy] Generated task_id={task_id} for prompt='{request.prompt}'")

        return GenerationResult(
            task_id=task_id,
            status="SUCCESS",
            audio_url=self.MOCK_AUDIO_URL,
            lyrics=lyrics,
            raw_response={"source": "mock", "task_id": task_id, "prompt": request.prompt},
        )

    def get_status(self, task_id: str) -> GenerationResult:
        logger.info(f"[MockStrategy] get_status called for task_id={task_id}")
        return GenerationResult(
            task_id=task_id,
            status="SUCCESS",
            audio_url=self.MOCK_AUDIO_URL,
            lyrics="[Mock] Task Complete.",
            raw_response={"source": "mock", "task_id": task_id},
        )
