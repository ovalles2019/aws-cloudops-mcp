"""Starlette app: static UI + JSON API (fixture-backed in demo mode)."""

from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import FileResponse, JSONResponse
from starlette.routing import Mount, Route
from starlette.staticfiles import StaticFiles

from aws_cloudops_mcp.demo_fixtures import dashboard_payload
from aws_cloudops_mcp.web.demo_mode import is_demo_mode

STATIC = Path(__file__).resolve().parent / "static"


@asynccontextmanager
async def lifespan(_: Starlette):
    yield


async def index(_: Request) -> FileResponse:
    return FileResponse(STATIC / "index.html")


async def api_health(_: Request) -> JSONResponse:
    return JSONResponse({"ok": True, "demo": is_demo_mode()})


async def api_dashboard(_: Request) -> JSONResponse:
    if not is_demo_mode():
        return JSONResponse(
            {
                "ok": False,
                "error": "Dashboard requires AWS_CLOUDOPS_DEMO=1 (synthetic data only on public host).",
            },
            status_code=503,
        )
    payload = dashboard_payload()
    payload["demo_mode"] = True
    return JSONResponse(payload)


routes = [
    Route("/", index),
    Route("/health", api_health, methods=["GET"]),
    Route("/api/dashboard", api_dashboard, methods=["GET"]),
    Mount("/static", StaticFiles(directory=str(STATIC)), name="static"),
]

app = Starlette(debug=False, routes=routes, lifespan=lifespan)
