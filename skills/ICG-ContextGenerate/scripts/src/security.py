"""Security helpers for ImageContext-Generator (S2-SecurityFix).

Pure functions — no I/O, no external deps.
Used by: cli.py, vision_engine.py, director.py, knowledge_manager.py
"""
from __future__ import annotations

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Path containment & validation (SEC-02, SEC-03, SEC-04, SEC-07)
# ---------------------------------------------------------------------------

_COURSE_RE = re.compile(r"^[a-z0-9-]+$", re.IGNORECASE)
_SEGMENT_RE = re.compile(r"^[A-Za-z0-9_-]+$")


class PathValidationError(ValueError):
    """Raised when a user-supplied path escapes its allowed root or has an unsafe name."""


def validate_course_id(course_id: str) -> str:
    """Validate course identifier per allowlist ^[a-z0-9-]+$ (case-insensitive)."""
    if not course_id or not _COURSE_RE.fullmatch(course_id):
        raise PathValidationError(f"Invalid course id: {course_id!r} (allowed: ^[a-z0-9-]+$)")
    return course_id.lower()


def validate_segment(value: str, label: str = "name") -> str:
    """Validate a path segment (pertemuan, folder name) per ^[A-Za-z0-9_-]+$."""
    if not value or not _SEGMENT_RE.fullmatch(value):
        raise PathValidationError(f"Invalid {label}: {value!r} (allowed: ^[A-Za-z0-9_-]+$)")
    return value


def resolve_under_root(
    root: str | Path,
    candidate: str | Path,
    *,
    must_exist: bool = False,
    suffix: str | None = None,
) -> Path:
    """
    Resolve `candidate` and ensure it lives inside `root`.

    Args:
        root: Containment root (workspace, project, knowledge dir, etc.).
        candidate: User-supplied path (relative or absolute).
        must_exist: If True, raise FileNotFoundError when the path does not exist.
        suffix: If set, require the resolved path to end with this suffix (e.g. ".txt").

    Returns:
        Absolute, symlink-resolved Path within root.

    Raises:
        PathValidationError: If candidate escapes root or suffix mismatch.
        FileNotFoundError: If must_exist and path missing.
    """
    root_path = Path(root).resolve()
    candidate_path = Path(candidate)
    resolved = candidate_path.resolve()

    # Reject absolute symlinks that escape root (resolve() follows symlinks)
    try:
        resolved.relative_to(root_path)
    except ValueError:
        raise PathValidationError(
            f"Path escapes containment root: {candidate!r} (root: {root_path})"
        )

    if suffix and resolved.suffix.lower() != suffix.lower():
        raise PathValidationError(
            f"Output must end with {suffix!r}, got {resolved.suffix!r}"
        )

    if must_exist and not resolved.exists():
        raise FileNotFoundError(f"Path not found: {resolved}")

    return resolved


# ---------------------------------------------------------------------------
# Redaction / sanitisation (SEC-01, SEC-09, SEC-10)
# ---------------------------------------------------------------------------

# key=value patterns (api_key, token, secret, password, bearer)
_KEYVAL_RE = re.compile(
    r"""(?xi)
    \b(
        api[_-]?key |
        token |
        secret |
        password |
        bearer
    )
    \s*[:=]\s*
    \S+
    """
)

# JWT: eyJ... (base64url segments separated by dots)
_JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b")

# URL with userinfo: scheme://user:pass@host...
_URL_USERINFO_RE = re.compile(r"\b([a-z][a-z0-9+.-]*://)[^/@\s]+@([^\s/]+)", re.IGNORECASE)

# Bearer token header
_BEARER_RE = re.compile(r"\bBearer\s+\S+", re.IGNORECASE)

# UPPER_SNAKE secret-like literals: FAKE-SECRET-XYZ, MY_SECRET_KEY, etc.
# At least 5 chars, contains SECRET|KEY|TOKEN|PASS|PASSWORD|API (case-insensitive).
# IGNORECASE is scoped to the keyword alternation ONLY — the token must be
# uppercase so common words like "monkey", "passport", "apikey" are not
# redacted (review round 1, MINOR #4).
_SECRET_LITERAL_RE = re.compile(
    r"\b(?=[A-Z0-9_-]{5,}\b)"
    r"(?=[A-Z0-9_-]*(?i:SECRET|KEY|TOKEN|PASSWORD|PASS|API)[A-Z0-9_-]*)"
    r"[A-Z0-9_-]+"
    r"\b"
)


def redact(text: str) -> str:
    """
    Strip sensitive patterns from arbitrary text (commit subjects, error messages, etc.).

    Order matters: Bearer → JWT → URL userinfo → key=value → secret literals.
    """
    if not text:
        return ""
    out = text
    out = _BEARER_RE.sub("Bearer [REDACTED]", out)
    out = _JWT_RE.sub("[REDACTED_JWT]", out)
    out = _URL_USERINFO_RE.sub(r"\1[REDACTED]@\2", out)
    out = _KEYVAL_RE.sub(r"\1=[REDACTED]", out)
    out = _SECRET_LITERAL_RE.sub("[REDACTED]", out)
    return out


# LaTeX special chars that must be escaped when emitting .tex
_LATEX_ESCAPE = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "&": r"\&",
    "#": r"\#",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
    "%": r"\%",
}

_LATEX_CMD_RE = re.compile(r"\\[A-Za-z]+\s*\{")


def escape_latex(text: str) -> str:
    """Escape LaTeX special characters in free text (for downstream consumer)."""
    return "".join(_LATEX_ESCAPE.get(ch, ch) for ch in text)


def sanitize_ai_line(text: str, max_len: int = 500) -> str | None:
    """
    Validate a single LLM output line before writing to inisiasi.txt.

    Rules:
    - Non-empty, <= max_len characters.
    - Contains 'Konteks:' and 'Arah:' markers (expected format).
    - No LaTeX commands (e.g. \textbf{...}).
    - No control characters except tab.
    """
    line = text.strip()
    if not line or len(line) > max_len:
        return None
    if "Konteks:" not in line or "Arah:" not in line:
        return None
    if _LATEX_CMD_RE.search(line):
        return None
    if any(ord(c) < 32 and c != "\t" for c in line):
        return None
    return line