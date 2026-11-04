# MyLaprak - Antigravity Plugin

Repositori ini adalah **Plugin Antigravity** yang menyediakan _Skill_ AI khusus untuk menyusun Laporan Praktikum tingkat Universitas secara interaktif, terstruktur, analitis, dan siap pakai dalam format LaTeX.

---

## 🌟 Fitur Unggulan (Rilis V1)

- 🌐 **Dukungan Dual-Mode:**
  - **Mode Matkul Terdaftar:** Menggunakan aturan penulisan dan template spesifik mata kuliah (`KEPL`, `PPD`, `PPG`).
  - **Mode Universal (General Fallback):** Mampu menyusun laporan untuk mata kuliah praktikum **apa pun** secara instan menggunakan basis `template-general/` dengan panduan `general.md`.
- 🛡️ **Privacy-Safe Architecture:** Menggunakan template acuan monolitik ber-placeholder (`template-[MATKUL].tex`) tanpa mengekspos data pribadi mahasiswa di repositori publik.
- 📖 **Peta Kerja Otomatis:** Membaca catatan alur kerja di `inisiasi.txt` dan mencocokkannya dengan screenshot bernomor di folder `gambar/`.
- 🔍 **Sitasi Ilmiah Nyata:** AI mencari dan memvalidasi sumber referensi asli (buku, jurnal IEEE ber-DOI, modul dosen) tanpa halusinasi sitasi.
- ⚡ **Auto-Generate Berkas Fisik `.tex`:** Langsung menghasilkan berkas `.tex` siap kompilasi di folder kerja pengguna pada tahap finalisasi.

---

## 📦 Cara Instalasi Plugin

Pilih salah satu cara instalasi berikut:

### Opsi A — Download via GitHub Releases (Paling Mudah)
1. Buka tab **[Releases](https://github.com/AcademyCity-RND/MyLaprak/releases)** di repositori ini.
2. Unduh berkas bundle rilis terbaru (`MyLaprak-vX.X.X.zip`).
3. Ekstrak isi berkas zip langsung ke direktori plugin Antigravity Anda (`~/.gemini/config/plugins/make-laprak`).

### Opsi B — Kloning Repositori (Git Clone)
**Instalasi Global (berlaku untuk semua workspace):**
```bash
git clone https://github.com/AcademyCity-RND/MyLaprak.git ~/.gemini/config/plugins/make-laprak
```

**Instalasi Lokal (per workspace proyek):**
```bash
mkdir -p .agents/plugins/
git clone https://github.com/AcademyCity-RND/MyLaprak.git .agents/plugins/make-laprak
```

---

## 📂 Struktur Folder Plugin

```text
MyLaprak/
├── .github/
│   ├── release.yml                          # Konfigurasi Auto-Changelog rilis
│   └── workflows/
│       └── release.yml                      # CI/CD otomatisasi rilis & bundle zip
├── plugin.json                              # Manifest metadata plugin Antigravity
├── README.md                                # Dokumentasi utama repositori
├── CONTRIBUTING.md                          # Panduan berkontribusi
├── scripts/                                 # Skrip utilitas pengembang
└── skills/
    ├── make-laprak/                         # Skill utama — penyusun laporan
    │   ├── SKILL.md                         # Prompt instruksi alur kerja (Workflow)
    │   ├── matkul/                          # Koleksi pedoman & template per matkul
    │   │   ├── KEPL/                        # Konstruksi & Evolusi Perangkat Lunak
    │   │   │   ├── KEPL.md                  # Pedoman penulisan & gaya naratif
    │   │   │   └── template-KEPL.tex        # Template monolitik acuan KEPL
    │   │   ├── PPD/                         # Praktikum Penambangan Data
    │   │   │   ├── PPD.md                   # Pedoman penulisan, formula & grafik
    │   │   │   └── template-PPD.tex         # Template monolitik acuan PPD (Cover UGM)
    │   │   └── PPG/                         # Pemrograman Permainan (Game)
    │   │       ├── PPG.md                   # Pedoman format khusus tanpa Teori/Kesimpulan
    │   │       └── template-PPG.tex         # Template monolitik acuan PPG
    │   └── template-general/                # Sistem Template Universal (Fallback)
    │       ├── general.md                   # Pedoman umum untuk matkul baru
    │       ├── template-master.tex          # Master template monolitik universal
    │       ├── template-dependencies-dan-style.tex
    │       ├── template-tujuanpraktikum.tex
    │       ├── template-dasarteori.tex
    │       ├── template-hasilpembahasan.tex
    │       ├── template-kesimpulan.tex
    │       └── template-daftarpustaka.tex
    ├── breakdown-matkul/                    # Skill ekstraksi .tex contoh → .md & template
    │   └── SKILL.md
    └── make-laprak-info/                    # Skill bantuan & panduan cepat
        └── SKILL.md
```

---

## 🚀 Cara Menggunakan

> **PENTING:** Anda **TIDAK PERLU** menaruh file tugas di dalam folder plugin ini. Plugin bertindak sebagai "otak" di latar belakang.

### Langkah 1 — Siapkan Folder Kerja
Buat folder kerja pertemuan **di mana saja** (misal: `D:\Tugas\PPD\Pertemuan-5\` atau `D:\Tugas\JaringanKomputer\Pertemuan-1\`).

### Langkah 2 — Isi Folder Kerja
Di dalam folder kerja tersebut, siapkan:
- `inisiasi.txt` — Catatan/peta penjelasan Anda tentang setiap screenshot langkah praktikum.
- Folder `gambar/` — Screenshot bernomor (misal: `1.png`, `2.png`, `T1.png`, dst).
- (Opsional) Berkas modul praktikum (PDF/PPT/Word) pertemuan terkait.

### Langkah 3 — Panggil AI
Buka workspace di folder kerja tersebut, lalu jalankan perintah di chat:
```text
/make-laprak buatkan laporan [NAMA_MATKUL], saya sudah siapkan inisiasi.txt dan folder gambar
```
*(Jika mata kuliah belum terdaftar di `matkul/`, AI akan otomatis menggunakan template universal dan menanyakan identitas Anda di awal).*

### Langkah 4 — Ikuti Alur Kerja 5 Tahap
AI bekerja secara iteratif dan selalu meminta persetujuan (ACC) Anda sebelum berpindah tahap:
1. **Tahap 1 — Inisiasi:** AI membaca referensi/template dan merangkum pemahaman (serta konfirmasi identitas jika mode universal).
2. **Tahap 2 — Outline:** AI menyusun kerangka bab dan sub-seksi laporan.
3. **Tahap 3a — Hasil dan Pembahasan:** AI menyusun draf pembahasan berdasarkan screenshot.
4. **Tahap 3b — Dasar Teori:** AI menyusun dasar teori relevan, formulasi matematis, dan diagram konsep.
5. **Tahap 4 — Finalisasi:** AI menyusun Kesimpulan dan Daftar Pustaka, lalu **langsung membuat file fisik `.tex`** siap kompilasi di folder Anda.

---

## 🎨 Menambahkan Mata Kuliah Baru Secara Permanen

Jika Anda memiliki mata kuliah baru dengan gaya penulisan khusus dan ingin menjadikannya standar permanen:
1. Buat folder baru di `skills/make-laprak/matkul/<NAMA_MATKUL>/`.
2. Letakkan file contoh laporan `.tex` di folder tersebut.
3. Jalankan perintah `/breakdown-matkul`. AI akan otomatis mengekstrak pola menjadi `<NAMA_MATKUL>.md` dan membuatkan `template-<NAMA_MATKUL>.tex`.

---

## 👥 Kontributor (Co-Author) Otomatis

Untuk memastikan kontribusi Anda tercatat rapi:
- **Windows:** Jalankan `scripts/setup-contributor.bat`
- **Linux/Mac:** Jalankan `bash scripts/setup-contributor.sh`

## ℹ️ Bantuan Cepat
Ketik `/make-laprak-info` di chat Antigravity untuk melihat panduan penggunaan langsung.

---

## 🗺️ Roadmap Proyek

- [x] Sistem Template Universal (`template-general/`) untuk segala matkul
- [x] Template monolitik acuan aman privasi (`template-KEPL`, `template-PPD`, `template-PPG`)
- [x] Otomatisasi GitHub Releases & Auto-Changelog via GitHub Actions
- [ ] Cross-Platform Adapters (`.cursorrules`, `CLAUDE.md`, `.github/copilot-instructions.md`)
- [ ] Fallback Script Pencari Jurnal Ilmiah Otomatis (`scripts/search_jurnal.py`)
- [ ] Integrasi MCP server untuk pencarian pustaka akademik
