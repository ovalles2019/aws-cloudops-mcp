"""Whether the web UI runs as a public portfolio demo."""

from __future__ import annotations

import os


def is_demo_mode() -> bool:
    raw = os.environ.get("AWS_CLOUDOPS_DEMO", "")
    return raw.strip().lower() in ("1", "true", "yes", "on")
