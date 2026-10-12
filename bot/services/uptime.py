from dataclasses import dataclass, field
from datetime import datetime, timezone

from bot.config import settings


@dataclass(slots=True)
class BotUptime:
    started_at: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )

    @property
    def uptime_seconds(self) -> int:
        delta = datetime.now(timezone.utc) - self.started_at
        return int(delta.total_seconds())

    @property
    def formatted_uptime(self) -> str:
        seconds = self.uptime_seconds
        days, seconds = divmod(seconds, 86400)
        hours, seconds = divmod(seconds, 3600)
        minutes, seconds = divmod(seconds, 60)

        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        parts.append(f"{minutes}m")
        parts.append(f"{seconds}s")
        return " ".join(parts)
