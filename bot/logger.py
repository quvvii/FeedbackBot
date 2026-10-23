import logging
import sys
from pathlib import Path

LOG_DIR = Path("logs")


def setup_logging(level: str = "INFO") -> None:
    handlers: list[logging.Handler] = [logging.StreamHandler(sys.stdout)]

    if LOG_DIR.is_dir():
        handlers.append(logging.FileHandler(LOG_DIR / "bot.log", encoding="utf-8"))

    logging.basicConfig(
        level=getattr(logging, level.upper(), logging.INFO),
        format="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        handlers=handlers,
    )
    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
