import base64
from typing import Tuple

def to_base64_png(png_bytes: bytes) -> str:
    return base64.b64encode(png_bytes).decode("utf-8")

def chart_payload(result: dict) -> Tuple[str, dict]:
    """
    Returns chart_type and payload dict compatible with storage and API.
    """
    if result["type"] == "png":
        b64 = to_base64_png(result["bytes"])
        return "png", {"chart_type": "png", "payload_base64": b64}
    elif result["type"] == "html":
        return "html", {"chart_type": "html", "payload_html": result["html"]}
    else:
        raise ValueError("Unknown chart result type")
