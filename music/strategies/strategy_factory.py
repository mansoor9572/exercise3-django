import logging
from django.conf import settings
from .song_generator_strategy import SongGeneratorStrategy

logger = logging.getLogger(__name__)


class StrategyFactory:
    """
    Factory class that creates the appropriate SongGeneratorStrategy
    based on the GENERATOR_STRATEGY setting.
    """

    STRATEGY_MOCK = "mock"
    STRATEGY_SUNO = "suno"

    @staticmethod
    def get_generator_strategy() -> SongGeneratorStrategy:
        strategy_name = getattr(settings, "GENERATOR_STRATEGY", "mock").lower().strip()

        if strategy_name == StrategyFactory.STRATEGY_SUNO:
            from .suno_song_generator_strategy import SunoSongGeneratorStrategy
            logger.info("[StrategyFactory] Using SunoSongGeneratorStrategy")
            return SunoSongGeneratorStrategy()

        if strategy_name != StrategyFactory.STRATEGY_MOCK:
            logger.warning(
                f"[StrategyFactory] Unknown GENERATOR_STRATEGY='{strategy_name}'. "
                f"Falling back to MockSongGeneratorStrategy."
            )

        from .mock_song_generator_strategy import MockSongGeneratorStrategy
        logger.info("[StrategyFactory] Using MockSongGeneratorStrategy")
        return MockSongGeneratorStrategy()
