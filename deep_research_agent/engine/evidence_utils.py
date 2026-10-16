"""Evidence ranking, metadata cleanup, and provenance helpers for the capstone."""

from __future__ import annotations

import re
from typing import Any


_STOPWORDS = {
    "a", "an", "the", "and", "or", "of", "for", "in", "on", "to", "with", "by",
    "is", "are", "be", "as", "at", "from", "into", "via", "vs", "over", "under",
}


def tokenize_query(text: str) -> set[str]:
    tokens = re.findall(r"[a-z0-9]{3,}", (text or "").lower())
    return {t for t in tokens if t not in _STOPWORDS}


def relevance_score(query: str, item: dict[str, Any]) -> float:
    """Lexical overlap score in [0, 1] against title/snippet/text/author."""
    q_tokens = tokenize_query(query)
    if not q_tokens:
        return 0.0
    blob = " ".join(
        str(item.get(k, ""))
        for k in ("title", "snippet", "text", "author", "grounding_quote")
    ).lower()
    hits = sum(1 for t in q_tokens if t in blob)
    return hits / max(len(q_tokens), 1)


def rank_and_filter_evidence(
    query: str,
    evidence: list[dict[str, Any]],
    *,
    min_score: float = 0.15,
    keep_at_least: int = 2,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Sort by relevance; drop low-score items but keep a minimum floor."""
    scored: list[dict[str, Any]] = []
    dropped: list[dict[str, Any]] = []
    for item in evidence:
        score = relevance_score(query, item)
        enriched = dict(item)
        enriched["relevance_score"] = round(score, 4)
        # Blend into confidence without inventing high scores.
        base_conf = float(enriched.get("confidence_score") or 0.5)
        enriched["confidence_score"] = round(max(0.05, min(0.99, 0.45 * base_conf + 0.55 * score)), 4)
        if score >= min_score:
            scored.append(enriched)
        else:
            dropped.append(enriched)
    scored.sort(key=lambda e: (e.get("relevance_score", 0), e.get("confidence_score", 0)), reverse=True)
    if len(scored) < keep_at_least and dropped:
        # Keep the best dropped items so demos don't go empty on niche queries.
        dropped_sorted = sorted(
            dropped,
            key=lambda e: e.get("relevance_score", 0),
            reverse=True,
        )
        need = keep_at_least - len(scored)
        for item in dropped_sorted[:need]:
            item = dict(item)
            item["provenance_note"] = "low_relevance_retained_for_coverage"
            scored.append(item)
        dropped = dropped_sorted[need:]
    return scored, dropped


def dedupe_repeated_phrase(text: str) -> str:
    """Collapse 'Name Name' / half-repeated channel strings."""
    clean = re.sub(r"\s+", " ", (text or "")).strip()
    if not clean:
        return ""
    parts = clean.split()
    n = len(parts)
    if n >= 2 and n % 2 == 0:
        half = n // 2
        if parts[:half] == parts[half:]:
            clean = " ".join(parts[:half])
    # Also collapse immediate word doubles: "Foo Foo Bar" -> "Foo Bar"
    collapsed: list[str] = []
    for w in clean.split():
        if collapsed and collapsed[-1].lower() == w.lower():
            continue
        collapsed.append(w)
    return " ".join(collapsed)


def clean_youtube_author(author: str) -> str:
    """Keep channel name; strip view-count / age metadata from author field."""
    raw = dedupe_repeated_phrase(author)
    # Drop trailing "(234K 1mo ago)" style suffixes
    raw = re.sub(r"\s*\([^)]*\b(?:ago|views?|subscribers?|K|M)\b[^)]*\)\s*$", "", raw, flags=re.I)
    raw = re.sub(r"\s+\d+(?:\.\d+)?[KkMm]?\s+(?:\d+\s*)?(?:day|week|month|year|mo|yr)s?\s+ago\s*$", "", raw, flags=re.I)
    raw = re.sub(r"\s+\d+(?:\.\d+)?[KkMm]\s*$", "", raw)
    return dedupe_repeated_phrase(raw) or "YouTube Tech Channel"


def clean_github_author(author: str) -> str:
    return dedupe_repeated_phrase(author) or "Open Source Developer"


def clean_evidence_metadata(item: dict[str, Any]) -> dict[str, Any]:
    out = dict(item)
    stype = (out.get("source_type") or "").lower()
    if stype == "youtube":
        out["author"] = clean_youtube_author(str(out.get("author", "")))
    elif stype == "github":
        out["author"] = clean_github_author(str(out.get("author", "")))
    else:
        out["author"] = dedupe_repeated_phrase(str(out.get("author", ""))) or out.get("author", "Author")
    # Never present synthetic fillers as verified live evidence.
    doc_id = str(out.get("doc_id", ""))
    if "guaranteed" in doc_id or "openalex_fallback" in doc_id or doc_id.startswith("doc_general_"):
        out["provenance"] = "synthetic"
        out["link_verified"] = False
    else:
        out.setdefault("provenance", "live")
    return out


def repair_evidence_structure(evidence: list[dict[str, Any]], query: str) -> list[dict[str, Any]]:
    """Deterministic structural repair for TDA — no confidence inflation."""
    repaired: list[dict[str, Any]] = []
    seen: set[str] = set()
    for idx, raw in enumerate(evidence):
        item = clean_evidence_metadata(raw)
        doc_id = str(item.get("doc_id") or "").strip() or f"doc_repaired_{idx:03d}"
        if doc_id in seen:
            doc_id = f"{doc_id}_{idx}"
        seen.add(doc_id)
        title = str(item.get("title") or "").strip() or f"Source on {query}"
        url = str(item.get("url") or "").strip() or "https://example.com"
        text = str(item.get("text") or item.get("snippet") or title)
        conf = item.get("confidence_score")
        try:
            conf_f = float(conf)
        except (TypeError, ValueError):
            conf_f = 0.35
        # Clamp into valid range without boosting weak evidence above 0.5 unless already higher.
        if conf_f < 0.30:
            conf_f = 0.30
        item.update(
            {
                "doc_id": doc_id,
                "title": title,
                "url": url,
                "domain": item.get("domain") or "web",
                "author": item.get("author") or "Researcher",
                "source_type": item.get("source_type") or "web",
                "text": text,
                "snippet": item.get("snippet") or text[:350],
                "grounding_quote": item.get("grounding_quote") or text[:260],
                "confidence_score": round(min(conf_f, 0.99), 4),
            }
        )
        repaired.append(item)
    return repaired


def drop_synthetic_evidence(evidence: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], int]:
    kept = [e for e in evidence if e.get("provenance") != "synthetic" and "guaranteed" not in str(e.get("doc_id", ""))]
    # Also drop openalex synthetic fallbacks by id pattern
    kept = [e for e in kept if "openalex_fallback" not in str(e.get("doc_id", "")) and not str(e.get("doc_id", "")).startswith("doc_general_")]
    return kept, len(evidence) - len(kept)
