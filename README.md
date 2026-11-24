# MyLaprak — Antigravity / Hermes Skill Plugin

Repositori ini menyediakan _Skill_ AI untuk menyusun **Laporan Praktikum universitas** secara interaktif, terstruktur, analitis, dan siap pakai dalam format **LaTeX**. Versi **v0.4.0** memperkenalkan **skill ICG di-vendor** (Renaming + ContextGenerate) serta **dukungan alur penuh bersama ImageContext-Generator (ICG)**. Fitur v0.3.0 yang dibawa ke depan: folder kerja `_contoh/`, parser `inisiasi.txt` dual-mode (enriched + legacy), gaya matkul **lokal milik user**, sistem template Universal.

---

## 🌟 Fitur Unggulan (v0.4.0)

- 🧩 **ICG Skills di-Vendor (BARU v0.4.0):**
  - **`/icg-renaming`** — membersihkan, mengurutkan, dan menamai screenshot mengikuti struktur modul (PDF/PPTX) → `gambar/` (`1.png`, `1a.png`, `T1.png`, …). Dedup hash + perceptual hash, ACC gate sebelum write.
  - **`/icg-contextgenerate`** — dua-pass (visual census → enriched context) menghasilkan `inisiasi.txt` enriched dengan `[@section]`, `type=`, `group=`, `Konteks:`, `Arah:`. Auto-save/resume via `.icg_cache`, ACC gate pending→final.
  - Engine Python **self-contained** di `skills/ICG-Renaming/scripts/` dan `skills/ICG-ContextGenerate/scripts/`. Sumber pengembangan tetap di repo ICG (lihat `VENDOR.md` tiap skill).
  - Kompatibel penuh dengan `inisiasi.txt` legacy (free-form) — backward compat dijamin.

- 🌐 **Dual-Mode yang Jujur:**
  - **Mode A — Gaya Matkul Lokal:** Pedoman `matkul/<NAMA>/` **dibuat dan disimpan di mesin Anda** lewat `/breakdown-matkul`. Folder ini sengaja **kosong di repo publik** (hanya `.gitkeep` + README) agar tidak ada gaya/data pribadi yang ikut ter-clone.
  - **Mode B — General Fallback:** Selalu tersedia via `template-general/` (`general.md` + `template-master.tex` + komponen pecahan). Clone bersih = Mode B langsung pakai.
- 📖 **Parser `inisiasi.txt` Dual-Mode:**
  - **Enriched:** `[@section] S<n> | <judul>` + `N.png | S<n> | type=<...> | group=<single|pair:M> | <Label> | Konteks: ... | Arah: ...`
  - **Legacy:** `N.png | Label | Konteks | Arah` (dan catatan bebas per baris) — **tetap didukung penuh**.
  - Deteksi otomatis, validasi simetri `group=pair:M`, dukungan nama file `N.png`, `Na.png`, `TN.png`, `TN-Na.png`.
- 📏 **Width dari `type`:** Lebar gambar diambil dari tabel `type`→width di `general.md` (atau override `matkul/<NAMA>.md`). Tidak lagi angka bebas yang tidak konsisten.
- 🛡️ **Privacy-Safe Architecture:** Tidak ada laporan riil di repo. Contoh masuk `_contoh/` (folder kerja user), hasil breakdown masuk `matkul/` lokal yang di-gitignore.
- 🔍 **Sitasi Nyata + ICG:** Verifikasi referensi via modul/web; jika skill ICG tersedia (F4 vendor), sitasi `ICG:xxx` (kode) dan `ICG:ctx:xxx` (konteks) dikenali.
- ⚡ **Auto-Generate `.tex`:** Langsung menulis berkas `.tex` fisik di folder kerja Anda pada tahap finalisasi.

---

## 📦 Cara Instalasi Plugin

### Opsi A — GitHub Releases (paling mudah)
1. Buka tab **[Releases](https://github.com/AcademyCity-RND/MyLaprak/releases)**.
2. Unduh bundle `MyLaprak-vX.X.X.zip` terbaru.
3. Ekstrak ke direktori plugin: `~/.gemini/config/plugins/make-laprak` (Antigravity) atau folder skills Hermes Anda.

### Opsi B — Git Clone
```bash
# Global
git clone https://github.com/AcademyCity-RND/MyLaprak.git ~/.gemini/config/plugins/make-laprak

# Per-workspace
mkdir -p .agents/plugins/
git clone https://github.com/AcademyCity-RND/MyLaprak.git .agents/plugins/make-laprak
```

> Clone bersih hanya berisi `template-general/` dan `matkul/.gitkeep` + README. Itu **disengaja**.

---

## 📂 Struktur Folder Plugin

```text
MyLaprak/
├── .github/
│   ├── release.yml                       # Auto-Changelog rilis
│   └── workflows/release.yml             # Build bundle zip + release
├── plugin.json                           # Manifest plugin
├── README.md                             # Dokumentasi utama (ini)
├── CONTRIBUTING.md                       # Panduan kontribusi
├── CHANGELOG.md                          # Riwayat versi (v0.4.0)
├── scripts/                              # Skrip utilitas pengembang
└── skills/
    ├── make-laprak/
    │   ├── SKILL.md                      # Alur 5 tahap + parser enriched/legacy
    │   ├── matkul/                       # LOKAL USER — di-gitignore
    │   │   ├── .gitkeep                 # Penanda folder tetap ada di clone
    │   │   ├── README.md                # Cara membuat gaya sendiri
    │   │   └── <NAMA>/                  # Hasil /breakdown-matkul user
    │   │       ├── <NAMA>.md            # Pedoman formatting
    │   │       └── template-<NAMA>.tex  # Template placeholder
    │   └── template-general/            # Fallback universal (selalu ada)
    │       ├── general.md               # Pedoman + tabel type→width
    │       ├── template-master.tex
    │       ├── template-dependencies-dan-style.tex
    │       ├── template-tujuanpraktikum.tex
    │       ├── template-dasarteori.tex
    │       ├── template-hasilpembahasan.tex
    │       ├── template-kesimpulan.tex
    │       └── template-daftarpustaka.tex
    ├── breakdown-matkul/
    │   └── SKILL.md                      # _contoh/*.tex → matkul/<NAMA>/ (lokal)
    ├── make-laprak-info/
    │   └── SKILL.md                      # Panduan verbatim (v0.4.0)
    ├── ICG-Renaming/                     # BARU v0.4.0 (vendored dari ICG)
    │   ├── SKILL.md
    │   └── scripts/                      # Engine Python self-contained
    │       ├── src/                      # 7 modul: renaming_engine, vision_engine, security, ...
    │       ├── requirements.txt
    │       └── VENDOR.md                 # Provenance + sync procedure
    └── ICG-ContextGenerate/              # BARU v0.4.0 (vendored dari ICG)
        ├── SKILL.md
        └── scripts/                      # Engine Python self-contained
            ├── src/                      # 7 modul: context_engine, vision_engine, security, ...
            ├── requirements.txt
            └── VENDOR.md                 # Provenance + sync procedure
```

---

## 🔗 Alur Penuh 4 Skill (dengan ICG — **sudah di-vendor v0.4.0**)

```text
Screenshot mentah
   │
   ├─(1) /icg-renaming ──────────► gambar/ bernomor rapi (1.png, 2.png, T1.png, ...)
   │
   ├─(2) /icg-contextgenerate ───► inisiasi.txt ENRICHED
   │                                ([@section] + type/group/Konteks/Arah)
   │
   ├─(3) /breakdown-matkul ──────► matkul/<NAMA>/ (LOKAL, dari _contoh/*.tex)
   │
   └─(4) /make-laprak ───────────► Laporan.tex siap kompilasi
```

Skill ICG kini **di-vendor (termasuk di repo ini)** sejak **F4 v0.4.0**. Engine Python self-contained di `skills/ICG-Renaming/scripts/` dan `skills/ICG-ContextGenerate/scripts/`. Sumber pengembangan (upstream) tetap di repo ICG: [github.com/AcademyCity-RND/ImageContext-Generator](https://github.com/AcademyCity-RND/ImageContext-Generator) — lihat `VENDOR.md` di setiap skill untuk provenance & sync procedure.

Repositori ICG: [github.com/AcademyCity-RND/ImageContext-Generator](https://github.com/AcademyCity-RND/ImageContext-Generator)

---

## 🚀 Cara Menggunakan

> **PENTING:** Anda **TIDAK PERLU** menaruh file tugas di dalam folder plugin.

### Langkah 1 — Siapkan Folder Kerja
Buat folder kerja pertemuan di mana saja, mis. `D:\Tugas\PPD\Pertemuan-5\`.

### Langkah 2 — Isi Folder Kerja
- `inisiasi.txt` — enriched **atau** legacy (lihat §Format Inisiasi).
- `gambar/` — screenshot bernomor (`1.png`, `2.png`, `T1.png`, `Na.png`, `TN-Na.png`, ...).
- `_contoh/` — **minimal satu** `.tex` laporan yang sudah disetujui & dianonimkan (dipakai `/breakdown-matkul`).
- (Opsional) modul praktikum (PDF/PPT).

### Langkah 3 — Panggil AI
```text
/make-laprak buatkan laporan [NAMA_MATKUL], saya sudah siapkan inisiasi.txt, gambar/, dan _contoh/
```
Jika `matkul/<NAMA>/` belum ada → Mode B, AI menanyakan identitas (Nama, NIM, Kelas, Dosen, Topik) di Tahap 1.

### Langkah 4 — Alur 5 Tahap (ACC setiap tahap)
1. **Inisiasi** — baca pedoman + parsing `inisiasi.txt`, validasi pair, rangkum.
2. **Outline** — dari `[@section]` (enriched) atau disusun dari nol (legacy).
3. **3a Hasil & Pembahasan** — `group=pair` → Gaya B; `single` → Gaya C; width dari `type`.
4. **3b Dasar Teori** — dilewati jika matkul tanpa teori.
5. **4 Finalisasi** — Kesimpulan + Daftar Pustaka, lalu **langsung generate `.tex`**.

---

## 📝 Format `inisiasi.txt`

**Enriched (disarankan):**
```text
[@section] S1 | Pendahuluan
1.png | S1 | type=code | group=single | Kode Utama | Konteks: ... | Arah: ...
2.png | S1 | type=terminal | group=pair:3 | Output Program | Konteks: ... | Arah: ...
3.png | S1 | type=gui | group=pair:2 | Grafik Hasil | Konteks: ... | Arah: ...
# baris komentar diabaikan
```

**Legacy (kompatibel penuh):**
```text
1.png | Label Gambar | Konteks penjelasan | Arah analisis
2.png | Output Program | Konteks ... | Arah ...
```

| Field | Arti |
|-------|------|
| `S<n>` | ID section dari header `[@section]` |
| `type` | Dipetakan ke lebar gambar di tabel `general.md` — 6 nilai kanonik V7: `config`, `code`, `terminal`, `gui`, `diagram`, `log` |
| `group=single` | Gaya C — 1 gambar per `figure` |
| `group=pair:M` | Gaya B — 2 gambar + `\vspace`; **simetri wajib** |
| `Konteks` / `Arah` | Bahan narasi analitis, bukan sekadar caption |

---

## 🎨 Membuat Gaya Matkul Sendiri (Mode A)

1. Taruh laporan contoh yang sudah dianonimkan di `_contoh/`.
2. Jalankan `/breakdown-matkul` → hasil ditulis ke `skills/make-laprak/matkul/<NAMA>/` **di mesin Anda**.
3. Panggil `/make-laprak` → gaya lokal dipakai otomatis.

Folder `matkul/` diabaikan Git. Jangan pernah commit laporan riil. Ingin berbagi? Bagikan `_contoh/` yang dianonimkan lewat issue/PR, lalu orang lain menjalankan `/breakdown-matkul` sendiri.

---

## 👥 Kontributor (Co-Author) Otomatis

- **Windows:** `scripts/setup-contributor.bat`
- **Linux/Mac:** `bash scripts/setup-contributor.sh`

## ℹ️ Bantuan Cepat
Ketik `/make-laprak-info` untuk panduan verbatim v0.4.0.

---

## 🗺️ Roadmap

- [x] Sistem Template Universal (`template-general/`)
- [x] Template monolitik aman privasi
- [x] Otomatisasi GitHub Releases
- [x] **v0.3.0 — `matkul/` lokal + `_contoh/` + parser enriched/legacy + `type`→width + docs**
- [x] **F4 — vendor skill ICG (Renaming + ContextGenerate) ke repo ini** ✅
- [ ] Cross-Platform Adapters (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`)
- [ ] Fallback script pencari jurnal (`scripts/search_jurnal.py`)
- [ ] Integrasi MCP pencarian pustaka akademik

Lihat [CHANGELOG.md](CHANGELOG.md) untuk rincian perubahan versi.