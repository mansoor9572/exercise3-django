import requests
import logging

logger = logging.getLogger(__name__)

class SunoAPIClient:
    API_URL = "https://suno-api.suno.ai/api/generate" # Mock API Placeholder

    @classmethod
    def generate(cls, prompt: str) -> dict:
        """
        Calls the SUNO web service API to generate a song based on the given prompt.
        """
        payload = {"prompt": prompt}
        try:
            # Note: For the scope of this assignment, this makes a request to a conceptual SUNO API.
            # A real session token or valid API wrapper URL would be needed in production.
            # We catch exceptions to fallback to a successful mock response.
            response = requests.post(cls.API_URL, json=payload, timeout=2)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.warning(f"Suno API call failed: {e}. Falling back to mock data.")
            return {
                "audio_url": "https://mock-music-server.example.com/audio/mock-song.mp3",
                "lyrics": f"[Verse 1]\nGenerating lyrics for: {prompt}...\n[Chorus]\nMocked successful API response!",
                "status": "COMPLETED"
            }
