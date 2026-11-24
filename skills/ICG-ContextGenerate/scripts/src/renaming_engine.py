"""F1 — ICG Renaming Engine.

Turns a pile of raw screenshots into an ordered, deduplicated, canonically
named image folder that follows the lab module (PDF/PPTX) step order.

Pipeline:
    extract_module_steps()  ->  [ModuleStep, ...]
    classify (vision)       ->  step index per screenshot
    dedup_screenshots()     ->  unique files per step + duplicate report
    assign_final_names()    ->  1.png, 1a.png, T1.png, T2-1.png, ...
    RenamingPlan.commit()   ->  write gambar/ + renaming_report.txt (ACC gate)

ACC gate: nothing is written to the output folder until `plan.commit()` is
called, which must happen only after the user approves the mapping table.
"""
from __future__ import annotations

import hashlib
import re
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from PIL import Image


def _natural_sort_key(name: str) -> tuple:
    """Natural sort key: '1.png', '2.png', '10.png' sorts numerically.

    Splits string into (numeric_part, non_numeric_part) tuples so that
    '2.png' < '10.png' < '10a.png' < '11.png'.
    """
    parts = re.split(r"(\d+)", name)
    key = []
    for part in parts:
        if part.isdigit():
            key.append((0, int(part)))  # numeric parts sort first by value
        else:
            key.append((1, part))  # non-numeric parts sort after
    return tuple(key)


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ModuleStep:
    """One ordered step of the lab module."""

    title: str
    is_task: bool = False


@dataclass
class RenameMapping:
    """Mapping of one source screenshot to its canonical final name."""

    source_path: Path
    final_name: str
    step_index: int
    step_title: str
    confidence: float = 1.0
    matched_by: str = "vision"  # "vision" | "fallback"


@dataclass
class RenamingPlan:
    """Full renaming proposal — written to disk only by `commit()`."""

    mappings: list[RenameMapping] = field(default_factory=list)
    duplicates: list[dict] = field(default_factory=list)
    unmatched: list[Path] = field(default_factory=list)
    mode: str = "reference"  # "reference" | "mtime-fallback"
    output_dir: Path = field(default_factory=lambda: Path("gambar"))
    source_dir: Path = field(default_factory=lambda: Path("gambar_raw"))

    @property
    def is_empty(self) -> bool:
        return not self.mappings

    def summary_rows(self) -> list[tuple[str, str, str, str]]:
        """(source name, final name, step label, confidence) for the ACC table."""
        return [
            (
                m.source_path.name,
                m.final_name,
                f"{m.step_index}. {m.step_title}",
                f"{m.confidence:.2f}",
            )
            for m in sorted(self.mappings, key=lambda x: _natural_sort_key(x.final_name))
        ]

    def commit(self) -> Path:
        """Write renamed copies + report. Only call after user ACC."""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        for mapping in self.mappings:
            shutil.copy2(mapping.source_path, self.output_dir / mapping.final_name)
        # Copy unmatched files to unmatched/ subfolder
        if self.unmatched:
            unmatched_dir = self.output_dir / "unmatched"
            unmatched_dir.mkdir(parents=True, exist_ok=True)
            for src_path in self.unmatched:
                shutil.copy2(src_path, unmatched_dir / src_path.name)
        report_path = self.output_dir / "renaming_report.txt"
        report_path.write_text(self.render_report(), encoding="utf-8")
        return report_path

    def render_report(self) -> str:
        lines = [
            "# RENAMING REPORT",
            f"Mode: {self.mode}",
            f"Unique kept: {len(self.mappings)}",
            f"Duplicates removed: {len(self.duplicates)}",
            f"Unmatched: {len(self.unmatched)}",
            "",
            "=== MAPPINGS ===",
        ]
        for m in sorted(self.mappings, key=lambda x: _natural_sort_key(x.final_name)):
            lines.append(
                f"{m.final_name} <- {m.source_path.name} | "
                f"step={m.step_index} ({m.step_title}) | "
                f"conf={m.confidence:.2f} | {m.matched_by}"
            )
        if self.duplicates:
            lines += ["", "=== DUPLICATES REMOVED ==="]
            for dup in self.duplicates:
                lines.append(
                    f"kept={dup['kept'].name} removed={dup['removed'].name} "
                    f"reason={dup['reason']}"
                )
        if self.unmatched:
            lines += ["", "=== UNMATCHED ==="]
            lines += [f"{p.name}" for p in self.unmatched]
        return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Module step extraction (PDF / PPTX)
# ---------------------------------------------------------------------------

_TASK_KEYWORDS = ("tugas", "latihan", "exercise", "assignment", "task")
_NUMBERED_RE = re.compile(
    r"^(?:\d+\s*[.)]\s*|langkah\s+\d+\s*[.:]\s*|step\s+\d+\s*[.:]\s*)",
    re.IGNORECASE,
)
_TASK_PREFIX_RE = re.compile(
    r"^(?:tugas(?:\s+akhir)?|latihan|exercise|assignment|task)\s*[:\-]\s*",
    re.IGNORECASE,
)


def _is_task_line(line: str) -> bool:
    low = line.lower()
    return any(keyword in low for keyword in _TASK_KEYWORDS)


def _is_step_line(line: str) -> bool:
    return bool(_NUMBERED_RE.match(line.strip()))


def _clean_title(line: str) -> str:
    """Strip numbering and task prefixes: '1. Setup' -> 'Setup', 'Tugas: X' -> 'X'."""
    title = _NUMBERED_RE.sub("", line.strip())
    title = _TASK_PREFIX_RE.sub("", title)
    return title.strip()


def extract_steps_from_pdf(pdf_path: str | Path) -> list[ModuleStep]:
    """Extract ordered module steps from a PDF reference."""
    import fitz

    steps: list[ModuleStep] = []
    with fitz.open(str(pdf_path)) as doc:
        for page in doc:
            for raw in page.get_text().split("\n"):
                line = raw.strip()
                if not line:
                    continue
                if _is_step_line(line):
                    steps.append(ModuleStep(_clean_title(line), is_task=False))
                elif _is_task_line(line):
                    steps.append(ModuleStep(_clean_title(line), is_task=True))

    if not steps:
        # Fallback: first non-empty line of each page = slide title.
        with fitz.open(str(pdf_path)) as doc:
            for page in doc:
                lines = [ln.strip() for ln in page.get_text().split("\n") if ln.strip()]
                if lines:
                    steps.append(ModuleStep(_clean_title(lines[0]), is_task=False))
    return steps


def extract_steps_from_pptx(pptx_path: str | Path) -> list[ModuleStep]:
    """Extract ordered module steps from PPTX slide titles."""
    from pptx import Presentation

    steps: list[ModuleStep] = []
    presentation = Presentation(str(pptx_path))
    for slide in presentation.slides:
        title_shape = slide.shapes.title
        if title_shape is None or not title_shape.text:
            continue
        raw = title_shape.text.strip()
        if not raw:
            continue
        steps.append(
            ModuleStep(_clean_title(raw), is_task=_is_task_line(raw))
        )
    return steps


def extract_module_steps(reference_path: str | Path) -> list[ModuleStep]:
    """
    Dispatch to the right extractor based on extension.

    If `reference_path` is a directory, pick the first PDF else first PPTX inside.
    If it's a file, use it directly.
    """
    ref = Path(reference_path)
    if not ref.exists():
        return []

    if ref.is_file():
        if ref.suffix.lower() == ".pdf":
            return extract_steps_from_pdf(ref)
        if ref.suffix.lower() == ".pptx":
            return extract_steps_from_pptx(ref)
        return []

    # Directory — scan for reference files
    pdfs = sorted(ref.glob("*.pdf"))
    if pdfs:
        return extract_steps_from_pdf(pdfs[0])
    pptxs = sorted(ref.glob("*.pptx"))
    if pptxs:
        return extract_steps_from_pptx(pptxs[0])
    return []


# ---------------------------------------------------------------------------
# Hashing & perceptual hash
# ---------------------------------------------------------------------------


def hash_file(path: str | Path) -> str:
    """SHA-256 hex digest of the file bytes (exact-duplicate detection)."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def perceptual_hash(path: str | Path, hash_size: int = 8) -> int:
    """dHash: grayscale resize to (hash_size+1, hash_size), compare neighbours."""
    with Image.open(str(path)) as img:
        small = img.convert("L").resize((hash_size + 1, hash_size))
        pixels = list(small.tobytes())
    bits = 0
    width = hash_size + 1
    for row in range(hash_size):
        for col in range(hash_size):
            left = pixels[row * width + col]
            right = pixels[row * width + col + 1]
            bits = (bits << 1) | (1 if left > right else 0)
    return bits


def hamming_distance(a: int, b: int) -> int:
    return bin(a ^ b).count("1")


def _avg_color(path: str | Path) -> tuple[float, float, float]:
    """Return mean R, G, B for quick uniform-image detection."""
    with Image.open(str(path)) as img:
        img = img.convert("RGB").resize((16, 16))
        data = img.tobytes()  # 3 bytes per pixel: R, G, B
        n = 16 * 16
        r = sum(data[i * 3] for i in range(n)) / n
        g = sum(data[i * 3 + 1] for i in range(n)) / n
        b = sum(data[i * 3 + 2] for i in range(n)) / n
    return (r, g, b)


def _color_distance(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    return ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2) ** 0.5


def _is_uniform_image(path: str | Path, threshold: float = 5.0) -> bool:
    """Detect near-solid-color images (low variance)."""
    with Image.open(str(path)) as img:
        img = img.convert("L").resize((16, 16))
        data = img.tobytes()  # 1 byte per pixel (grayscale)
        if not data:
            return True
        n = len(data)
        mean = sum(data) / n
        var = sum((p - mean) ** 2 for p in data) / n
    return var < threshold


# ---------------------------------------------------------------------------
# Deduplication
# ---------------------------------------------------------------------------


def _mtime(path: Path) -> float:
    return path.stat().st_mtime


def dedup_screenshots(
    paths: list[Path],
    phash_threshold: int = 5,
    color_dist_threshold: float = 30.0,
) -> tuple[list[Path], list[dict]]:
    """
    Remove exact duplicates (SHA-256) and near-duplicates (dHash).

    Exact duplicates: the first file in input order is kept.
    Near duplicates: the newest file (mtime) is kept, older variants flagged.
    Skips perceptual dedup for uniform (solid-color) images or when average
    color distance exceeds `color_dist_threshold`.
    """
    duplicates: list[dict] = []

    # Stage 1 — exact hash, keep the first occurrence in input order.
    seen_hashes: dict[str, Path] = {}
    unique_after_hash: list[Path] = []
    for path in paths:
        digest = hash_file(path)
        if digest in seen_hashes:
            duplicates.append(
                {"kept": seen_hashes[digest], "removed": path, "reason": "hash"}
            )
        else:
            seen_hashes[digest] = path
            unique_after_hash.append(path)

    if len(unique_after_hash) <= 1:
        return unique_after_hash, duplicates

    # Stage 2 — perceptual hash, keep the newest file.
    hashed = [(path, perceptual_hash(path)) for path in unique_after_hash]
    # Precompute average colors for color-distance guard
    avg_colors = {path: _avg_color(path) for path in unique_after_hash}

    keep = [True] * len(hashed)
    for i in range(len(hashed)):
        if not keep[i]:
            continue
        for j in range(i + 1, len(hashed)):
            if not keep[j]:
                continue
            # Primary guard: color distance
            if _color_distance(avg_colors[hashed[i][0]], avg_colors[hashed[j][0]]) > color_dist_threshold:
                continue
            # Guard: if both are uniform images with DISSIMILAR colors, skip phash
            # (prevents false positives on solid-color images of different hues)
            if _is_uniform_image(hashed[i][0]) and _is_uniform_image(hashed[j][0]):
                if _color_distance(avg_colors[hashed[i][0]], avg_colors[hashed[j][0]]) > 5.0:
                    continue
            if hamming_distance(hashed[i][1], hashed[j][1]) > phash_threshold:
                continue
            if _mtime(hashed[i][0]) >= _mtime(hashed[j][0]):
                kept_idx, removed_idx = i, j
            else:
                kept_idx, removed_idx = j, i
            keep[removed_idx] = False
            duplicates.append(
                {
                    "kept": hashed[kept_idx][0],
                    "removed": hashed[removed_idx][0],
                    "reason": "phash",
                }
            )
            if removed_idx == i:
                break

    return [path for path, alive in zip(unique_after_hash, keep) if alive], duplicates


# ---------------------------------------------------------------------------
# Naming
# ---------------------------------------------------------------------------


def _index_to_letter(index: int) -> str:
    """0 -> 'a', 25 -> 'z', 26 -> 'aa' (Excel-style suffix)."""
    letters = []
    index += 1
    while index > 0:
        index -= 1
        letters.append(chr(ord("a") + index % 26))
        index //= 26
    return "".join(reversed(letters))


def assign_final_names(
    groups: list[tuple[ModuleStep, list[Path | str]]],
) -> list[RenameMapping]:
    """
    Assign canonical names. `groups` is ordered [(step, [source, ...]), ...].

    Regular step, 1 shot      -> 1.png
    Regular step, N shots     -> 1a.png, 1b.png, ...
    Task step, 1 shot         -> T1.png
    Task step, N shots        -> T1-1.png, T1-2.png, ...
    """
    mappings: list[RenameMapping] = []
    step_counter = 0
    task_counter = 0

    for step, sources in groups:
        if not sources:
            continue
        paths = [Path(s) for s in sources]
        if step.is_task:
            task_counter += 1
            if len(paths) == 1:
                names = [f"T{task_counter}.png"]
            else:
                names = [f"T{task_counter}-{i}.png" for i in range(1, len(paths) + 1)]
            step_number = task_counter
        else:
            step_counter += 1
            if len(paths) == 1:
                names = [f"{step_counter}.png"]
            else:
                names = [
                    f"{step_counter}{_index_to_letter(i)}.png"
                    for i in range(len(paths))
                ]
            step_number = step_counter

        for source, name in zip(paths, names):
            mappings.append(
                RenameMapping(
                    source_path=source,
                    final_name=name,
                    step_index=step_number,
                    step_title=step.title,
                )
            )
    return mappings


# ---------------------------------------------------------------------------
# Plan building (ACC gate)
# ---------------------------------------------------------------------------

# (image path, candidate steps) -> (1-based step index, confidence); 0 = unmatched.
ClassifierFn = Callable[[Path, list[ModuleStep]], "tuple[int, float]"]

_IMAGE_SUFFIXES = (".png", ".jpg", ".jpeg")


def list_screenshots(directory: str | Path) -> list[Path]:
    """All screenshot files in a directory, case-insensitive extension match."""
    folder = Path(directory)
    return sorted(
        p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in _IMAGE_SUFFIXES
    )


def build_renaming_plan(
    source_dir: str | Path,
    reference_dir: str | Path | None,
    output_dir: str | Path,
    classifier: ClassifierFn | None = None,
) -> RenamingPlan:
    """
    Build the renaming proposal. Nothing is written until `plan.commit()`.

    Without a reference (or without a classifier) the plan falls back to
    mtime ordering with sequential names and `mode="mtime-fallback"`.
    """
    src = Path(source_dir)
    out = Path(output_dir)
    if not src.exists():
        raise FileNotFoundError(f"Source directory not found: {src}")

    images = list_screenshots(src)
    if not images:
        return RenamingPlan(output_dir=out, source_dir=src)

    steps = extract_module_steps(reference_dir) if reference_dir else []

    if not steps or classifier is None:
        # Fallback: dedup first, then each unique image is its own step (mtime order).
        images = sorted(images, key=_mtime)
        unique_images, all_duplicates = dedup_screenshots(images)
        groups = [
            (ModuleStep(f"Screenshot {i}", False), [path])
            for i, path in enumerate(unique_images, start=1)
        ]
        mappings = assign_final_names(groups)
        for mapping in mappings:
            mapping.matched_by = "fallback"
            mapping.confidence = 1.0
        return RenamingPlan(
            mappings=mappings,
            duplicates=all_duplicates,
            mode="mtime-fallback",
            output_dir=out,
            source_dir=src,
        )

    # Reference mode: global exact/perceptual pre-dedup BEFORE classification,
    # then dedup within each step bucket for visual-similarity duplicates.
    images = sorted(images, key=_mtime)
    unique_images, global_duplicates = dedup_screenshots(images)

    buckets: dict[int, list[Path]] = {i: [] for i in range(1, len(steps) + 1)}
    confidence: dict[Path, float] = {}
    unmatched: list[Path] = []
    for image in unique_images:
        step_index, score = classifier(image, steps)
        if 1 <= step_index <= len(steps):
            buckets[step_index].append(image)
            confidence[image] = score
        else:
            unmatched.append(image)

    all_duplicates: list[dict] = list(global_duplicates)
    groups: list[tuple[ModuleStep, list[Path]]] = []
    for i in range(1, len(steps) + 1):
        if buckets[i]:
            unique_in_bucket, dup_in_bucket = dedup_screenshots(buckets[i])
            all_duplicates.extend(dup_in_bucket)
            groups.append((steps[i - 1], unique_in_bucket))

    mappings = assign_final_names(groups)
    for mapping in mappings:
        mapping.matched_by = "vision"
        mapping.confidence = confidence.get(mapping.source_path, 0.0)

    return RenamingPlan(
        mappings=mappings,
        duplicates=all_duplicates,
        unmatched=unmatched,
        mode="reference",
        output_dir=out,
        source_dir=src,
    )