# CHANGELOG — MyLaprak

Semua perubahan signifikan didokumentasikan di sini. Format mengikuti [Keep a Changelog](https://keepachangelog.com/id/1.0.0/), versi mengikuti [SemVer](https://semver.org/lang/id/).

---

## [0.4.0] — 2026-11-24

### ✨ Baru (F4: Vendor ICG Skills)
- **Skill `icg-renaming` di-vendor** — Engine Python F1 (extract steps, vision classify, dedup hash+perceptual, canonical naming `1.png`/`1a.png`/`T1.png`, ACC-gated commit) disalin self-contained ke `skills/icg-renaming/scripts/`. SKILL.md + `VENDOR.md` (provenance & sync).
- **Skill `icg-contextgenerate` di-vendor** — Engine Python F2 (two-pass visual census + enriched context, pending store auto-save/resume, `AccRequiredError` gate) disalin self-contained ke `skills/icg-contextgenerate/scripts/`. SKILL.md + `VENDOR.md` (provenance & sync).
- **Cross-citation docs** — `README.md` menautkan repo ICG + menjelaskan posisi ICG sebagai hulu, alur 4 skill diperbarui, struktur folder diperluas. Engine upstream tetap di [ImageContext-Generator](https://github.com/AcademyCity-RND/ImageContext-Generator) (vendored from upstream **working tree @ 2026-11-24**: base commit `32a81c1d` + R4/R5 fixes; 3 modules untracked, 4 modified), source-of-truth pengembangan tetap di sana.
- **Backward compat dipertahankan** — `inisiasi.txt` legacy (free-form) tetap didukung penuh; enriched format tidak mengubah kontrak V17.

### 📦 Internal
- Versi plugin `plugin.json` naik ke `0.4.0`.
- File engine Python identik dengan upstream **working tree @ 2026-11-24** (base `32a81c1d` + R4/R5 fixes; tanpa modifikasi kode saat vendoring) — bukan identik dengan commit `32a81c1d` saja (3 module untracked, 4 modified). Hanya SKILL.md yang disesuaikan (nama skill + path lokal + vendor header). `requirements.txt` kedua skill ditambah `PyMuPDF` + `python-pptx` yang di-import engine namun absen di upstream.

---

## [0.3.0] — 2026-11-23

### ✨ Baru (F3: MyLaprak Rework)
- **Folder kerja `_contoh/`** — Minimal 1 file `.tex` laporan riil dianonimkan di folder kerja user, dibaca `/breakdown-matkul` untuk membangun gaya matkul.
- **Gaya matkul lokal (`matkul/`)** — Hasil `/breakdown-matkul` ditulis ke `skills/make-laprak/matkul/<NAMA>/` **di mesin user**. Folder ini di-gitignore (hanya `.gitkeep` + `README.md` yang ter-clone). Clone bersih = Mode Universal aktif.
- **Parser `inisiasi.txt` Dual-Mode (Enriched + Legacy):**
  - *Enriched:* `[@section] S<n> | <judul>` + `N.png | S<n> | type=<T> | group=<single|pair:M> | <Label> | Konteks: ... | Arah: ...`
  - *Legacy:* `N.png | Label | Konteks | Arah` (kompatibel penuh, tidak breaking change)
  - Deteksi otomatis format, validasi simetri `group=pair:M` (warn + tanya user, bukan auto-fix).
  - Dukungan nama file: `N.png`, `Na.png`, `TN.png`, `TN-Na.png`, komentar `#`.
- **Lebar gambar dari `type`→width tabel** — Di `general.md` (dan override-able di `matkul/<NAMA>.md`). Menghilangkan angka bebas tidak konsisten.
- **Dual-Mode eksplisit di `/make-laprak`:**
  - **Mode A (Lokal):** `matkul/<NAMA>/` ada → pakai pedoman user.
  - **Mode B (General Fallback):** Selalu tersedia via `template-general/`.
- **Dukungan sitasi ICG (F4 vendor)** — Format `ICG:xxx` (kode) dan `ICG:ctx:xxx` (konteks) dikenali di parser.
- **Dokumentasi v0.3.0 penuh** — `README.md`, `CONTRIBUTING.md`, `skills/*/SKILL.md` (make-laprak, breakdown-matkul, make-laprak-info) diupdate.

### 🛠️ Diperbaiki
- `.gitignore` diperluas: `matkul/*` ignore + `!.gitkeep` + `!README.md`, plus safety net `gambar_raw/`, `gambar/`, `unmatched/`, `_contoh/`, `.icg_cache/`, `inisiai.txt`.
- File matkul lama (`KEPL/`, `PPD/`, `PPG/`) dihapus dari index Git (`git rm --cached`), kini hanya folder kosong + panduan yang ter-clone.

### 📦 Internal
- 3 skill (`make-laprak`, `breakdown-matkul`, `make-laprak-info`) version bump ke `0.3.0`.
- `template-general/general.md` **dipertahankan** perubahan V7 `type`→width table (dari R1-FIX attempt run-14).

---

## [0.2.0] — 2026-11-??
### ✨ Baru
- Sistem Template Universal (`template-general/`) dengan `general.md` + `template-master.tex` + komponen pecahan.
- Template monolitik aman privasi: `template-KEPL.tex`, `template-PPD.tex`, `template-PPG.tex`.
- Otomatisasi GitHub Releases & Auto-Changelog via GitHub Actions.
- Skill `breakdown-matkul` (ekstraksi `.tex` contoh → `.md` + template).
- Skill `make-laprak-info` (panduan verbatim).

---

## [0.1.0] — 2026-11-??
### ✨ Rilis Awal
- Plugin Antigravity `make-laprak` dengan alur 5 tahap (Inisiasi → Outline → Hasil & Pembahasan → Dasar Teori → Finalisasi).
- Dukungan mata kuliah: KEPL, PPD, PPG (di `matkul/` — kini dipindahkan ke lokal user).
- Parser `inisiasi.txt` legacy (`N.png | Label | Konteks | Arah`).
- Auto-generate `.tex` fisik di folder kerja user.