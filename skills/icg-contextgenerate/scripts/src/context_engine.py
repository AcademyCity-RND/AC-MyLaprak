"""ICG-ContextGenerate engine (F2) — visual census + enriched context generation.

Pass 1: Visual Census & Narrative Planning (holistic, all images at once)
Pass 2: Context Generation per image (enriched format: @section, type=, group=)
ACC gate: pending -> final only after user approval
Auto-save/resume via .icg_cache/pending_inisiasi.txt
"""
from __future__ import annotations

import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Constants & helpers
# ---------------------------------------------------------------------------
VALID_TYPES = {"config", "code", "terminal", "gui", "diagram", "log"}
DEFAULT_TYPE = "config"


def sort_image_name(filename: str) -> tuple[int, int, int, str]:
    """Sort key for image filenames like 1.png, 1a.png, 9.png, 10.png, T1.png.

    Ordering: numeric basename first (1 < 1a < 2 < 10), then T-prefixed tasks.
    """
    stem = Path(filename).stem
    m = re.match(r"^(\d+)([a-z]*)$", stem, re.IGNORECASE)
    if m:
        suffix = m.group(2).lower()
        return (0, int(m.group(1)), 1 if suffix else 0, suffix)
    m = re.match(r"^T(\d+)-?(\d*)([a-z]*)$", stem, re.IGNORECASE)
    if m:
        return (1, int(m.group(1)), int(m.group(2) or 0), m.group(3).lower())
    return (2, 0, 0, stem)


# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------
@dataclass
class Section:
    id: str
    title: str


@dataclass
class NarrativePlan:
    sections: list[Section]
    order: list[str]
    pairs: dict[str, str]
    raw_response: str = ""
    image_sections: dict[str, str] = field(default_factory=dict)

    def section_for(self, filename: str) -> str:
        return self.image_sections.get(filename, "")


@dataclass
class InisiasiLine:
    filename: str = ""
    section: str = ""
    type: str = ""
    group: str = "single"
    label: str = ""
    konteks: str = ""
    arah: str = ""
    raw: str = ""


@dataclass
class InisiasiDocument:
    mode: str  # "enriched" | "legacy"
    sections: list[Section]
    lines: list[InisiasiLine]


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------
class AccRequiredError(RuntimeError):
    """Raised when commit_pending is called without explicit approval."""


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------
def parse_narrative_plan(text: str) -> NarrativePlan:
    """Parse Pass 1 LLM response into structured plan.

    Expected lines (order-insensitive, prefixes optional #):
      [SECTION] S1 | Title
      [ORDER] 1.png | 2.png | 9.png
      [GROUP] S1: 1.png, 2.png
      [PAIR] 9.png:10.png
    """
    sections: list[Section] = []
    order: list[str] = []
    pairs: dict[str, str] = {}
    image_sections: dict[str, str] = {}

    for raw_line in text.splitlines():
        line = raw_line.strip().lstrip("#").strip()
        if not line:
            continue
        if line.startswith("[SECTION]"):
            rest = line[len("[SECTION]"):].strip()
            if "|" in rest:
                sid, title = rest.split("|", 1)
                sections.append(Section(id=sid.strip(), title=title.strip()))
        elif line.startswith("[ORDER]"):
            rest = line[len("[ORDER]"):].strip()
            for part in rest.split("|"):
                name = part.strip()
                if name:
                    order.append(name)
        elif line.startswith("[GROUP]"):
            rest = line[len("[GROUP]"):].strip()
            if ":" in rest:
                sid, names = rest.split(":", 1)
                sid = sid.strip()
                for n in names.split(","):
                    n = n.strip()
                    if n:
                        image_sections[n] = sid
        elif line.startswith("[PAIR]"):
            rest = line[len("[PAIR]"):].strip()
            if ":" in rest:
                a, b = rest.split(":", 1)
                a, b = a.strip(), b.strip()
                if a and b:
                    pairs[a] = b
                    pairs[b] = a

    return NarrativePlan(
        sections=sections,
        order=order,
        pairs=pairs,
        raw_response=text,
        image_sections=image_sections,
    )


def parse_inisiasi(text: str) -> InisiasiDocument:
    """Parse inisiasi.txt — dual mode: enriched (with @section, type=, group=) or legacy."""
    lines: list[InisiasiLine] = []
    sections: list[Section] = []
    mode = "legacy"

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line:
            continue

        # [@...] section markers (may or may not be preceded by #)
        if line.startswith("[@section]"):
            rest = line[len("[@section]"):].strip()
            if "|" in rest:
                sid, title = rest.split("|", 1)
                sections.append(Section(id=sid.strip(), title=title.strip()))
                mode = "enriched"
            continue

        if line.startswith("#"):
            continue

        # Enriched line: N.png | S1 | type=config | group=single | Label | Konteks: ... | Arah: ...
        if "|" in line:
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 7 and parts[2].startswith("type=") and parts[3].startswith("group="):
                mode = "enriched"
                filename = parts[0].replace(".png", "").strip()
                section = parts[1]
                type_val = parts[2].split("=", 1)[1].strip()
                group_val = parts[3].split("=", 1)[1].strip()
                label = parts[4]
                konteks = parts[5].split(":", 1)[1].strip() if ":" in parts[5] else parts[5]
                arah = parts[6].split(":", 1)[1].strip() if ":" in parts[6] else parts[6]
                lines.append(InisiasiLine(
                    filename=filename + ".png" if not filename.endswith(".png") else filename,
                    section=section, type=type_val, group=group_val,
                    label=label, konteks=konteks, arah=arah, raw=line,
                ))
                continue

            # Legacy line with pipes: N.png | Label | Konteks: ... | Arah: ...
            if len(parts) >= 4:
                filename = parts[0].replace(".png", "").strip()
                label = parts[1]
                konteks = parts[2].split(":", 1)[1].strip() if ":" in parts[2] else parts[2]
                arah = parts[3].split(":", 1)[1].strip() if ":" in parts[3] else parts[3]
                lines.append(InisiasiLine(
                    filename=filename + ".png" if not filename.endswith(".png") else filename,
                    label=label, konteks=konteks, arah=arah, raw=line,
                ))
                continue

            # Legacy line with fewer parts
            lines.append(InisiasiLine(raw=line))
            continue

        # Pure free-form legacy (no pipes)
        lines.append(InisiasiLine(raw=line))

    return InisiasiDocument(mode=mode, sections=sections, lines=lines)


# ---------------------------------------------------------------------------
# Serializers
# ---------------------------------------------------------------------------
def serialize_enriched_line(line: InisiasiLine) -> str:
    """Serialize one InisiasiLine in enriched format."""
    return " | ".join([
        line.filename,
        line.section,
        f"type={line.type}",
        f"group={line.group}",
        line.label,
        f"Konteks: {line.konteks}",
        f"Arah: {line.arah}",
    ])


def serialize_enriched_document(
    lines: list[InisiasiLine],
    sections: list[Section],
    course: str,
    meeting: str,
    total: int,
    mode: str = "director",
) -> str:
    """Serialize full enriched inisiasi.txt document."""
    header = [
        "# ========================================================",
        f"# INISIASI: {course} — {meeting}",
        f"# ENGINE: image-context v0.3 | MODE: {mode}",
        f"# TOTAL: {total} gambar | URUTAN: narrative",
        "# ========================================================",
        "",
    ]
    section_lines = [f"[@section] {s.id} | {s.title}" for s in sections]
    body = [serialize_enriched_line(l) for l in lines]
    footer = ["", "# ========================================================"]
    return "\n".join(header + section_lines + [""] + body + footer)


# ---------------------------------------------------------------------------
# ContextEngine
# ---------------------------------------------------------------------------
class ContextEngine:
    """Two-pass enriched context generator."""

    def __init__(self, model: Any):
        self.model = model

    # ---- Pass 1 ----
    def visual_census(
        self,
        image_paths: list[Path],
        module_summary: str,
    ) -> NarrativePlan:
        """Pass 1: send all images + module summary in ONE call; get narrative plan."""
        pil_images = []
        for p in image_paths:
            from PIL import Image
            pil_images.append(Image.open(p).copy())

        prompt = self._build_pass1_prompt(module_summary, image_paths)
        # single call: [prompt, *pil_images]
        response = self.model.generate_content([prompt, *pil_images])
        return parse_narrative_plan(response.text or "")

    def _build_pass1_prompt(self, module_summary: str, image_paths: list[Path]) -> str:
        names = "\n".join(f"- {p.name}" for p in image_paths)
        return f"""Anda adalah asisten perencanaan narasi laporan praktikum.
Berikut ringkasan modul praktikum:
{module_summary}

Gambar yang tersedia ({len(image_paths)} total):
{names}

TUGAS: Buat rencana narasi holistik untuk semua gambar di atas.
Output HANYA format berikut (tanpa teks tambahan):

[SECTION] S1 | Judul Section 1
[SECTION] S2 | Judul Section 2
...
[ORDER] 1.png | 2.png | 9.png | 10.png | ...
[GROUP] S1: 1.png, 2.png
[GROUP] S2: 9.png, 10.png
...
[PAIR] 9.png:10.png
[PAIR] ...

Aturan:
- Section S1..Sn: kelompokkan gambar ke dalam alur logis (setup, observability, validasi, dll).
- ORDER: urutan final gambar sesuai narasi (bukan mtime, bukan nama file).
- GROUP: setiap gambar harus berada di tepat satu section.
- PAIR: pasangkan gambar yang saling terkait (terminal+GUI, sebelum+sesudah) — simetris.
- Setiap gambar muncul tepat sekali di ORDER dan GROUP.
"""

    # ---- Pass 2 ----
    def generate_context(
        self,
        image_paths: list[Path],
        plan: NarrativePlan,
        course_context: str,
    ) -> list[InisiasiLine]:
        """Pass 2: generate enriched line for each image in plan order."""
        path_by_name = {p.name: p for p in image_paths}
        lines: list[InisiasiLine] = []

        for filename in plan.order:
            path = path_by_name.get(filename)
            if path is None:
                continue

            section = plan.section_for(filename)
            pair = plan.pairs.get(filename)
            if pair:
                pair_stem = Path(pair).stem
                group = f"pair:{pair_stem}"
            else:
                group = "single"

            prompt = self._build_pass2_prompt(
                filename=filename,
                section=section,
                group=group,
                course_context=course_context,
            )
            from PIL import Image
            pil_img = Image.open(path).copy()
            response = self.model.generate_content([prompt, pil_img])
            text = (response.text or "").strip()

            # Parse LLM response: "type=X | Label | Konteks: ... | Arah: ..."
            line = self._parse_pass2_line(
                filename=filename,
                section=section,
                group=group,
                response_text=text,
            )
            lines.append(line)

        return lines

    def _build_pass2_prompt(
        self,
        filename: str,
        section: str,
        group: str,
        course_context: str,
    ) -> str:
        return f"""Analisis screenshot '{filename}' untuk laporan praktikum.

Section: {section}
Group: {group}  (type: config|code|terminal|gui|diagram|log)
Konteks materi: {course_context}

Buat SATU baris format enriched (TANPA nama file dan section di depan):
type=<type> | <Label> | Konteks: <konteks teknis> | Arah: <arah analisis>

Aturan ketat:
- type HARUS salah satu: config, code, terminal, gui, diagram, log
- Label: judul singkat ≤ 50 karakter, deskripsi visual nyata
- Konteks: fakta teknis yang terlihat (GUI/terminal/editor/browser)
- Arah: arah pembahasan/evaluasi teknis
- Bahasa Indonesia, teknis, ringkas
- Output HANYA satu baris, tanpa penjelasan, tanpa markdown
"""

    def _parse_pass2_line(
        self,
        filename: str,
        section: str,
        group: str,
        response_text: str,
    ) -> InisiasiLine:
        # Expected: "type=config | Inisialisasi Monorepo | Konteks: Setup Laravel | Arah: CI/CD"
        parts = [p.strip() for p in response_text.split("|")]
        if len(parts) < 4:
            return InisiasiLine(
                filename=filename, section=section, type=DEFAULT_TYPE, group=group,
                label=filename, konteks="", arah="",
            )

        type_raw = parts[0]
        type_val = DEFAULT_TYPE
        if type_raw.startswith("type="):
            type_val = type_raw.split("=", 1)[1].strip()
            if type_val not in VALID_TYPES:
                type_val = DEFAULT_TYPE

        label = parts[1]
        konteks = parts[2].split(":", 1)[1].strip() if ":" in parts[2] else parts[2]
        arah = parts[3].split(":", 1)[1].strip() if ":" in parts[3] else parts[3]

        return InisiasiLine(
            filename=filename,
            section=section,
            type=type_val,
            group=group,
            label=label,
            konteks=konteks,
            arah=arah,
        )

    # ---- Pending store / ACC gate ----
    def generate_pending(
        self,
        image_paths: list[Path],
        plan: NarrativePlan,
        course_context: str,
        pending_path: Path,
        course: str,
        meeting: str,
    ) -> dict[str, int]:
        """Run Pass 2 with per-image auto-save to pending file; resume from existing pending.

        Generates images one at a time, writing pending after each success.
        If an image fails (exception), stops and preserves partial progress.
        On resume, skips already-completed images.
        """
        pending_path.parent.mkdir(parents=True, exist_ok=True)

        # Load existing pending (resume)
        completed: dict[str, InisiasiLine] = {}
        if pending_path.exists():
            doc = parse_inisiasi(pending_path.read_text(encoding="utf-8"))
            for l in doc.lines:
                if l.filename:
                    completed[l.filename] = l

        path_by_name = {p.name: p for p in image_paths}
        to_generate = [f for f in plan.order if f not in completed and f in path_by_name]

        # Generate one at a time, auto-save after each
        for filename in to_generate:
            try:
                new_lines = self.generate_context([path_by_name[filename]], plan, course_context)
                completed[filename] = new_lines[0]
            except Exception:
                # Partial progress preserved in pending; stop on first failure
                break

            # Auto-save after each image
            sorted_lines = [completed[f] for f in plan.order if f in completed]
            total = len(plan.order)
            pending_text = serialize_enriched_document(
                lines=sorted_lines,
                sections=plan.sections,
                course=course,
                meeting=meeting,
                total=total,
                mode="director",
            )
            pending_path.write_text(pending_text, encoding="utf-8")

        # Final write (in case loop completed without exceptions)
        sorted_lines = [completed[f] for f in plan.order if f in completed]
        total = len(plan.order)
        pending_text = serialize_enriched_document(
            lines=sorted_lines,
            sections=plan.sections,
            course=course,
            meeting=meeting,
            total=total,
            mode="director",
        )
        pending_path.write_text(pending_text, encoding="utf-8")

        return {"total": total, "generated": len(completed), "pending": len(to_generate)}

    @staticmethod
    def commit_pending(pending_path: Path, final_path: Path, *, approved: bool = False) -> None:
        """Move pending -> final ONLY if approved=True (ACC gate)."""
        if not approved:
            raise AccRequiredError("ACC required before writing final inisiasi.txt")
        if not pending_path.exists():
            raise FileNotFoundError(f"Pending file not found: {pending_path}")
        final_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(str(pending_path), str(final_path))