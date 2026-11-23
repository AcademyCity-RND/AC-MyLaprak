---
name: breakdown-matkul
description: Ekstrak pedoman format matkul dari contoh laporan LaTeX.
version: 0.2.0
author: AcademyCity-RND (AcademyCity-RND), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [latex, matkul, pedoman, template, formatting]
    related_skills: [make-laprak, make-laprak-info]
---

# Breakdown-Matkul Skill

Menganalisis file `.tex` contoh laporan praktikum dan mengekstrak **pola penulisan** menjadi file pedoman `.md` terstruktur plus berkas template placeholder `template-<NAMA_MATKUL>.tex`. Hasilnya dipakai `make-laprak` sebagai aturan formatting. Kompatibel dengan Antigravity dan Hermes Agent.

## When to Use

- Menambahkan mata kuliah baru ke plugin `make-laprak`
- Memperbarui pedoman matkul setelah ada file `.tex` referensi baru
- Ingin mengganti laporan riil dengan template placeholder demi privasi repositori

Don't use for:
- Menulis laporan praktikum (gunakan `make-laprak`)
- Menampilkan info plugin (gunakan `make-laprak-info`)

## Prerequisites

- Akses ke folder `matkul/` di skill base directory (bukan folder kerja pengguna)
- Minimal satu file `.tex` laporan riil di `matkul/<NAMA_MATKUL>/`
- Izin menulis ke folder matkul tersebut

## How to Run

**Tool mapping lintas platform:**

| Antigravity | Hermes Agent | Kegunaan |
|---|---|---|
| `list_dir` | `search_files(target='files')` | Menemukan sub-folder matkul & file |
| `view_file` | `read_file` | Membaca file `.tex`/`.md` |
| `write_to_file` | `write_file` / `execute_code` | Menulis `.md` dan `template-*.tex` |

**Menemukan folder referensi:**
1. AGY: cari entri skill `make-laprak` di Available skills, derive folder `matkul/` dari path SKILL.md-nya.
2. Hermes: resolve dari skill base directory (`~/.hermes/skills/<category>/make-laprak/matkul/`).
3. Gunakan path penuh di AGY; path skill-relatif yang di-resolve di Hermes.

## Quick Reference

| Langkah | Fokus | Output |
|---------|-------|--------|
| 1 — Identifikasi | Target matkul + list file | Daftar `.tex`/`.md` |
| 2 — Analisis | Struktur, gambar, sitasi, konvensi, evolusi | Catatan pola |
| 3 — Susun | File `.md` + `template-<NAMA>.tex` | Draf dokumen |
| 4 — Tulis | Simpan ke folder matkul | File fisik + ringkasan |

## Procedure

1. **Identifikasi Target**
   - Tanyakan matkul yang ingin di-breakdown (mis. "KEPL").
   - Temukan folder matkul tersebut; list semua file `.tex` dan `.md`.
   - Jika sudah ada `.md`, baca dan pahami isinya terlebih dahulu.
   - Selesai ketika: target dan berkas referensi teridentifikasi.

2. **Analisis Semua `.tex` Laporan Riil**
   - Baca **setiap** file `.tex` contoh (abaikan `template-*.tex` agar fokus pada dokumen riil).
   - Untuk masing-masing, catat:
     - **A. Struktur Dokumen:** hierarki bab/section/subsection; `\clearpage` antar section; section khusus; preamble/cover sendiri (PPD) vs langsung `\chapter` (KEPL/PPG); ada/tidaknya Dasar Teori & Kesimpulan.
     - **B. Tata Letak Gambar:** `\begin{figure}[H]`?; semua variasi `width=...`; posisi penjelasan (sebelum gambar = Gaya C KEPL, atau di bawah dengan `Penjelasan Gambar :` = PPD/PPG); gambar gabungan dalam satu figure + `\vspace`; side-by-side dengan `\minipage`.
     - **C. Sitasi & Daftar Pustaka:** `\cite{...}` + `thebibliography`, atau `[\ref{...}]` + `enumerate`; format (APA, IEEE, dll).
     - **D. Konvensi Penulisan:** `\textit{...}`, `\texttt{...}`, `\enumerate` vs narasi, escape `\_`, `\&`, `\allowbreak`.
     - **E. Evolusi Gaya:** perubahan dari `.tex` tertua ke terbaru; gaya paling matang/konsisten.
   - Selesai ketika: semua pola tercatat dengan bukti dari minimal satu file.

3. **Susun File `.md` dan `template-<NAMA_MATKUL>.tex`**
   - Tulis/perbarui `.md` mengikuti FORMAT OUTPUT di bawah.
   - Susun `template-<NAMA_MATKUL>.tex` monolitik yang setia pada format asli, memakai teks placeholder.
   - Selesai ketika: kedua dokumen memiliki struktur sesuai format.

4. **Tulis File & Konfirmasi**
   - **LANGSUNG** tulis `.md` dan `template-<NAMA_MATKUL>.tex` ke folder matkul via `write_file` (Hermes) atau `write_to_file` (AGY).
   - Tampilkan ringkasan perubahan.
   - Tanya: *"Pedoman dan template matkul sudah diperbarui. Ada yang perlu direvisi?"*
   - Selesai ketika: file fisik ada di disk dan ringkasan disampaikan.

## Pitfalls

- **ANALISIS, BUKAN COPY-PASTE:** jangan menyalin isi `.tex` ke `.md`; ekstrak pola dan aturan.
- **JANGAN MENGARANG ATURAN:** setiap aturan harus dibuktikan dari minimal satu `.tex`. Jika ragu, tandai `(perlu konfirmasi)`.
- **KUMULATIF, BUKAN TIMPA:** jika `.md` sudah ada, baca dulu; perbarui/perkaya, jangan hapus aturan yang benar.
- **PRIORITASKAN `.TEX` TERBARU:** nomor tertinggi = paling mutakhir, jadi rekomendasi utama.
- **KEBERSIHAN PRIVASI:** buat/perbarui `template-<NAMA_MATKUL>.tex` berisi placeholder agar laporan riil bisa dihapus dari repo.
- Jangan mengabaikan `template-*.tex` saat menganalisis — itu bukan dokumen riil.
- Jangan menulis laporan untuk penugasan pengguna; skill ini hanya menghasilkan pedoman + template.

## Verification

- File `.md` mengikuti 8 bagian FORMAT OUTPUT di bawah.
- `template-<NAMA_MATKUL>.tex` berisi placeholder, bukan data laporan riil.
- Setiap aturan di `.md` memiliki bukti dari minimal satu `.tex` referensi.
- Aturan lama yang benar tidak hilang (kumulatif).
- Gaya terbaru menjadi rekomendasi utama bila ada konflik.

## FORMAT OUTPUT (.md)

```markdown
# Pedoman Penulisan Laporan Mata Kuliah [NAMA_MATKUL]

Dokumen ini adalah panduan **wajib baca** bagi AI sebelum menyusun laporan.
Diekstrak dari [N] laporan riil: `file1.tex`, `file2.tex`, dst.

> **ATURAN UTAMA:** Jangan mengarang format sendiri. Ikuti pola di bawah ini.

---

## 1. Struktur Bab (Wajib, Urut)
[Daftar chapter/section/subsection yang konsisten di semua referensi]

## 2. Dasar Teori (jika ada pada matkul)
[Aturan penulisan dasar teori — gaya naratif, sitasi, penggunaan gambar ilustrasi]

## 3. Hasil dan Pembahasan — Tata Letak Gambar
[Dokumentasikan SEMUA gaya figure yang ditemukan, dengan label (Gaya A/B/C/dst)]
[Sertakan contoh kode LaTeX untuk setiap gaya]
[Sertakan tabel panduan lebar gambar]

## 4. Kesimpulan (jika ada pada matkul)
[Format kesimpulan — enumerate/paragraf, tingkat detail]

## 5. Tautan Repositori (jika ada)
[Di mana dan bagaimana source code dicantumkan]

## 6. Daftar Pustaka
[Dokumentasikan SEMUA format yang ditemukan]
[Rekomendasikan format yang paling sering dipakai]

## 7. Konvensi Penulisan LaTeX
[Italic, monospace, escape characters, clearpage, allowbreak, dll]

## 8. Instruksi Adaptasi untuk AI
[Panduan kapan menggunakan gaya mana, berdasarkan konteks inisiasi.txt]
```

Setelah selesai, pengguna bisa langsung memanggil `/make-laprak` yang membaca `.md` dan `template-<NAMA_MATKUL>.tex` hasil breakdown ini.
