from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass
class SafetyResult:
    allowed: bool
    risk_level: str
    reason: str
    sanitized_text: str


class ContentSafetyService:
    def __init__(self, blocked_terms: Iterable[str] | None = None):
        self.blocked_terms = [term.lower() for term in (blocked_terms or [
            "<script",
            "ignore previous instructions",
            "api_key",
            "password",
        ])]

    def check_input(self, text: str) -> SafetyResult:
        return self._check(text)

    def check_output(self, text: str) -> SafetyResult:
        return self._check(text, redact=True)

    def _check(self, text: str, redact: bool = False) -> SafetyResult:
        normalized = (text or "").lower()
        for term in self.blocked_terms:
            if term and term in normalized:
                return SafetyResult(
                    allowed=False,
                    risk_level="high",
                    reason=f"blocked term detected: {term}",
                    sanitized_text="[blocked]" if redact else "",
                )
        return SafetyResult(
            allowed=True,
            risk_level="low",
            reason="allowed",
            sanitized_text=text or "",
        )
