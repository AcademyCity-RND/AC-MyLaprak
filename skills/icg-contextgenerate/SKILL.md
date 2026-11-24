---
name: icg-contextgenerate
description: "Use when implementing F2 ICG-ContextGenerate tasks — two-pass visual census + enriched context generation, narrative planning from screenshots, enriched inisiasi.txt format (@section, type=, group=), ACC-gated pending/final write, auto-save/resume via .icg_cache. VENDORED from ImageContext-Generator v0.3.0."
category: software-development
---

# ICG ContextGenerate Engine (F2) — Skill (VENDORED)

> **VENDORED COPY** — This skill is a local copy of the ICG ContextGenerate Engine from the [ImageContext-Generator](https://github.com/AcademyCity-RND/AC-ImageContext-Generator) repository (upstream commit: see VENDOR.md). The authoritative source for development remains the upstream repo. Changes here should be synced back upstream or re-vendored.

This skill covers the **ImageContext-Generator ContextGenerate Engine (F2)** — a two-pass pipeline that transforms lab screenshots into an enriched `inisiasi.txt` with narrative structure, per-image typing, grouping, and section mapping.

## Agent Pre-flight (WAJIB — sebelum menjalankan engine)

Saat user memberi folder sumber + klaim (mis. "modul chapter 11 Flask"), jangan
langsung generate dan jangan mengaudit bebas. Urutannya:

1. **Konfirmasi klaim user ke modul, bukan ke tebakan.**
   - Baca PDF/PPTX di folder sumber; cari heading pertemuan/section + nomor halaman.
   - Laporkan faktanya singkat: mis. "Flask ada di Pertemuan 10 (hlm 210–223);
     Pertemuan 11 = Streamlit".
   - **Jangan batalkan tugas** karena nomor bab berbeda dari kata user. Tugas
     ditentukan oleh folder/tugas yang user berikan, bukan penomoran modul.
2. **Petakan screenshot ke section laporan.** Konvensi yang berlaku (contoh PPD-11):
   - nama tanpa prefix `T` → **Hasil Praktikum**
   - nama dengan prefix `T` (`T1`, `T3-a`, `T8-c`) → **Tugas Praktikum**
   - Keduanya masuk **satu** `inisiasi.txt`; jangan menyingkirkan salah satunya.
3. **Klaim isi screenshot harus dari gambar (vision), bukan dari nama file.**
   Jangan mengarang isi proyek/file yang tidak terlihat di screenshot.
4. **`inisiasi.txt` yang belum ada = normal, F2 yang akan membuatnya.**
   Sumber = folder yang user berikan, dibaca langsung. **Pendekatan user tidak
   memakai folder `gambar/` sama sekali** — jangan menyebutnya sebagai "belum
   ada", prasyarat, atau target output. Jangan meminta konsolidasi/renumber
   sebelum generate kecuali user memintanya. `gambar/` hanya output opsional F1
   untuk alur lain, bukan bagian dari alur ini.
5. **Tanya ACC pengerjaan sebelum Pass 1.** Ringkas: file output, section, jumlah
   gambar, dan apa yang belum ada. Lalu berhenti dan tunggu jawaban user.
6. **Format nama saat F1 dijalankan:** pertahankan suffix manual (`7a`, `8b`,
   `T3-a`) apa adanya; urutan kanonik `1, 1a, 1b, …, T1, T1-a, …`; jangan
   renumber lintas section.

**Anti-pattern yang harus dihindari:** menyimpulkan screenshot "bukan tugas ini"
hanya dari nama file; menyebut file/proyek yang tidak ada di folder; menolak
generate karena `gambar/` kosong; atau menjalankan Pass 1 sebelum ACC.

---

## Pipeline Overview

```
Pass 1: Visual Census
  ContextEngine.visual_census(images, module_summary)  →  NarrativePlan
  [sections, order, groups, pairs] via single multimodal call (all images at once)

Pass 2: Enriched Context Generation
  ContextEngine.generate_context(images, plan, course_context)  →  list[InisiasiLine]
  One LLM call per image: type=, label, Konteks:, Arah:

Pending Store & ACC Gate
  ContextEngine.generate_pending()  →  .icg_cache/pending_inisiasi.txt (auto-save per image)
  ContextEngine.commit_pending(approved=True)  →  final inisiasi.txt (ACC required)
```

**ACC Gate**: Nothing is written to the final `inisiasi.txt` until `commit_pending(pending, final, approved=True)` is called — which must happen **only after user approves the pending output**.

---

## Local Engine Location

The vendored Python engine lives in `scripts/src/`, relative to this SKILL.md
(Hermes: `~/.hermes/skills/software-development/icg-contextgenerate/scripts/src/`;
Antigravity: `<repo>/skills/icg-contextgenerate/scripts/src/`).

Key modules:
- `context_engine.py` — Core engine (Pass 1 visual census, Pass 2 context generation, pending store, ACC gate)
- `vision_engine.py` — Vision AI integration (Gemini 3.1 Flash-Lite)
- `security.py` — Path validation (`resolve_under_root`)
- `renaming_engine.py` — Independent F1 pipeline (F2 can run on already-renamed `gambar/`)
- `director.py` — Independent Director Mode
- `knowledge_manager.py` — Course config YAML + PDF reference extraction
- `cli.py` — Typer CLI entry point (not used directly by skill; engine is imported)

## Installation (Dependencies)

```bash
pip install -r scripts/requirements.txt   # jalankan dari folder skill
```

Dependencies: `pyyaml`, `Pillow`, `python-dotenv`, `typer[all]`, `rich`, `google-genai`, `openai`, `fitz` (PyMuPDF), `python-pptx`.

> **Note:** Requires Python 3.12+. Set `GOOGLE_API_KEY` in environment or `.env` for vision generation.

---

## Data Structures

```python
@dataclass
class Section:
    id: str          # "S1", "S2", ...
    title: str       # "Konfigurasi Layanan & Orkestrasi Docker"

@dataclass
class NarrativePlan:
    sections: list[Section]           # Ordered sections
    order: list[str]                  # Image filenames in narrative order
    pairs: dict[str, str]             # Symmetric pairing: {"9.png": "10.png", "10.png": "9.png"}
    raw_response: str                 # Full LLM Pass 1 response
    image_sections: dict[str, str]    # {"1.png": "S1", "9.png": "S2", ...}

@dataclass
class InisiasiLine:
    filename: str = ""                # "1.png"
    section: str = ""                 # "S1"
    type: str = ""                    # config|code|terminal|gui|diagram|log
    group: str = "single"             # "single" | "pair:10"
    label: str = ""                   # "Inisialisasi Monorepo"
    konteks: str = ""                 # "Setup Laravel 11 + Vue 3"
    arah: str = ""                    # "CI/CD pipeline setup"
    raw: str = ""                     # Original line for legacy mode

@dataclass
class InisiasiDocument:
    mode: str                         # "enriched" | "legacy"
    sections: list[Section]
    lines: list[InisiasiLine]
```

---

## Key Functions

### Pass 1: Visual Census & Narrative Planning
```python
engine.visual_census(
    image_paths: list[Path],
    module_summary: str,
) -> NarrativePlan
```
- Sends **all images in one multimodal call** (prompt + PIL images).
- Returns structured `NarrativePlan` with sections, order, groups, pairs.
- LLM response format:
```
[SECTION] S1 | Judul Section 1
[SECTION] S2 | Judul Section 2
[ORDER] 1.png | 2.png | 9.png | 10.png
[GROUP] S1: 1.png, 2.png
[GROUP] S2: 9.png, 10.png
[PAIR] 9.png:10.png
```

### Pass 2: Per-Image Enriched Context
```python
engine.generate_context(
    image_paths: list[Path],
    plan: NarrativePlan,
    course_context: str,
) -> list[InisiasiLine]
```
- One LLM call **per image** (in `plan.order`).
- LLM response format (single line):
```
type=config | Inisialisasi Monorepo | Konteks: Setup Laravel 11 | Arah: CI/CD pipeline
```
- Invalid `type` values fall back to `config` (SEC-10 spirit).

### Pending Store & Auto-Save / Resume
```python
engine.generate_pending(
    image_paths: list[Path],
    plan: NarrativePlan,
    course_context: str,
    pending_path: Path,          # .icg_cache/pending_inisiasi.txt
    course: str,                 # "KEPL"
    meeting: str,                # "UTS"
) -> dict[str, int]              # {"total": N, "generated": M, "pending": K}
```
- Reads existing `pending_path` to resume (skips already-completed images).
- Generates images **one at a time**, writes pending after each success.
- On exception: stops, preserves partial progress in pending file.
- Returns counts for UI reporting.

### ACC Gate: Pending → Final
```python
ContextEngine.commit_pending(
    pending_path: Path,
    final_path: Path,
    *,
    approved: bool = False,
) -> None
```
- **Raises `AccRequiredError` if `approved=False`**.
- Moves pending → final atomically (shutil.move).
- Removes pending file on success.

---

## Serializers & Parsers

### Enriched Line Serialization (V17 Contract)
```python
serialize_enriched_line(line: InisiasiLine) -> str
# "1.png | S1 | type=config | group=single | Inisialisasi Monorepo | Konteks: Setup Laravel | Arah: CI/CD pipeline"
```

### Full Document Serialization
```python
serialize_enriched_document(
    lines: list[InisiasiLine],
    sections: list[Section],
    course: str,
    meeting: str,
    total: int,
    mode: str = "director",
) -> str
```
Output includes:
```
# ========================================================
# INISIASI: KEPL — UTS
# ENGINE: image-context v0.3 | MODE: director
# TOTAL: 4 gambar | URUTAN: narrative
# ========================================================
[@section] S1 | Konfigurasi Layanan & Orkestrasi Docker
[@section] S2 | Observability, Logging & Health Checking

1.png | S1 | type=config | group=single | Inisialisasi Monorepo | Konteks: Setup Laravel | Arah: CI/CD pipeline
9.png | S2 | type=terminal | group=pair:10 | Log terstruktur INFO | Konteks: artisan logs | Arah: structured logging
...
# ========================================================
```

### Dual-Mode Parser (Backward Compat E6)
```python
parse_inisiasi(text: str) -> InisiasiDocument
```
- **Enriched mode**: Detects `[@section]` headers and `type=`/`group=` in lines.
- **Legacy mode**: Reads free-form notes, lines with/without pipes.
- Never throws — returns best-effort document.

### Narrative Plan Parser
```python
parse_narrative_plan(text: str) -> NarrativePlan
```
- Extracts `[SECTION]`, `[ORDER]`, `[GROUP]`, `[PAIR]` markers (order-insensitive).
- Populates `image_sections` from `[GROUP]` lines.

### Natural Sort Key
```python
sort_image_name(filename: str) -> tuple[int, int, int, str]
```
Order: `1.png < 1a.png < 2.png < 9.png < 10.png < T1.png < T1-1.png`

---

## CLI Integration

```bash
python -m src.cli generate-context \
    --course kepl \
    --pertemuan UTS \
    --workspace workspace \
    --module-summary "Modul Docker: setup, build, health check" \
    --course-context "Mata kuliah KEPL, fokus CI/CD dengan GitHub Actions"
```

Options:
- `--course / -c`: Course ID (e.g., `kepl`, `ppg`).
- `--pertemuan / -p`: Pertemuan folder name (e.g., `Per4`, `UTS`).
- `--workspace / -w`: Workspace root (default: `workspace`).
- `--module-summary`: Brief module summary for Pass 1 narrative planning.
- `--course-context`: Additional context for Pass 2 per-image generation.
- `--output / -o`: Custom output file (must stay under workspace root).

**ACC Gate in CLI**: After Pass 2 completes, the CLI displays pending file location and prompts for approval before writing final `inisiasi.txt`.

---

## Constraints & Rules

1. **ACC is mandatory** — never call `commit_pending()` with `approved=False`.
2. **Git context is advisory only** — never override visual evidence from screenshots.
3. **Backward compatibility** — legacy `inisiai.txt` (free-form notes) must remain readable.
4. **Workspace isolation** — all paths validated via `resolve_under_root()`.
5. **Pass 1 is holistic** — all images sent in ONE call, not per-image.
6. **Pass 2 is per-image** — one LLM call per image for enriched context.
7. **Auto-save/resume** — `generate_pending` auto-saves after each image; resumes from `.icg_cache/pending_inisiasi.txt`.
8. **Type safety** — invalid `type` falls back to `config`; never poisons output.
9. **Pair symmetry** — `[PAIR] 9.png:10.png` implies both `9.png ↔ 10.png`.

---

## Testing (TDD)

Run tests against the vendored engine:
```bash
cd scripts   # dari folder skill ini
py -3.12 -m pytest tests/test_context_engine.py -v
```

> **Note:** Tests must be copied from upstream to run locally. See `VENDOR.md` in `scripts/` for the sync procedure.

Test coverage:
- `test_parse_inisiasi_reads_manual_freeform_notes` — legacy parser
- `test_parse_inisiasi_reads_enriched_format` — enriched parser
- `test_serialize_enriched_line_matches_contract` — V17 line format
- `test_serialize_enriched_document_includes_header_and_sections` — full doc
- `test_sort_image_name_orders_numeric_then_letter_then_task` — natural sort
- `test_parse_narrative_plan_extracts_sections_order_and_pairs` — Pass 1 parser
- `test_pass1_visual_census_sends_all_images_and_module_summary` — Pass 1 integration
- `test_pass2_generates_one_enriched_line_per_image` — Pass 2 integration
- `test_pass2_invalid_type_falls_back_to_config` — SEC-10 fallback
- `test_commit_requires_acc_approval_before_writing_final` — ACC gate (denied)
- `test_commit_writes_final_after_approval` — ACC gate (approved)
- `test_generate_pending_autosaves_and_resumes` — auto-save + resume
- `test_full_two_pass_pipeline` — end-to-end integration

---

## Integration Points

- **VisionEngine** (`src/vision_engine.py`): Provides the `model` for both passes.
- **Renaming Engine** (`src/renaming_engine.py`): Independent F1 pipeline; F2 can run on already-renamed `gambar/` images.
- **DirectorEngine** (`src/director.py`): Independent Director Mode; F2 is a separate pipeline.
- **Security** (`src/security.py`): All paths go through `resolve_under_root()`.
- **KnowledgeManager** (`src/knowledge_manager.py`): Not directly used; `--module-summary` may come from its knowledge base.

---

## Common Pitfalls

| Pitfall | Prevention |
|---------|------------|
| Passing images one-by-one in Pass 1 | `visual_census` MUST send all images in single call |
| Forgetting ACC gate | `commit_pending` enforces `approved=True` at Python level |
| Pending file corruption on crash | Auto-save after each image; pending is valid at any point |
| Resume not skipping completed | `generate_pending` reads existing pending first |
| Invalid type poisoning output | `_parse_pass2_line` falls back to `config` |
| Pair asymmetry in Pass 1 | `[PAIR] a:b` → add both `a→b` and `b→a` in `pairs` dict |
| Legacy inisiasi.txt broken | `parse_inisiasi` dual-mode; never changes format detection |
| Langsung generate tanpa konfirmasi klaim user | Ikuti Agent Pre-flight langkah 1–5 |
| Screenshot non-T dianggap "bukan tugas" | non-T = Hasil Praktikum, T = Tugas Praktikum (satu dokumen) |
| `gambar/` kosong dijadikan blocker | `gambar/` opsional; sumber = folder user |
| Mengarang isi screenshot dari nama file | Buka gambar via vision sebelum mengklaim |

---

## Future Extensions (not F2)

- Confidence scoring from vision (logprobs / ensemble) for Pass 2.
- OCR-based context extraction from screenshot text.
- Cross-session narrative continuity (persistent plan cache).
- Interactive ACC review (TUI for pending table with diffs).
- Multi-meeting narrative linking (S1 in Per4 → S3 in Per5).

---

## Vendor Metadata

- **Upstream Repo:** https://github.com/AcademyCity-RND/AC-ImageContext-Generator
- **Upstream Skill:** `icg-context-generate` (skills/icg-context-generate/SKILL.md)
- **Vendored Commit:** See `VENDOR.md` in `scripts/`
- **Vendor Date:** 2026-11-24 (F4 integration)
- **MyLaprak Version:** v0.4.0