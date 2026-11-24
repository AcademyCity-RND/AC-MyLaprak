"""Knowledge manager — course config (YAML) & PDF reference extraction.

S2-SecurityFix:
- SEC-04: `yaml.safe_load` retained (no unsafe loaders).
- SEC-07: `course_id` validated via allowlist; config resolved through
  `knowledge_dir` (repo root), reference_dir through `reference_root`
  (workspace root). They are now *separate* roots so that configs at
  `knowledge/courses/` (repo root) are not rejected when workspace is
  a subdirectory (review round 1, MAJOR #1).
- SEC-09: PyMuPDF errors caught specifically, messages redacted.
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict

import fitz
import yaml

from src.security import (
    PathValidationError,
    resolve_under_root,
    validate_course_id,
    redact,
)


class KnowledgeManager:
    """Load course knowledge from YAML and reference PDFs safely."""

    def __init__(
        self,
        knowledge_dir: str = "knowledge/courses",
        allowed_root: str | Path | None = None,
        reference_root: str | Path | None = None,
    ):
        """
        `knowledge_dir` is the containment root for course YAML configs (it
        lives at repo root). `allowed_root`/`reference_root` is a *separate*
        root used only for PDF reference directories (which live in the user
        workspace). Keeping them distinct is what prevents SEC-07 from
        breaking `generate`/`generate-director` (review round 1, MAJOR #1).
        """
        self.knowledge_dir = Path(knowledge_dir).resolve()
        ref = reference_root if reference_root is not None else allowed_root
        self.reference_root = Path(ref).resolve() if ref else None
        # Kept as a backwards-compatible alias for callers/tests that used it.
        self.allowed_root = self.reference_root
        self.course_cache: dict[str, Dict] = {}

    def _resolve_config_path(self, course_id: str) -> Path:
        """Validate course id and ensure its config stays inside knowledge_dir."""
        cid = validate_course_id(course_id)
        candidate = self.knowledge_dir / f"{cid}.yaml"
        try:
            return resolve_under_root(self.knowledge_dir, candidate, must_exist=False)
        except PathValidationError as exc:
            raise ValueError(redact(str(exc))) from exc

    def load_course_config(self, course_id: str) -> Dict:
        """Load YAML config for a course (safe_load only)."""
        config_path = self._resolve_config_path(course_id)
        if not config_path.exists():
            raise FileNotFoundError(f"Course config not found: {config_path}")
        with open(config_path, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        return data if isinstance(data, dict) else {}

    def extract_pdf_knowledge(self, pdf_path: str) -> Dict:
        """Extract structured knowledge from PDF reference."""
        knowledge: Dict = {"slides": [], "key_terms": [], "topics": []}
        try:
            doc = fitz.open(pdf_path)
        except (RuntimeError, OSError, ValueError) as exc:
            raise ValueError(f"Cannot open PDF: {redact(str(exc))}") from exc
        with doc:
            for page_num in range(doc.page_count):
                text = doc[page_num].get_text()
                lines = [line.strip() for line in text.split("\n") if line.strip()]
                if lines:
                    knowledge["slides"].append({
                        "page": page_num + 1,
                        "title": lines[0],
                        "content": lines[:5],
                    })
                    for line in lines[:3]:
                        for word in line.split():
                            if len(word) > 3 and (word.isupper() or word[0].isupper()):
                                knowledge["key_terms"].append(word)
        knowledge["key_terms"] = list(set(knowledge["key_terms"]))
        return knowledge

    def build_course_context(self, course_id: str, reference_dir: str | None = None) -> str:
        """Build comprehensive context string for vision prompt."""
        config = self.load_course_config(course_id)
        context_parts = [
            f"MATA KULIAH: {config.get('course_name', course_id)}",
            f"KODE: {config.get('code', '')}",
            f"DESKRIPSI: {config.get('description', '')}",
            "",
            "PANDUAN ANALISIS:",
        ]
        for area in config.get("analysis_guidelines", {}).get("focus_areas", []):
            context_parts.append(f"  - Fokus: {area}")
        context_parts.append("\n  Terminologi Teknis Kunci:")
        for term in config.get("analysis_guidelines", {}).get("technical_terms", []):
            context_parts.append(f"    - {term}")

        if reference_dir:
            base = self.reference_root or Path.cwd()
            candidate = Path(reference_dir)
            if not candidate.is_absolute():
                candidate = base / candidate
            try:
                ref_root = resolve_under_root(base, candidate, must_exist=True)
            except PathValidationError:
                raise
            except FileNotFoundError as e:
                raise PathValidationError(str(e)) from None
            pdf_files = sorted(ref_root.glob("*.pdf"))
            if pdf_files:
                context_parts.append(
                    "\n  REFERENSI MATERI PRAKTIKUM (dari slide PDF):"
                )
                for pdf in pdf_files:
                    pdf_knowledge = self.extract_pdf_knowledge(str(pdf))
                    context_parts.append(f"    File: {pdf.name}")
                    for slide in pdf_knowledge["slides"][:3]:
                        context_parts.append(
                            f"      Slide {slide['page']}: {slide['title'][:80]}"
                        )
                    if pdf_knowledge["key_terms"]:
                        context_parts.append(
                            "      Istilah kunci: "
                            + ", ".join(pdf_knowledge["key_terms"][:15])
                        )

        context_parts.append("\n  FORMAT OUTPUT:")
        context_parts.append(
            f"  Pola baris: {config.get('output_template', {}).get('line_pattern', '{index}.png | {label} | Konteks: {context} | Arah: {direction}')}"
        )
        context_parts.append(
            "  Bahasa: Indonesia, singkat, teknis, langsung to-the-point"
        )
        context_parts.append(
            "  Gaya: Seperti catatan praktikum mahasiswa (ringkas, berurutan)"
        )
        return "\n".join(context_parts)