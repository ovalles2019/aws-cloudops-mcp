"""Run dashboard: python -m aws_cloudops_mcp.web"""

from __future__ import annotations

import os


def main() -> None:
    import uvicorn

    from aws_cloudops_mcp.web.starlette_app import app

    port = int(os.environ.get("PORT") or os.environ.get("AWS_CLOUDOPS_UI_PORT", "8846"))
    default_host = "0.0.0.0" if os.environ.get("PORT") else "127.0.0.1"
    host = os.environ.get("AWS_CLOUDOPS_UI_HOST", default_host)
    uvicorn.run(app, host=host, port=port, log_level="info")


if __name__ == "__main__":
    main()
