import logging
from django.conf import settings
from .base import SongGeneratorStrategy

STRATEGY_MOCK = "mock"
STRATEGY_SUNO = "suno"

logger = logging.getLogger(__name__)

def get_generator_strategy() -> SongGeneratorStrategy:
    strategy_name = getattr(settings, "GENERATOR_STRATEGY", STRATEGY_MOCK).lower().strip()

    if strategy_name == STRATEGY_SUNO:
        from .suno_strategy import SunoSongGeneratorStrategy
        logger.info("[StrategyFactory] Using SunoSongGeneratorStrategy")
        return SunoSongGeneratorStrategy()

    if strategy_name != STRATEGY_MOCK:
        logger.warning(
            f"[StrategyFactory] Unknown GENERATOR_STRATEGY='{strategy_name}'. "
            f"Falling back to MockSongGeneratorStrategy."
        )

    from .mock_strategy import MockSongGeneratorStrategy
    logger.info("[StrategyFactory] Using MockSongGeneratorStrategy")
    return MockSongGeneratorStrategy()
