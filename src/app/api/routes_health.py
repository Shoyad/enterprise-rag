"""Liveness/readiness endpoint: reports DB and Redis connectivity."""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ..config import get_settings
from ..logging import get_logger
from ..persistence.db import check_db
from ..redis_client import check_redis

router = APIRouter(tags=["health"])
log = get_logger("health")


async def _probe(name: str, check) -> str:
    try:
        await check()
        return "ok"
    except Exception as exc:  # noqa: BLE001 - report any dependency failure as degraded
        log.warning("health.dependency_unavailable", dependency=name, error=str(exc))
        return "error"


@router.get("/health")
async def health() -> JSONResponse:
    dependencies = {
        "database": await _probe("database", check_db),
        "redis": await _probe("redis", check_redis),
    }
    healthy = all(state == "ok" for state in dependencies.values())
    body = {
        "status": "ok" if healthy else "degraded",
        "version": get_settings().app_version,
        "dependencies": dependencies,
    }
    return JSONResponse(body, status_code=200 if healthy else 503)
