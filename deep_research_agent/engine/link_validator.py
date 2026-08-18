"""
Link Validator & Live HTTP Liveness Verification Engine for Deep Research Agent.
Verifies that all discovered evidence URLs return HTTP 200 before being accepted
into the verified citation corpus and publication dossier.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
from typing import Any
import urllib.error
import urllib.parse
import urllib.request

logger = logging.getLogger(__name__)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)


def check_url_status(url: str, timeout: float = 4.5) -> int:
    """
    Performs a live HTTP check on the provided URL.
    Returns HTTP status code (e.g. 200), or 0 on network/connection failure.
    """
    if not url or not isinstance(url, str):
        return 0

    url = url.strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        return 0

    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.9",
        },
    )

    # First attempt lightweight GET with streaming read to capture status
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
            return status
    except urllib.error.HTTPError as err:
        # Some servers (like Wikipedia / YouTube) might return 403 on certain headers,
        # but if code is 200..399 it's considered valid
        if 200 <= err.code < 400:
            return err.code
        return err.code
    except Exception:
        return 0


def is_url_valid_and_live(url: str, timeout: float = 4.5) -> bool:
    """
    Returns True ONLY if the URL is accessible and returns HTTP 200 (or 2xx/3xx redirect).
    If the link returns 404, 500, or fails connection, returns False.
    """
    status = check_url_status(url, timeout=timeout)
    return 200 <= status < 400


def validate_and_filter_evidence_links(
    evidence_list: list[dict[str, Any]],
    timeout: float = 4.5,
    max_workers: int = 8,
) -> list[dict[str, Any]]:
    """
    Concurrently verifies all URLs in the candidate evidence list.
    Attaches `url_status: 200` to valid documents.
    Drops any document whose URL does not return a successful 200/2xx status code.
    """
    if not evidence_list:
        return []

    valid_documents: list[dict[str, Any]] = []

    def _verify_item(item: dict[str, Any]) -> tuple[dict[str, Any], int]:
        url = item.get("url", "")
        status = check_url_status(url, timeout=timeout)
        return item, status

    with ThreadPoolExecutor(max_workers=min(max_workers, max(1, len(evidence_list)))) as executor:
        futures = [executor.submit(_verify_item, doc) for doc in evidence_list]
        for future in as_completed(futures):
            try:
                doc, status = future.result()
                if 200 <= status < 400:
                    doc["url_status"] = status
                    doc["link_verified"] = True
                    valid_documents.append(doc)
                else:
                    logger.warning(
                        "[LINK_VALIDATOR_REJECTED] Document '%s' rejected due to non-200 HTTP code: %d (URL: %s)",
                        doc.get("title", "Untitled"),
                        status,
                        doc.get("url", ""),
                    )
            except Exception as exc:
                logger.warning("[LINK_VALIDATOR_ERROR] Failed checking document: %s", exc)

    return valid_documents
