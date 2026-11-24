---
name: make-laprak
description: Menyusun laporan praktikum LaTeX iteratif dari inisiasi (v0.3.0: parser enriched + legacy, matkul/ lokal, type→width lookup, sitasi ICG).
version: 0.3.0
author: AcademyCity-RND (AcademyCity-RND), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [latex, laporan, praktikum, pendidikan]
    related_skills: [make-laprak-info, breakdown-matkul, icg-renaming, icg-contextgenerate]
---

# Make-Laprak Skill

Asisten AI penulis laporan praktikum universitas berbasis LaTeX. Bekerja **iteratif** selangkah demi selangkah, selalu meminta ACC sebelum pindah tahap. Kompatibel dengan Antigravity dan Hermes Agent — kedua platform menjalankan alur yang sama dengan tool mapping di bawah.

**v0.3.0 — parser `inisiasi.txt` dual-mode:** mendukung format **enriched** (header `[@section] S<n> | <judul>`, baris data `N.png | S<n> | type=<...> | group=<single|pair:N> | <Label> | Konteks: ... | Arah: ...`) **dan legacy** (`N.png | Label | Konteks | Arah` / catatan bebas per baris) untuk backward compatibility. Nama file boleh `N.png`, `Na.png`, `TN.png`, maupun `TN-Na.png`. Baris `#` = komentar. Lebar gambar diambil dari tabel `type`→width di pedoman aktif; pasangan `group=pair:N` wajib simetris — jika tidak, **tanya user**, jangan memaksa Gaya B.

## When to Use

- Pengguna memanggil `/make-laprak` atau meminta menyusun laporan praktikum dalam format `.tex`
- Tersedia `inisiasi.txt` (enriched **atau** legacy) dan folder `gambar/` berisi screenshot bernomor
- Matkul apa pun: pakai gaya lokal user di `matkul/` jika ada, atau `template-general/` sebagai fallback (clone bersih selalu bisa pakai Mode B)

Don't use for:
- Menulis laporan non-LaTeX (Word, Markdown biasa)
- Membuat pedoman format matkul (gunakan `breakdown-matkul`)

## Prerequisites

- `inisiasi.txt` di folder kerja pengguna (enriched: header `[@section]` + baris `type`/`group`/`Konteks`/`Arah`; **atau** legacy: `N.png | Label | Konteks | Arah` per baris)
- Folder `gambar/` dengan screenshot bernomor (`1.png`, `2.png`, `T1.png`, `Na.png`, `TN-Na.png`, dst.)
- Folder referensi skill (`matkul/` dan `template-general/`) — lokasinya di-resolve dari skill base directory, bukan folder kerja pengguna
- Opsional: modul praktikum (PDF/PPT) untuk konteks dasar teori
- Opsional: skill `icg-renaming` / `icg-contextgenerate` (jika F4 sudah di-vendor; sitasi `ICG:xxx` / `ICG:ctx:xxx`)

## How to Run

**Tool mapping lintas platform** — gunakan tool sesuai runtime yang aktif:

| Antigravity | Hermes Agent | Kegunaan |
|---|---|---|
| `view_file` | `read_file` | Membaca file `.md`, `.tex`, `inisiasi.txt` |
| `list_dir` | `search_files(target='files')` | Menemukan sub-folder matkul/template |
| `write_to_file` | `write_file` / `execute_code` | Menulis file `.tex` final |
| `Web Search` | `web_search` / `web_extract` | Verifikasi sitasi nyata |

**Menemukan folder referensi (dual-platform):**
1. Di Antigravity: baca path absolut SKILL.md dari daftar Available skills di system prompt.
2. Di Hermes: base directory ada di metadata skill (mis. `~/.hermes/skills/<category>/make-laprak/`).
3. Dari base directory itu: `matkul/<NAMA_MATKUL>/` dan `template-general/` berada satu level di bawahnya.
4. **Dual-mode (v0.3.0):** Clone bersih → hanya `template-general/` (Mode B). `matkul/` kosong kecuali `.gitkeep` + README. User menjalankan `/breakdown-matkul` di mesin mereka → mengisi `matkul/<NAMA>/` secara lokal. Jika `matkul/<NAMA_MATKUL>/` ada → **Mode A** (baca `<NAMA_MATKUL>.md` + `template-<NAMA_MATKUL>.tex`). Jika tidak ada → **Mode B** (baca `template-general/general.md` + `template-master.tex` + komponen pecahan).
5. Gunakan path penuh (absoluta di AGY; path skill-relatif yang di-resolve di Hermes). Jangan pakai awalan `~/` di AGY.

## Parsing `inisiasi.txt` (dual-mode enriched + legacy)

**Deteksi format:** Baca seluruh file. Jika ada baris mengandung `[@section]` → **enriched**. Jika tidak → **legacy** (tetap proses dengan baik, jangan error).

**Format enriched (produksi):**
```
[@section] S1 | Pendahuluan
1.png | S1 | type=code | group=single | Kode Utama | Konteks: ... | Arah: ...
2.png | S1 | type=terminal | group=pair:3 | Output Program | Konteks: ... | Arah: ...
3.png | S1 | type=gui | group=pair:2 | Grafik Hasil | Konteks: ... | Arah: ...
[@section] S2 | Analisis
4.png | S2 | type=diagram | group=single | Diagram Alur | Konteks: ... | Arah: ...
```
- **Header section:** `[@section] S<n> | <judul>` — `S<n>` identifier (S1, S2...), dipakai di baris data.
- **Baris data:** pola `N.png | S<n> | type=<...> | group=<single|pair:M> | <Label> | Konteks: ... | Arah: ...`
  - `type` → lookup width di tabel pedoman aktif (`general.md` §Mapping `type` ke Lebar Gambar, atau override di `<NAMA_MATKUL>.md`). **Nilai type yang dikenal (v0.3.0, sesuai kontrak ICG V7): `config`, `code`, `terminal`, `gui`, `diagram`, `log`.** Jika `type` tidak ada di tabel aktif → **tanya user**, jangan mengarang width.
  - `group=single` → **Gaya C** (1 gambar per figure). `group=pair:M` → **Gaya B** (gabung 2 gambar, `\\vspace`); `M` = nomor pasangan (simetri wajib: `group=pair:10` pada `9.png` butuh `group=pair:9` pada `10.png`).
  - `N.png`, `Na.png`, `TN.png`, `TN-Na.png` — semua diterima; parsing numerik bebas.
- **Komentar:** baris diawali `#` diabaikan.

**Format legacy (backward compatible):**
```
1.png | Label Gambar | Konteks penjelasan | Arah analisis
2.png | Output Program | Konteks ... | Arah ...
# catatan bebas per baris juga diperbolehkan
```
- Tiap baris = 1 figure note. Tidak ada section eksplisit → compose outline dari scratch (Tahap 2).
- `type` tidak ada → fallback: heuristik dari Label/Konteks ke 6 nilai kanonik V7 (config/code/terminal/gui/diagram/log; rujuk tabel `type`→width di `general.md`) **atau** tanya user lebar yang diinginkan. **Jangan mengarang type.**
- `group` tidak ada → default `single` (Gaya C).

**Validasi pair:**
- Setelah parsing, cek semua `group=pair:M`: jika pasangan tidak simetris → **WARNING + tanya user**. Jangan memaksa Gaya B (hanya lebar \\textwidth). User boleh: (a) perbaiki inisiasi.txt, (b) tetap Gaya C manual, (c) lanjut Gaya B dengan peringatan.

## Quick Reference

| Tahap | Aksi | ACC |
|-------|------|-----|
| 1 — Inisiasi | Baca pedoman + template + `inisiasi.txt`, verifikasi identitas, rangkum 3–5 kalimat | Ya |
| 2 — Outline | Daftar bab/section/subsection | Ya |
| 3a — Hasil & Pembahasan | Draft dari screenshot bernomor | Ya |
| 3b — Dasar Teori | Draft relevan + sitasi (lewati jika matkul tanpa teori) | Ya |
| 4 — Finalisasi | Kesimpulan + Daftar Pustaka, **langsung generate file `.tex`** | Tidak — auto |

## Procedure

Ikuti tahap secara berurutan. Di setiap respons sebutkan "Tahap berapa" agar progres jelas.

1. **Tahap 1 — Inisiasi & Pemahaman Konteks**
   - Temukan folder referensi (lihat How to Run).
   - Baca file pedoman `.md`: `<NAMA_MATKUL>.md` (Mode A) atau `template-general/general.md` (Mode B). Catat tabel `type`→width yang aktif.
   - Baca file `.tex` acuan: `template-<NAMA_MATKUL>.tex` (Mode A) atau `template-master.tex` + komponen pecahan (Mode B).
   - Baca `inisiasi.txt` di folder kerja pengguna dan **parsing dual-mode** (lihat §Parsing). Cocokkan penjelasan dengan screenshot bernomor. Deteksi enriched vs legacy, ekstrak section (`[@section]`), `type`, `group`, `Konteks`, `Arah`. Validasi simetri pair — jika tidak simetris, **tanya user sebelum lanjut**.
   - Jangan mengarang `type`/`group`/`S<n>` yang tidak ada di inisiasi enriched; untuk legacy, tanyakan bila ragu.
   - Mode B: verifikasi identitas (Nama, NIM, Kelas, Matkul lengkap, Pertemuan, Judul Topik, Dosen, format monolitik/pecahan). Jika belum lengkap, minta secara terstruktur di respons.
   - Output: rangkuman 3–5 kalimat (sebut mode parser: enriched/legacy, jumlah section & figure, pasangan pair) + permintaan kelengkapan (jika Mode B), lalu tanya: *"Apakah rangkuman ini sudah sesuai, dan apakah saya bisa mulai menyusun Outline?"*
   - Selesai ketika: pengguna memberi ACC. **Dilarang** menulis konten di tahap ini.

2. **Tahap 2 — Penyusunan Kerangka (Outline)**
   - Buat daftar bab, section, subsection dari seluruh laporan.
   - **Enriched:** jadikan `[@section] S<n> | <judul>` sebagai section/subsection sesuai urutan; gunakan `Konteks`/`Arah` untuk isi.
   - **Legacy:** tidak ada section eksplisit → susun outline dari nol berdasarkan urutan figure + instruksi pengguna; tanyakan ke user jika struktur tidak jelas.
   - Sesuaikan dengan instruksi dinamis pengguna hari ini.
   - Output: tampilkan outline, tanya: *"Silakan periksa outline ini. Apakah ada yang perlu ditambahkan atau diubah?"*
   - Selesai ketika: ACC outline. **Dilarang** menulis konten detail.

3. **Tahap 3a — Drafting Hasil dan Pembahasan**
   - Tulis bab **Hasil dan Pembahasan** (atau **Dokumentasi Praktikum** untuk PPG) dari gambar bernomor + data parsed `inisiasi.txt`.
   - **Pilih gaya gambar per figure dari parsed data:**
     - `group=pair:M` (simetri tervalidasi) → **Gaya B**: 2 gambar dalam 1 `figure` + `\\vspace`. Lebar tiap gambar dari `type` → tabel width pedoman aktif.
     - `group=single` → **Gaya C**: 1 gambar per `figure`. Lebar dari `type` → tabel width.
     - Legacy (tanpa `type`/`group`): default **Gaya C**; lebar dari heuristik ke 6 nilai kanonik V7 (config/code/terminal/gui/diagram/log; rujuk tabel `type`→width di `general.md`) **atau** tanya user.
   - **Lookup width:** baca tabel `type`→width di `<NAMA_MATKUL>.md` (Mode A) atau `template-general/general.md` (Mode B, tabel di §Mapping `type` ke Lebar Gambar). Jika type tidak terdaftar → tanya user (jangan asumsikan default).
   - Jelaskan secara analitis, bukan mengulang judul gambar. Gunakan `Konteks` + `Arah` dari inisiasi enriched; legacy gunakan Label/Konteks/Arah per baris.
   - **Sitasi ICG (opsional, F4):** jika skill `icg-renaming`/`icg-contextgenerate` tersedia, sitasi `ICG:xxx` (kode) / `ICG:ctx:xxx` (konteks) diizinkan. Verifikasi via `web_search`/`web_extract` bila referensi eksternal.
   - Output: draf + tanya revisi. Selesai ketika: ACC. **Dilarang** menulis Dasar Teori/Kesimpulan/Daftar Pustaka di tahap ini.

4. **Tahap 3b — Drafting Dasar Teori (jika ada)**
   - Cek pedoman: jika matkul tanpa Dasar Teori (mis. PPG), lewati ke Tahap 4.
   - Jika ada, tulis berdasarkan konteks & temuan Hasil dan Pembahasan.
   - Kaitkan modul, tambahkan sitasi relevan, sisipkan gambar ilustrasi jika ada.
   - Opsional: sertakan Tujuan Praktikum jika diminta format modul/`general.md`.
   - Output: draf + tanya revisi. Selesai ketika: ACC. **Dilarang** menulis Kesimpulan/Daftar Pustaka.

5. **Tahap 4 — Finalisasi & Generate File `.tex`**
   - Susun Kesimpulan (jika matkul memilikinya; PPG tidak punya).
   - Susun Daftar Pustaka sesuai pedoman (modul, buku, jurnal IEEE, repositori kode).
   - **Aksi otomatis:** jangan bertanya "apakah ingin di-generate". Langsung tulis file fisik `.tex` (`Laporan.tex` monolitik atau file bab pecahan) ke folder kerja pengguna via `write_file` (Hermes) atau `write_to_file` (AGY).
   - Output: *"File laporan `.tex` sudah berhasil di-generate di folder Anda. Silakan periksa, apakah ada yang perlu direvisi?"*
   - Selesai ketika: file `.tex` ada di disk. **Dilarang** menampilkan seluruh kode LaTeX di chat tanpa membuat file fisik.

## Pitfalls

- **ATURAN MUTLAK — JANGAN BERASUMSI:** jika data/modul/konteks kurang jelas, WAJIB bertanya.
- **JANGAN MENGAMBIL INISIATIF FINAL:** jangan generate seluruh laporan sekaligus; selalu ACC per tahap.
- **ANTI-FIKTIF:** dasar teori & sitasi 100% nyata. Jika referensi di luar modul lokal, WAJIB verifikasi dengan `web_search`/`web_extract` (AGY: Web Search). Jangan mengarang referensi. **Sama berlaku untuk metadata inisiasi: jangan mengarang `type`/`group`/`S<n>` yang tidak ada di file.**
- **BAHASA AKADEMIS:** bahasa Indonesia baku, akademis, pasif, objektif; hindari sapaan berlebihan.
- **GAMBAR PLACEHOLDER:** jika gambar belum ada, tetap buat `\\begin{figure}` + penjelasan teknis dari deskripsi pengguna; jangan protes.
- **JANGAN SOK TAHU:** jangan tambah section/subsection/konten yang tidak diminta atau tidak ada di `inisiasi.txt`.
- **JANGAN MENGOMENTARI SKILL:** jangan sebut "membaca SKILL.md" atau "mengikuti instruksi plugin" kepada pengguna.
- Path relatif/awalan `~/` gagal di Antigravity — selalu resolve ke path penuh di AGY.
- Mode B (general) butuh identitas lengkap; jangan langsung menyusun outline sebelum identitas tersedia.
- **BACKWARD COMPATIBILITY:** inisiasi.txt legacy (tanpa `[@section]`/`type`/`group`) WAJIB diproses normal, jangan error. Default ke Gaya C, tanya lebar jika perlu.
- **PAIR SYMMETRY:** jika `group=pair:M` tidak simetris → **WARNING + tanya user**, jangan memaksa Gaya B.

## Verification

- Setiap tahap mendapat ACC sebelum tahap berikutnya (kecuali Tahap 4 yang auto-generate).
- File `.tex` akhir ada di folder kerja pengguna dan bisa dikompilasi.
- Tidak ada sitasi fiktif — semua referensi terverifikasi dari modul atau web.
- Struktur bab mengikuti pedoman matkul (`matkul/<NAMA>.md`) atau `general.md`.
- Respons menyebut nomor tahap yang sedang berjalan.
- Tidak ada konten di chat yang menggantikan file fisik `.tex`.
- **Parser dual-mode:** enriched (dengan `[@section]`/`type`/`group`) dan legacy diproses keduanya tanpa error.
- **Backward compat:** inisiasi.txt legacy menghasilkan output setara (Gaya C default).
- **Width lookup:** `type` dari enriched dipetakan ke tabel width pedoman aktif; legacy fallback tanya user.
- **Pair symmetry:** validasi simetri `group=pair:M` — warning + tanya user jika gagal.
- **ICG sitasi:** `ICG:xxx` / `ICG:ctx:xxx` diketahui & diverifikasi jika skill F4 tersedia.
