"""arq background worker entrypoint.

No job functions yet — ingestion tasks are added at the ingestion milestone. This wires
up the worker process, Redis connection, and startup/shutdown lifecycle only.
"""

from typing import Any

from arq.connections import RedisSettings

from .config import get_settings
from .logging import configure_logging, get_logger


async def startup(ctx: dict[str, Any]) -> None:
    configure_logging()
    get_logger("worker").info("worker.startup")


async def shutdown(ctx: dict[str, Any]) -> None:
    get_logger("worker").info("worker.shutdown")


class WorkerSettings:
    functions: list[Any] = []
    redis_settings = RedisSettings.from_dsn(get_settings().redis_url)
    on_startup = startup
    on_shutdown = shutdown
