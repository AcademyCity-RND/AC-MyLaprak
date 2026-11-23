---
name: make-laprak
description: Menyusun laporan praktikum LaTeX secara iteratif dari inisiasi.
version: 0.2.0
author: AcademyCity-RND (AcademyCity-RND), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [latex, laporan, praktikum, pendidikan]
    related_skills: [make-laprak-info, breakdown-matkul]
---

# Make-Laprak Skill

Asisten AI penulis laporan praktikum universitas berbasis LaTeX. Bekerja **iteratif** selangkah demi selangkah, selalu meminta ACC sebelum pindah tahap. Kompatibel dengan Antigravity dan Hermes Agent — kedua platform menjalankan alur yang sama dengan tool mapping di bawah.

## When to Use

- Pengguna memanggil `/make-laprak` atau meminta menyusun laporan praktikum dalam format `.tex`
- Tersedia `inisiasi.txt` dan folder `gambar/` berisi screenshot bernomor
- Mata kuliah terdaftar (`KEPL`, `PPD`, `PPG`) **atau** mata kuliah apa pun via `template-general/`

Don't use for:
- Menulis laporan non-LaTeX (Word, Markdown biasa)
- Membuat pedoman format matkul (gunakan `breakdown-matkul`)

## Prerequisites

- `inisiasi.txt` di folder kerja pengguna (peta alur + penjelasan screenshot)
- Folder `gambar/` dengan screenshot bernomor (`1.png`, `2.png`, `T1.png`, dst)
- Folder referensi skill (`matkul/` dan `template-general/`) — lokasinya di-resolve dari skill base directory, bukan folder kerja pengguna
- Opsional: modul praktikum (PDF/PPT) untuk konteks dasar teori

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
4. **Dual-mode:** Jika `matkul/<NAMA_MATKUL>/` ada → Mode A (baca `<NAMA_MATKUL>.md` + `template-<NAMA_MATKUL>.tex`). Jika tidak ada → Mode B (baca `template-general/general.md` + `template-master.tex` dan komponen pecahan).
5. Gunakan path penuh (absoluta di AGY; path skill-relatif yang di-resolve di Hermes). Jangan pakai awalan `~/` di AGY.

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
   - Baca file pedoman `.md`: `<NAMA_MATKUL>.md` (Mode A) atau `template-general/general.md` (Mode B).
   - Baca file `.tex` acuan: `template-<NAMA_MATKUL>.tex` (Mode A) atau `template-master.tex` + komponen pecahan (Mode B).
   - Baca `inisiasi.txt` di folder kerja pengguna; cocokkan penjelasan dengan screenshot bernomor.
   - Mode B: verifikasi identitas (Nama, NIM, Kelas, Matkul lengkap, Pertemuan, Judul Topik, Dosen, format monolitik/pecahan). Jika belum lengkap, minta secara terstruktur di respons.
   - Output: rangkuman 3–5 kalimat + permintaan kelengkapan (jika Mode B), lalu tanya: *"Apakah rangkuman ini sudah sesuai, dan apakah saya bisa mulai menyusun Outline?"*
   - Selesai ketika: pengguna memberi ACC. **Dilarang** menulis konten di tahap ini.

2. **Tahap 2 — Penyusunan Kerangka (Outline)**
   - Buat daftar bab, section, subsection dari seluruh laporan.
   - Sesuaikan dengan instruksi dinamis pengguna hari ini.
   - Output: tampilkan outline, tanya: *"Silakan periksa outline ini. Apakah ada yang perlu ditambahkan atau diubah?"*
   - Selesai ketika: ACC outline. **Dilarang** menulis konten detail.

3. **Tahap 3a — Drafting Hasil dan Pembahasan**
   - Tulis bab **Hasil dan Pembahasan** (atau **Dokumentasi Praktikum** untuk PPG) dari gambar bernomor + `inisiasi.txt`.
   - Ikuti gaya tata letak gambar dari pedoman `.md`.
   - Jelaskan secara analitis, bukan mengulang judul gambar.
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
- **ANTI-FIKTIF:** dasar teori & sitasi 100% nyata. Jika referensi di luar modul lokal, WAJIB verifikasi dengan `web_search`/`web_extract` (AGY: Web Search). Jangan mengarang referensi.
- **BAHASA AKADEMIS:** bahasa Indonesia baku, akademis, pasif, objektif; hindari sapaan berlebihan.
- **GAMBAR PLACEHOLDER:** jika gambar belum ada, tetap buat `\begin{figure}` + penjelasan teknis dari deskripsi pengguna; jangan protes.
- **JANGAN SOK TAHU:** jangan tambah section/subsection/konten yang tidak diminta atau tidak ada di `inisiasi.txt`.
- **JANGAN MENGOMENTARI SKILL:** jangan sebut "membaca SKILL.md" atau "mengikuti instruksi plugin" kepada pengguna.
- Path relatif/awalan `~/` gagal di Antigravity — selalu resolve ke path penuh di AGY.
- Mode B (general) butuh identitas lengkap; jangan langsung menyusun outline sebelum identitas tersedia.

## Verification

- Setiap tahap mendapat ACC sebelum tahap berikutnya (kecuali Tahap 4 yang auto-generate).
- File `.tex` akhir ada di folder kerja pengguna dan bisa dikompilasi.
- Tidak ada sitasi fiktif — semua referensi terverifikasi dari modul atau web.
- Struktur bab mengikuti pedoman matkul (`KEPL`/`PPD`/`PPG`) atau `general.md`.
- Respons menyebut nomor tahap yang sedang berjalan.
- Tidak ada konten di chat yang menggantikan file fisik `.tex`.
