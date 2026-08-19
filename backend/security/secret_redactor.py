"""Secret Redaction Engine for AuditVector."""

import re
from typing import Dict, Tuple, List


class SecretRedactor:
    """Detects and redacts credentials, private keys, and sensitive tokens from source files and configs."""

    SECRET_PATTERNS: List[Tuple[str, re.Pattern]] = [
        ("GENERIC_SECRET", re.compile(r'(?i)(api[_-]?key|secret|token|password|auth[_-]?token|access[_-]?key)\s*[:=]\s*["\']([^"\']{6,})["\']')),
        ("BEARER_TOKEN", re.compile(r'(?i)bearer\s+([a-zA-Z0-9_\-\.]{15,})')),
        ("PRIVATE_KEY", re.compile(r'-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----')),
        ("GOOGLE_API_KEY", re.compile(r'AIza[0-9A-Za-z-_]{35}')),
        ("AWS_KEY", re.compile(r'(?i)AKIA[0-9A-Z]{16}')),
        ("BINANCE_KEY", re.compile(r'(?i)(binance[_-]?(?:api[_-]?)?key|binance[_-]?secret)\s*[:=]\s*["\']([a-zA-Z0-9]{32,64})["\']')),
    ]

    @classmethod
    def sanitize(cls, text: str) -> Tuple[str, int]:
        """Replaces detected secrets with [REDACTED] placeholders and returns count of redactions."""
        sanitized = text
        redaction_count = 0

        # Redact private key blocks first
        for name, pattern in cls.SECRET_PATTERNS:
            if name == "PRIVATE_KEY":
                matches = pattern.findall(sanitized)
                if matches:
                    redaction_count += len(matches)
                    sanitized = pattern.sub("[REDACTED_PRIVATE_KEY]", sanitized)

        # Redact regex patterns with capture groups
        for name, pattern in cls.SECRET_PATTERNS:
            if name == "PRIVATE_KEY":
                continue
            
            def replacer(match):
                nonlocal redaction_count
                redaction_count += 1
                if match.lastindex and match.lastindex >= 2:
                    # Key-value match
                    full = match.group(0)
                    val = match.group(2)
                    return full.replace(val, "[REDACTED]")
                elif match.lastindex and match.lastindex == 1:
                    full = match.group(0)
                    val = match.group(1)
                    return full.replace(val, "[REDACTED]")
                else:
                    return "[REDACTED]"

            sanitized = pattern.sub(replacer, sanitized)

        return sanitized, redaction_count
