import requests
import logging
from django.conf import settings
from .song_generator_strategy import SongGeneratorStrategy
from .generation_request import GenerationRequest
from .generation_result import GenerationResult

logger = logging.getLogger(__name__)


class SunoSongGeneratorStrategy(SongGeneratorStrategy):
    """
    Strategy B: Suno API Song Generator
    Integrates with https://api.sunoapi.org using Bearer token authentication.
    """
    BASE_URL = "https://api.sunoapi.org/api/v1"

    def _get_headers(self) -> dict:
        api_key = getattr(settings, "SUNO_API_KEY", "")
        if not api_key:
            logger.warning("[SunoStrategy] SUNO_API_KEY is not set.")
        return {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def generate(self, request: GenerationRequest) -> GenerationResult:
        payload = {
            "prompt": request.prompt,
            "callBackUrl": "https://dummy.com/callback",
            "model": "V4_5ALL",
            "customMode": False,
            "instrumental": False,
        }
        logger.info(f"[SunoStrategy] Sending generate request for prompt='{request.prompt}'")

        try:
            response = requests.post(
                f"{self.BASE_URL}/generate",
                json=payload,
                headers=self._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()

            # Suno API often returns HTTP 200 even for errors, returning code=401 in body
            if data.get("code") and data.get("code") != 200:
                logger.error(f"[SunoStrategy] API Error Data: {data}")
                return GenerationResult(task_id="", status="FAILED", raw_response=data)

            task_id = data.get("data", {}).get("taskId", "")
            if not task_id:
                logger.error(f"[SunoStrategy] No taskId returned: {data}")
                return GenerationResult(task_id="", status="FAILED", raw_response=data)

            return GenerationResult(
                task_id=task_id,
                status="PENDING",
                raw_response=data,
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"[SunoStrategy] API Call Failed: {e}")
            return GenerationResult(task_id="", status="FAILED", raw_response={"error": str(e)})

    def get_status(self, task_id: str) -> GenerationResult:
        logger.info(f"[SunoStrategy] Polling status for taskId={task_id}")
        try:
            response = requests.get(
                f"{self.BASE_URL}/generate/record-info",
                params={"taskId": task_id},
                headers=self._get_headers(),
                timeout=30,
            )
            response.raise_for_status()
            data = response.json()
            inner = data.get("data", {})

            # ── Extract clips from the actual Suno API response structure ──
            suno_response = inner.get("response") or {}
            suno_data = suno_response.get("sunoData") or []

            audio_url = None
            lyrics = None
            resolved_status = "PENDING"

            if suno_data and isinstance(suno_data, list) and len(suno_data) > 0:
                first_clip = suno_data[0]

                audio_url = first_clip.get("audioUrl") or ""
                if not audio_url:
                    audio_url = first_clip.get("streamAudioUrl") or ""

                lyrics = first_clip.get("prompt") or ""

                if audio_url:
                    resolved_status = "SUCCESS"
                    logger.info(f"[SunoStrategy] Song ready! audio_url={audio_url[:80]}...")
                else:
                    resolved_status = "PENDING"
            else:
                # Also try legacy format: data.clips
                clips = inner.get("clips") or []
                if clips:
                    first_clip = clips[0] if isinstance(clips, list) else next(iter(clips.values()), {})
                    audio_url = first_clip.get("audio_url") or first_clip.get("streamAudioUrl") or ""
                    meta = first_clip.get("metadata") or {}
                    lyrics = meta.get("prompt") or first_clip.get("lyric") or ""
                    if audio_url:
                        resolved_status = "SUCCESS"

            logger.info(f"[SunoStrategy] Poll result: status={resolved_status}, has_audio={'yes' if audio_url else 'no'}")

            return GenerationResult(
                task_id=task_id,
                status=resolved_status,
                audio_url=audio_url if audio_url else None,
                lyrics=lyrics if lyrics else None,
                raw_response=data,
            )
        except requests.exceptions.RequestException as e:
            logger.error(f"[SunoStrategy] Status Poll Failed: {e}")
            return GenerationResult(task_id=task_id, status="FAILED", raw_response={"error": str(e)})
