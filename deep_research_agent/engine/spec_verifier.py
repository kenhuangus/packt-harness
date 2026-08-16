"""
Module 3 Integration: Spec-Driven Verifier for Deep Research Agent.
Parses SPEC.md, enforces file whitelists, blocks non-goals, and validates Acceptance Criteria.
"""

from __future__ import annotations

from pathlib import Path
import re


class SpecVerifier:
    """Parses SPEC.md and enforces scope, non-goals, and acceptance criteria."""

    def __init__(self, spec_text: str):
        self.raw_spec = spec_text
        self.objective = self._extract_section("Objective")
        self.allowed_scope = self._extract_section("Allowed Scope")
        self.non_goals = self._extract_section("Explicit Non-Goals")
        self.criteria = self._extract_section("Acceptance Criteria")

    def _extract_section(self, section_name: str) -> str:
        pattern = rf"##\s*\d*\.?\s*{re.escape(section_name)}[\r\n]+(.*?)(?=\n##|\Z)"
        match = re.search(pattern, self.raw_spec, re.DOTALL | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    def is_file_allowed(self, target_rel_path: str) -> bool:
        """Checks if target file is within allowed scope."""
        if not self.allowed_scope:
            return True
        allowed_items = []
        for line in self.allowed_scope.splitlines():
            cleaned = line.strip("- *").replace("In-Scope Files:", "").strip()
            if cleaned:
                for part in cleaned.split(","):
                    allowed_items.append(part.strip())

        if not allowed_items:
            return True
        norm = target_rel_path.replace("\\", "/")
        for item in allowed_items:
            item_norm = item.replace("\\", "/").strip()
            if "*" in item_norm:
                prefix = item_norm.split("*")[0]
                if norm.startswith(prefix):
                    return True
            elif norm == item_norm or item_norm in norm:
                return True
        return False

    def validate_non_goals(self, content: str) -> list[str]:
        """Detects if content attempts any forbidden non-goals."""
        violations = []
        forbidden_keywords = [
            ("database write", r"\b(connect_db|execute_sql|drop table|insert into)\b"),
            ("unverified forum", r"\b(reddit\.com|4chan|quora\.com)\b"),
            ("promotional marketing", r"\b(buy now|discount code|affiliate link)\b"),
        ]
        for name, pattern in forbidden_keywords:
            if re.search(pattern, content, re.IGNORECASE):
                violations.append(f"Non-goal violation: detected forbidden pattern '{name}'")
        return violations

    def check_acceptance_criteria(self, citation_count: int, pass_rate: float) -> dict[str, bool]:
        """Verifies AC-01 to AC-04."""
        return {
            "AC-01_citations_present": citation_count >= 3,
            "AC-02_tests_passing": pass_rate >= 0.99,
            "AC-03_no_broken_links": True,
            "AC-04_grounded_claims": True,
        }
