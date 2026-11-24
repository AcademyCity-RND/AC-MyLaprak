# Panduan Uji Coba Mandiri — Alur 4 Command MyLaprak + ICG

Panduan ini untuk teman yang mau mencoba sendiri alur:

```
/make-laprak-info  →  /ICG-Renaming  →  /ICG-ContextGenerate  →  /breakdown-matkul  →  /make-laprak
```

Estimasi: 30–45 menit (tergantung jumlah screenshot dan kuota Gemini).

---

## 0. Yang disiapkan dulu

- Komputer dengan **Git** dan **Python 3.12** (`py -3.12 --version` / `python3.12 --version`).
- Agent AI: **Antigravity** **atau** **Hermes** (boleh dua-duanya kalau mau bandingkan).
- **Kunci API Gemini** (Google AI Studio → *Get API key*). Pakai key uji coba, jangan pakai key produksi.
- Data uji coba (boleh dummy):
  - 5–10 screenshot praktikum (PNG) yang urutannya masih berantakan.
  - 1 file referensi modul/slide (`.pdf` atau `.pptx`) yang berisi daftar langkah praktikum.
  - 1 file template `_contoh/<nama>.tex` (boleh sangat sederhana) dengan placeholder gambar.

> Jangan pakai data asli/nilai asli untuk uji coba. Jangan pernah kirim API key di laporan bug.

---

## 1. Pasang skill

### Opsi A — Antigravity

```bash
# Global
git clone https://github.com/AcademyCity-RND/AC-MyLaprak.git ~/.gemini/config/plugins/make-laprak

# Atau per-workspace
mkdir -p .agents/plugins
git clone https://github.com/AcademyCity-RND/AC-MyLaprak.git .agents/plugins/make-laprak
```

Buka agent di workspace itu. Kelima skill ada di folder `skills/`.

### Opsi B — Hermes

Salin isi folder `skills/` ke direktori skill Hermes:

```bash
# macOS/Linux
cp -r skills/* ~/.hermes/skills/productivity/        # make-laprak, make-laprak-info, breakdown-matkul
cp -r skills/icg-* ~/.hermes/skills/software-development/

# Windows (Git Bash)
cp -r skills/make-laprak* "$LOCALAPPDATA/hermes/skills/productivity/"
cp -r skills/breakdown-matkul "$LOCALAPPDATA/hermes/skills/productivity/"
cp -r skills/icg-renaming skills/icg-contextgenerate "$LOCALAPPDATA/hermes/skills/software-development/"
```

Mulai ulang Hermes, lalu cek dengan `/skills` — harus muncul 5 skill:
`make-laprak`, `make-laprak-info`, `breakdown-matkul`, `icg-renaming`, `icg-contextgenerate`.

Repo **ImageContext-Generator tidak perlu di-clone** — engine-nya sudah di-vendor di dalam `skills/icg-*/scripts/`.

---

## 2. Pasang dependensi Python + API key

Jalankan dari root repo/plugins:

```bash
py -3.12 -m pip install -r skills/icg-renaming/scripts/requirements.txt
py -3.12 -m pip install -r skills/icg-contextgenerate/scripts/requirements.txt
```

Isi dependensi: `google-genai`, `pillow`, `typer`, `rich`, `pyyaml`, `python-dotenv`.

Set env var (nama variabelnya **`GOOGLE_API_KEY`**, bukan `GEMINI_API_KEY`):

```bash
# macOS/Linux
export GOOGLE_API_KEY="kunci_dari_ai_studio"

# Windows PowerShell
$env:GOOGLE_API_KEY="kunci_dari_ai_studio"
```

Kalau mau pakai CLI langsung (bukan lewat agent), boleh juga taruh di
`skills/icg-renaming/scripts/.env` dan `skills/icg-contextgenerate/scripts/.env`:

```
GOOGLE_API_KEY=kunci_dari_ai_studio
```

Cek cepat:

```bash
cd skills/icg-renaming/scripts
py -3.12 -c "from src.vision_engine import VisionEngine; from src.security import resolve_under_root; print('import OK')"
```

Harus keluar `import OK`.

---

## 3. Siapkan workspace uji coba

Buat struktur ini di folder kerja (boleh di mana saja):

```
workspace/
└── KEPL/
    ├── screenshots/
    │   └── Per4/            ← screenshot dummy (.png), urutan bebas
    ├── reference/           ← PDF/PPTX modul praktikum
    └── inisiasi/            ← kosong; output nanti ditaruh di sini
_contoh/
└── contoh.tex               ← template LaTeX dengan placeholder gambar
```

Kalau punya `inisiasi.txt` lama (format teks biasa), taruh di workspace juga — skill pendukung legacy tetap bisa membacanya.

---

## 4. Jalankan 4 command berurutan

### ① `/make-laprak-info`

Tanyakan: *"Cek kesiapan skill dan jelaskan format `_contoh` serta format `inisiasi.txt` yang dibutuhkan."*

✅ **Expect:** penjelasan format enriched + legacy, tidak ada error "skill not supported".

### ② `/ICG-Renaming`

Prompt contoh:

> Rename screenshot di `workspace/KEPL/screenshots/Per4` pakai referensi `workspace/KEPL/reference/`. Tampilkan rencana renaming dulu, minta ACC sebelum menulis hasil ke `workspace/KEPL/gambar/Per4`.

✅ **Expect:** tabel rencana (Source → Final Name, step, confidence), lalu **diminta konfirmasi**. Jangan approve kalau tidak mau menimpa. Cek hasil di `gambar/Per4/` (nama seperti `1.png`, `1a.png`, `T1.png`).

### ③ `/ICG-ContextGenerate`

Prompt contoh:

> Dari screenshot hasil rename di `workspace/KEPL/gambar/Per4`, buat `inisiasi.txt` enriched. Lakukan visual census dulu, kelompokkan per `@section`, tandai `type=` dan `group=pair:` kalau ada pasangan gambar. Tulis file pending dulu, minta ACC sebelum menulis final.

✅ **Expect:** ada ringkasan sections/order/pairs, lalu file pending di `.icg_cache/pending_inisiasi.txt`, lalu konfirmasi ACC, baru `workspace/KEPL/inisiasi/Per4.txt` berisi marker `[@section]`, `type=`, `group=`.

### ④ `/breakdown-matkul`

Prompt contoh:

> Parse `workspace/KEPL/inisiasi/Per4.txt` jadi matriks keilmuan: Kajian, Pembahasan, Analisis.

✅ **Expect:** tiga bagian matriks terisi, bukan cuma copy-paste inisiasi.

### ⑤ `/make-laprak`

Prompt contoh:

> Susun laporan LaTeX dari `_contoh/contoh.tex` + matriks + inisiasi tadi. Pakai gaya matkul lokal dan tautkan gambar dari `gambar/Per4`.

✅ **Expect:** file `.tex` baru dengan struktur lengkap dan path gambar valid.

---

## 5. Kalau mau coba lewat CLI (opsional)

CLI ada di dalam folder skill, sedangkan `--workspace` dihitung relatif terhadap folder tempat Anda menjalankan perintah. Jadi jalankan dari folder induk `workspace/` dan tambahkan `PYTHONPATH`:

```bash
# dari folder induk workspace/
export PYTHONPATH="$PWD/<path-ke-plugin>/skills/icg-renaming/scripts"   # Windows: set PYTHONPATH=...

py -3.12 -m src.cli rename -c kepl -p Per4 -w workspace -r KEPL/reference
```

Perintah akan menampilkan tabel rencana lalu meminta konfirmasi (`y/N`) sebelum menulis ke `workspace/KEPL/gambar/Per4/`.

Untuk generate context:

```bash
export PYTHONPATH="$PWD/<path-ke-plugin>/skills/icg-contextgenerate/scripts"
py -3.12 -m src.cli generate-context -c kepl -p Per4 -w workspace \
    --module-summary "Praktikum KEPL Per4" \
    --course-context "Mata kuliah Konstruksi dan Evolusi Perangkat Lunak"
```

Catatan: `generate-context` lewat CLI membaca dari `workspace/<KODE>/screenshots/<Pertemuan>`, sedangkan `rename` menulis ke `workspace/<KODE>/gambar/<Pertemuan>`. Kalau memakai CLI berurutan, salin dulu hasil `gambar/` ke `screenshots/` (atau biarkan agent yang menangani lewat skill).

---

## 6. Cara lapor bug

Kirimkan:

- OS + platform (Antigravity / Hermes) + versi Python.
- Tag/plugin version (mis. `v1.1.6`) dan commit hash kalau tahu.
- Command ke-berapa yang gagal (①–⑤).
- Langkah persis untuk mengulang.
- **Expected vs actual**.
- Log/error (API key **wajib** disensor), plus screenshot kalau perlu.

Kirim ke: https://github.com/AcademyCity-RND/AC-MyLaprak/issues

---

## 7. Batasan yang sudah diketahui

- Test symlink (`SEC-04`) ter-skip di Windows tanpa hak admin — bukan bug alur.
- Tanpa `GOOGLE_API_KEY`, command ② dan ③ tidak bisa jalan; ①, ④, ⑤ masih bisa diuji dengan `inisiasi.txt` legacy.
- Pemanggilan slash-command persis di Antigravity belum diuji dari sisi Antigravity — kalau command tidak dikenali, sebutkan explicit di prompt: *"pakai skill `icg-renaming` …"*.
- Salinan skill di Hermes adalah **vendored**. Kalau ICG upstream berubah, `scripts/` harus di-sync ulang dari repo.
