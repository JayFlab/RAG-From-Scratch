"""Load DashScope credentials from the process environment."""

import os


def require_dashscope_api_key() -> str:
    key = os.environ.get("DASHSCOPE_API_KEY", "").strip()
    if not key:
        raise RuntimeError("Set the DASHSCOPE_API_KEY environment variable before running this demo.")
    return key
