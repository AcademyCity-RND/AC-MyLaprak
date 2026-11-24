# Panduan Kontribusi — MyLaprak (v0.4.0)

Terima kasih telah tertarik berkontribusi! Panduan ini menjelaskan cara menambahkan **gaya matkul baru** agar plugin `make-laprak` bisa menyesuaikan format laporan untuk mata kuliah Anda.

> **Sitasi silang:** Engine skill ICG (`icg-renaming`, `icg-contextgenerate`) di-vendor dari [ImageContext-Generator](https://github.com/AcademyCity-RND/AC-ImageContext-Generator). Sumber pengembangan (upstream) tetap di repo ICG — lihat `VENDOR.md` di masing-masing skill sebelum mengubah engine.

---

## 🎯 Filosofi v0.3.0: Gaya Matkul adalah Lokal, Bukan Di-Repo

Berbeda dengan versi sebelumnya, **Anda tidak perlu membuat PR ke repo ini untuk menambahkan gaya matkul**. Semua gaya matkul dibuat **di mesin Anda sendiri** lewat skill `/breakdown-matkul`.

**Alur singkat:**
1. Anda punya `_contoh/` berisi laporan `.tex` riil yang sudah dianonimkan.
2. Jalankan `/breakdown-matkul` → menghasilkan `matkul/<NAMA>/` **di folder plugin Anda**.
3. `/make-laprak` otomatis mendeteksi dan memakai gaya lokal tersebut.

Mengapa? Privasi & portabilitas. Clone bersih = hanya Mode Universal aktif. Setiap user punya gaya sendiri tanpa konflik di repo upstream.

---

## 📋 Cara Berkontribusi ke Repo Ini (Bukan Gaya Matkul)

Kontribusi ke repo ini berarti memperbaiki **core skill**, **template general**, **dokumentasi**, atau **tooling**.

### 1. Fork & Branch
```bash
git fork https://github.com/AcademyCity-RND/AC-MyLaprak
git checkout -b feat/<deskripsi-singkat>   # mis. feat/parser-validate-pair-symmetry
```

### 2. Apa yang Bisa Diubah
| File/Folder | Deskripsi | Catatan |
|-------------|-----------|---------|
| `skills/make-laprak/SKILL.md` | Alur kerja + parser enriched/legacy | PR butuh review ketat (workflow inti) |
| `skills/make-laprak/template-general/` | Universal fallback (general.md, *.tex) | **Tidak boleh mengubah `type`→width di `general.md` tanpa alasan kuat** (V7 = stabil) |
| `skills/breakdown-matkul/SKILL.md` | Ekstraksi `_contoh/` → `matkul/` lokal | |
| `skills/make-laprak-info/SKILL.md` | Panduan verbatim (v0.4.0) | Hanya update jika fitur core berubah |
| `skills/icg-renaming/SKILL.md` | ICG F1 Renaming Engine (vendored) | **Read-only** — engine di VENDOR.md upstream |
| `skills/icg-contextgenerate/SKILL.md` | ICG F2 ContextGenerate Engine (vendored) | **Read-only** — engine di VENDOR.md upstream |
| `README.md`, `CONTRIBUTING.md`, `CHANGELOG.md` | Dokumentasi | Bisa diubah bebas |
| `scripts/` | Tooling pengembang | |
| `.github/workflows/` | CI/CD | |

### 3. Apa yang **TIDAK** Dibolehkan di Repo
- ❌ Menambah folder `matkul/<NAMA>/` ke repo — **lokal user only**.
- ❌ Menyimpan file `.tex` contoh laporan riil di repo — **privacy risk**.
- ❌ Mengubah `general.md` tabel `type`→width (V7) tanpa dokumentasi perubahan di PR.

### 4. Commit & PR
```bash
git commit -m "feat(scope): deskripsi singkat"
git push origin feat/<deskripsi-singkat>
```
Buat PR ke branch `dev`. Tunggu review (reviewer = review only, tidak merge sendiri).

---

## 🛠️ Membuat Gaya Matkul Baru (Di Mesin Anda Sendiri)

Meskipun tidak ke repo, berikut langkah standar agar gaya Anda konsisten dengan ekosistem.

### Langkah 1 — Siapkan `_contoh/`
Di folder kerja Anda, buat folder `_contoh/` dan masukkan minimal 1 file `.tex` laporan yang sudah disetujui & **dianonimkan** (hapus nama, NIM, dosen, tanggal). Lebih banyak contoh = pola lebih presisi.

**Struktur file contoh:**
- Hanya body laporan (mulai `\chapter{...}` sampai `\end{thebibliography}`).
- Bukan preamble (`\documentclass`, `\usepackage`, dll).

### Langkah 2 — Jalankan Breakdown
Buka chat di workspace yang punya `_contoh/`, lalu:
```text
/breakdown-matkul
```
AI akan menganalisis pola dan menulis ke:
```
skills/make-laprak/matkul/<NAMA>/
├── <NAMA>.md              # Pedoman formatting (v0.3.0 enriched)
└── template-<NAMA>.tex    # Template placeholder
```

### Langkah 3 — Verifikasi & Iterasi
- Buka `<NAMA>.md` — cek apakah tabel `type`→width, gaya figure (A/B/C/D), struktur bab, dsb sudah sesuai.
- Jika perlu, edit manual `<NAMA>.md` (AI hanya ekstrak, Anda yang jamin).
- Tambahkan lebih banyak `.tex` ke `_contoh/` → jalankan `/breakdown-matkul` lagi → `.md` di-update.

---

## 📄 Template File Pedoman `.md` (Hasil `/breakdown-matkul`)

File ini dibaca AI saat `/make-laprak` Mode A. Struktur standar:

```markdown
# Pedoman Penulisan Laporan Mata Kuliah [NAMA_MATKUL]

Diekstrak dari [N] laporan riil: `file1.tex`, `file2.tex`, ...

> **ATURAN UTAMA:** Jangan mengarang format sendiri. Ikuti pola di bawah ini.

---

## 1. Struktur Bab (Wajib, Urut)
<!-- Contoh: \chapter{Dasar Teori}, \chapter{Hasil dan Pembahasan}, \chapter{Kesimpulan} -->

## 2. Dasar Teori
<!-- Gaya naratif, sitasi, gambar ilustrasi, rumus -->

## 3. Hasil dan Pembahasan — Tata Letak Gambar
<!-- Gaya Figure: A (1 gambar + caption di atas), B (2 gambar pair + \vspace), C (1 gambar penuh), D (kustom) -->
<!-- Sertakan contoh kode LaTeX untuk tiap gaya -->
<!-- Sertakan tabel panduan lebar gambar per type (override general.md jika perlu) -->

## 4. Kesimpulan
<!-- Format: enumerate / paragraf? Seberapa detail? -->

## 5. Tautan Repositori (jika ada)
<!-- Section sendiri / di daftar pustaka / di footnote? -->

## 6. Daftar Pustaka
<!-- \thebibliography + \cite ATAU enumerate + ref? -->
<!-- Contoh kode LaTeX -->

## 7. Konvensi Penulisan LaTeX
<!-- \textit{}, \texttt{}, escape _, clearpage, label/ref, dll -->

## 8. Instruksi Adaptasi untuk AI
<!-- Kapan pakai Gaya A vs B vs C, fallback jika type tidak dikenal, dll -->
```

---

## ⚙️ Parser `inisiai.txt` Enriched — Spesifikasi (Untuk Kontributor Core)

| Elemen | Format | Validasi |
|--------|--------|----------|
| Header section | `[@section] S<n> \| <judul>` | `S` + angka, unik |
| Baris data | `N.png \| S<n> \| type=<T> \| group=<G> \| <Label> \| Konteks: ... \| Arah: ...` | `type` ∈ tabel `general.md`; `group` = `single` atau `pair:M` (M integer) |
| Simetri pair | `pair:M` → harus ada pasangan `pair:M` lain di section yg sama | Warn + tanya user, **jangan auto-fix ke Gaya B** |
| Komentar | `# ...` (awal baris) | Diabaikan |
| Nama file dukungan | `N.png`, `Na.png`, `TN.png`, `TN-Na.png` | Regex: `^(\d+|T\d+|N[a-z]|T\d+-N[a-z])\.png$` |

---

## 🧪 Verifikasi Sebelum PR

1. `skills/make-laprak/SKILL.md` — validasi markdown (tidak ada link rusak, header konsisten).
2. `skills/make-laprak/template-general/general.md` — tabel `type`→width utuh (V7).
3. `skills/breakdown-matkul/SKILL.md` — procedure merujuk `_contoh/` input + `matkul/` lokal output.
4. `skills/make-laprak-info/SKILL.md` — verbatim panduan v0.4.0 (baca sebelum commit).
5. `skills/icg-renaming/SKILL.md` — VENDOR.md konsisten dengan upstream ICG, `scripts/src/` utuh.
6. `skills/icg-contextgenerate/SKILL.md` — VENDOR.md konsisten dengan upstream ICG, `scripts/src/` utuh.
7. `README.md` — struktur folder mencerminkan realita (matkul/ kosong + .gitkeep + ICG skills).
8. `CONTRIBUTING.md` — panduan ini sendiri.

---

## 💡 Tips

- Mulai dari 1 file `.tex` di `_contoh/`. Tambah seiring waktu.
- Gunakan `/breakdown-matkul` setiap kali `.tex` baru ditambahkan.
- Perhatikan evolusi gaya penulisan Anda — `.tex` terbaru biasanya paling matang.
- Ingin share gaya ke komunitas? Buka issue di GitHub dengan `_contoh/` yang dianonimkan, minta orang lain jalanin `/breakdown-matkul` sendiri.

---

## 📬 Kontak

Issue: [github.com/AcademyCity-RND/MyLaprak/issues](https://github.com/AcademyCity-RND/AC-MyLaprak/issues)