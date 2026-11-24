# VENDOR.md — ICG-Renaming Engine

This directory contains a **vendored copy** of the ImageContext-Generator Renaming Engine (F1).

## Provenance

| Field | Value |
|-------|-------|
| Upstream repository | `C:/laragon/www/ImageContext-Generator` |
| Upstream URL | https://github.com/AcademyCity-RND/ImageContext-Generator |
| Vendored commit | `32a81c1d499217965518548a2a9a28cd6bd422ac` (base HEAD only — **not** the exact source) |
| Source snapshot | Upstream **working tree @ 2026-11-24**, i.e. commit `32a81c1` + uncommitted R4/R5 fixes |
| Source detail | 4 modules modified vs. `32a81c1` (`cli.py`, `director.py`, `knowledge_manager.py`, `vision_engine.py`); 3 modules **untracked** in that commit (`context_engine.py`, `renaming_engine.py`, `security.py`) — vendored bytes came from the working tree, not from the commit object |
| Commit date | 2026-10-23 18:57:49 +0700 (base HEAD; source snapshot is newer) |
| Commit subject | `feat(director): add output path option, resume capability, and auto-save for Director Mode` (base HEAD) |
| Vendor date | 2026-11-24 (F4 integration into MyLaprak v0.4.0) |
| Vendored paths | `src/*.py` → `skills/ICG-Renaming/scripts/src/` |

## What was copied

- `src/` (all 7 Python modules): `renaming_engine.py`, `context_engine.py`, `vision_engine.py`, `security.py`, `knowledge_manager.py`, `cli.py`, `director.py`
- `requirements.txt` → `scripts/requirements.txt`
- Root `SKILL.md` → adapted as `SKILL.md` with vendor header + MyLaprak path updates

## What was NOT copied

- `tests/` — upstream tests remain only in the upstream repo. To run the full suite locally, copy `tests/` from upstream into `scripts/tests/`.
- `.git/`, `.github/`, `examples/`, `docs/`, `workspace/` — not needed for skill operation.
- `pyproject.toml`, `setup.cfg` — only `requirements.txt` is needed.

## Sync procedure (when upstream changes)

```bash
# 1. Pull latest upstream
cd /c/laragon/www/ImageContext-Generator && git pull

# 2. Re-copy engine files into MyLaprak
cp src/*.py "C:/LAPORAN UGM/Semester 5/MyLaprak/skills/ICG-Renaming/scripts/src/"
cp requirements.txt "C:/LAPORAN UGM/Semester 5/MyLaprak/skills/ICG-Renaming/scripts/requirements.txt"

# 3. Update this file's "Vendored commit" field
cd /c/laragon/www/ImageContext-Generator && git rev-parse HEAD

# 4. Run tests and verify no regressions
# 5. Commit in MyLaprak only after ACC from Avin (GATE ACC)
```

## Contract guarantees

- **ACC gate**: `RenamingPlan.commit()` must only be called after explicit user approval. No writes to output dir before that.
- **Naming contract**: `1.png`, `1a.png`, `T1.png`, `T1-1.png` — do not change without updating downstream `make-laprak-info` skill.
- **Backward compatibility**: legacy free-form `inisiasi.txt` must remain readable by downstream tools.
- **No git operations** without ACC from Avin — this vendored copy is no exception.

## Known differences from upstream

- SKILL.md `name:` changed from upstream `icg-renaming-engine` to `icg-renaming` to match MyLaprak skill naming convention (mixed-case directory names).
- Added `Local Engine Location`, `Installation (Dependencies)`, and `Vendor Metadata` sections to SKILL.md.
- **`requirements.txt` extended**: `PyMuPDF>=1.23` (module `fitz`) and `python-pptx>=0.6` added — these are imported by the engine (`knowledge_manager.py`, `renaming_engine.py`) but absent from upstream `requirements.txt`. Both SKILL.md dependency lists were updated to match. This is required for PDF/PPTX step extraction to work from a clean `pip install -r`.
- Engine Python source files are byte-identical to the upstream **working tree snapshot @ 2026-11-24** (see "Source snapshot" above). They are **not** byte-identical to commit `32a81c1` alone — 3 modules are untracked and 4 are modified relative to that commit. No Python code was modified during vendoring.
