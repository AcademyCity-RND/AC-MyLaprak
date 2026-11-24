---
name: breakdown-matkul
description: Ekstrak pedoman format matkul dari contoh laporan LaTeX (versi 0.3.0: baca dari folder kerja _contoh/, output ke matkul/ lokal).
version: 0.3.0
author: AcademyCity-RND (AcademyCity-RND), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [latex, matkul, pedoman, template, formatting]
    related_skills: [make-laprak, make-laprak-info, icg-renaming, icg-contextgenerate]
---

# Breakdown-Matkul Skill

Menganalisis file `.tex` contoh laporan praktikum dan mengekstrak **pola penulisan** menjadi file pedoman `.md` terstruktur plus berkas template placeholder `template-<NAMA_MATKUL>.tex`. Hasilnya dipakai `make-laprak` sebagai aturan formatting.

**Sejak v0.3.0:** contoh laporan dibaca dari **`<folder kerja>/_contoh/`**, sedangkan hasil ditulis ke folder **`matkul/` lokal di dalam skill** (yang sengaja di-gitignore agar gaya pribadi tidak pernah masuk repo publik). Kompatibel dengan Antigravity dan Hermes Agent.

## When to Use

- Menambahkan mata kuliah baru ke plugin `make-laprak`
- Memperbarui pedoman matkul setelah ada file `.tex` referensi baru
- Ingin mengganti laporan riil dengan template placeholder demi privasi repositori

Don't use for:
- Menulis laporan praktikum (gunakan `make-laprak`)
- Menampilkan info plugin (gunakan `make-laprak-info`)

## Prerequisites

- Folder kerja pertemuan yang sedang dipakai user, berisi **`_contoh/`** dengan minimal satu file `.tex` laporan riil yang sudah disetujui.
- Akses menulis ke folder **`matkul/` di skill base directory** (milik lokal user, diabaikan Git).
- Jika `_contoh/` kosong atau tidak ada: **WAJIB** minta user menyediakan minimal 1 `.tex` contoh. Jangan mengarang pola dari matkul lain, dan jangan membaca `matkul/` sebagai sumber contoh.

## How to Run

**Tool mapping lintas platform:**

| Antigravity | Hermes Agent | Kegunaan |
|---|---|---|
| `list_dir` | `search_files(target='files')` | Menemukan `_contoh/` di folder kerja & sub-folder matkul |
| `view_file` | `read_file` | Membaca file `.tex`/`.md` |
| `write_to_file` | `write_file` / `execute_code` | Menulis `.md` dan `template-*.tex` ke `matkul/` lokal |

**Menemukan folder referensi:**
1. Tanyakan/path-kan folder kerja user yang sedang aktif (mis. `D:\Tugas\KEPL\UTS\`). Jika tidak disebut, minta konfirmasi — jangan menebak.
2. **Input:** `<folder kerja>/_contoh/*.tex`. Di AGY gunakan path penuh; di Hermes resolve path absolut.
3. **Output:** `matkul/<NAMA_MATKUL>/` di dalam base directory skill `make-laprak` (AGY: derive dari path SKILL.md; Hermes: `~/.hermes/skills/<category>/make-laprak/matkul/`). Folder ini lokal dan tidak dipush.
4. Jangan pernah menulis hasil breakdown ke `<folder kerja>/_contoh/` — folder itu hanya untuk input contoh.

## Quick Reference

| Langkah | Fokus | Input / Output |
|---------|-------|----------------|
| 1 — Identifikasi | Target matkul + list file | Input: `_contoh/*.tex`; Output: daftar `.tex`/`.md` |
| 2 — Analisis | Struktur, gambar, sitasi, konvensi, evolusi | Catatan pola |
| 3 — Susun | File `.md` + `template-<NAMA>.tex` | Draf dokumen |
| 4 — Tulis | Simpan ke `matkul/<NAMA>/` (lokal) | File fisik + ringkasan |

## Procedure

1. **Identifikasi Target**
   - Tanyakan matkul yang ingin di-breakdown (mis. "KEPL").
   - Resolve folder kerja user, lalu list semua `.tex` di `<folder kerja>/_contoh/`. Jika kosong/tidak ada → minta user menyediakan minimal 1 `.tex`; **jangan lanjut** dengan menebak atau memakai `matkul/` sebagai pengganti.
   - Cek juga `matkul/<NAMA_MATKUL>/` (lokal): jika sudah ada `.md`, baca dan pahami isinya terlebih dahulu untuk pembaruan kumulatif.
   - Selesai ketika: target, berkas referensi di `_contoh/`, dan tujuan output teridentifikasi.

2. **Analisis Semua `.tex` Laporan Riil di `_contoh/`**
   - Baca **setiap** file `.tex` contoh di `_contoh/` (abaikan `template-*.tex` agar fokus pada dokumen riil).
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
   - **LANGSUNG** tulis `.md` dan `template-<NAMA_MATKUL>.tex` ke `matkul/<NAMA_MATKUL>/` di skill base directory (folder lokal user) via `write_file` (Hermes) atau `write_to_file` (AGY).
   - **Jangan** menyalin laporan riil dari `_contoh/` ke dalam repo/plugin. Hanya template placeholder yang boleh dihasilkan.
   - Tampilkan ringkasan perubahan.
   - Tanya: *"Pedoman dan template matkul sudah diperbarui di folder lokal Anda. Ada yang perlu direvisi?"*
   - Selesai ketika: file fisik ada di disk dan ringkasan disampaikan.

## Pitfalls

- **ANALISIS, BUKAN COPY-PASTE:** jangan menyalin isi `.tex` ke `.md`; ekstrak pola dan aturan.
- **JANGAN MENGARANG ATURAN:** setiap aturan harus dibuktikan dari minimal satu `.tex`. Jika ragu, tandai `(perlu konfirmasi)`.
- **KUMULATIF, BUKAN TIMPA:** jika `.md` sudah ada, baca dulu; perbarui/perkaya, jangan hapus aturan yang benar.
- **PRIORITASKAN `.TEX` TERBARU:** nomor tertinggi = paling mutakhir, jadi rekomendasi utama.
- **KEBERSIHAN PRIVASI:** baca contoh hanya dari `_contoh/`; tulis hanya template placeholder ke `matkul/` lokal. Laporan riil tidak pernah masuk repo.
- Abaikan `template-*.tex` saat menganalisis — itu hanya placeholder hasil skill, bukan dokumen riil.
- Jangan menulis laporan untuk penugasan pengguna; skill ini hanya menghasilkan pedoman + template.
- **JANGAN MENGAMBIL INISIATIF FINAL:** hasil breakdown adalah draf gaya; user tetap mengonfirmasi sebelum dipakai `make-laprak`.

## Verification

- Sumber contoh adalah `<folder kerja>/_contoh/*.tex`, bukan `matkul/`.
- File `.md` mengikuti 8 bagian FORMAT OUTPUT di bawah.
- `template-<NAMA_MATKUL>.tex` berisi placeholder, bukan data laporan riil.
- Setiap aturan di `.md` memiliki bukti dari minimal satu `.tex` referensi.
- Aturan lama yang benar tidak hilang (kumulatif).
- Gaya terbaru menjadi rekomendasi utama bila ada konflik.
- File hasil ada di `matkul/<NAMA>/` (lokal) dan **tidak** muncul di `git status` repo publik.

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
