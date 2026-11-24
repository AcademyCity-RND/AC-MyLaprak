# CHANGELOG — MyLaprak

Semua perubahan signifikan didokumentasikan di sini. File ini di-generate otomatis
oleh [git-cliff](https://github.com/orhun/git-cliff) dari Conventional Commits.
Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.0.0/),
versi mengikuti [SemVer](https://semver.org/lang/id/).

---
## [1.1.0] — 2026-11-24

### ✨ Baru
- **skills:** Vendor ICG renaming + context engines- **release:** Git-cliff auto versioning + release workflow

### 📝 Dokumentasi
- Sync skill docs with lowercase ICG names + ecosystem

### 📦 Internal
- **privacy:** Untrack course matkul, ignore local working dirs
## [1.0.1] — 2026-11-23

### ✨ Baru
- Hermes-compatible skills + CI workflows (ci, health-check, pr-lint, release-please)

### 🛠️ Diperbaiki
- **ci:** Use valid semantic-PR inputs (requireScope)- **ci:** Valid job outputs for release-please; sync manifest to v1.0.0 (#28)- **ci:** Use proven tag-based release workflow with auto-changelog (#29)
## [1.0.0] — 2026-11-04

### ✨ Baru
- Add /laprak command trigger- Add make-laprak-info skill- Enforce web search for 100% accurate external references- **make-laprak:** Extract KEPL guideline and clarify folder workflow- **make-laprak:** Force direct generation of .tex file in TAHAP 4- **make-laprak:** Enrich KEPL.md with KEPL2.tex styling insights- **v2:** Complete overhaul — portable path resolution, KEPL3 breakdown, anti-ngide rules, docs sync- Add breakdown-matkul skill for .tex to .md extraction- Split Tahap 3 into 3a (Hasil) and 3b (Dasar Teori) with separate ACC checkpoints- Add matkul PPG with 3 .tex references and breakdown .md- **release:** V1 release with universal template-general and course templates- **ci:** Add GitHub Releases Auto-Changelog workflow and update documentation

### 📝 Dokumentasi
- Make the prompt example complete and clear without trailing dots- Add roadmap and checklist for universal AI support- **make-laprak-info:** Sync generation logic- Add CONTRIBUTING.md with matkul template and contribution guide

### 📦 Internal
- Refine skill paths and add .gitignore- **privacy:** Remove real student reference reports in favor of placeholder templates

### 🔒 Lainnya
- Refine skill drafting logic and update README

### 🛠️ Diperbaiki
- Rename skill to make-laprak to match the desired slash command- **make-laprak:** Clarify plugin path for specific template reference- **make-laprak:** Instruct AI to dynamically find absolute plugin path- **make-laprak:** Hardcode windows absolute path to avoid view_file errors- **make-laprak-info:** Use exact output text instead of letting AI paraphrase

