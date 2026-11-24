---
name: make-laprak-info
description: Menampilkan panduan penggunaan plugin make-laprak apa adanya (v0.3.0: alur ICG + parser dual-mode).
version: 0.3.0
author: AcademyCity-RND (AcademyCity-RND), Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [dokumentasi, bantuan, make-laprak]
    related_skills: [make-laprak, breakdown-matkul, icg-renaming, icg-contextgenerate]
---

# Make-Laprak Info Skill

Skill bantuan yang menampilkan teks panduan plugin `make-laprak` **persis seperti tertulis**. Tidak memodifikasi file apa pun. Kompatibel dengan Antigravity dan Hermes Agent.

**v0.3.0:** panduan mencakup alur 4 skill (ICG-Renaming → ICG-ContextGenerate → breakdown-matkul → make-laprak), parser dual-mode enriched/legacy, folder kerja `_contoh/`, gaya matkul lokal (`matkul/`) yang tidak ikut ter-clone, dan sitasi ICG.

## When to Use

- Pengguna memanggil `/make-laprak-info`
- Pengguna meminta informasi tentang apa itu plugin/skill `make-laprak`, fitur, atau cara pakainya

Don't use for:
- Menulis laporan (gunakan `make-laprak`)
- Membuat pedoman matkul (gunakan `breakdown-matkul`)

## Prerequisites

- Tidak ada dependency eksternal
- Tool tidak diperlukan — cukup tampilkan teks

## How to Run

1. Deteksi panggilan `/make-laprak-info` atau permintaan info setara.
2. Salin teks di bagian **Procedure** di bawah **persis seperti tertulis**.
3. Jangan memodifikasi, memparafrase, atau menambahkan kata-kata sendiri.
4. Jangan mengubah file apa pun.

| Antigravity | Hermes Agent | Kegunaan |
|---|---|---|
| (tanpa tool) | (tanpa tool) | Langsung tampilkan teks |

## Quick Reference

| Aksi | Hasil |
|------|-------|
| `/make-laprak-info` | Tampilkan panduan lengkap (teks verbatim) |
| Permintaan info plugin | Tampilkan panduan lengkap (teks verbatim) |

## Procedure

**Tampilkan teks berikut apa adanya — jangan mengubah satu pun kata:**

---

# 📋 Plugin `/make-laprak` — Panduan Penggunaan

## 1. Apa itu `/make-laprak`?

Plugin AI (Antigravity Skill) yang membantu menyusun **Laporan Praktikum** tingkat Universitas dalam format **LaTeX**. AI bekerja secara **iteratif** — selangkah demi selangkah, selalu meminta persetujuan (ACC) Anda sebelum lanjut ke tahap berikutnya.

## 2. Fitur Utama

- 📖 Membaca `inisiasi.txt` (format **enriched** dengan header `[@section]` + `type`/`group`/`Konteks`/`Arah` **atau** **legacy** `N.png | Label | Konteks | Arah`) dan mencocokkan instruksi dengan screenshot bernomor.
- 🌐 **Dukungan Dual-Mode (v0.3.0):**
  - **Mode Gaya Matkul Lokal (User):** Menggunakan pedoman formatting hasil `/breakdown-matkul` Anda di folder `matkul/<NAMA>/` (**lokal, tidak ikut ter-clone** — clone bersih = kosong). Anda buat gaya sendiri dari `_contoh/` laporan riil yang sudah dianonimkan.
  - **Mode Universal (General Fallback):** Selalu tersedia, mendukung mata kuliah praktikum **apa pun** secara instan menggunakan basis `template-general/`.
- ✍️ Menyusun Tujuan Praktikum, Dasar Teori analitis, Hasil & Pembahasan terstruktur, Kesimpulan bernomor, hingga Daftar Pustaka IEEE.
- 🔍 Sitasi nyata — AI wajib memverifikasi referensi melalui modul atau pencarian literatur daring, bukan mengarang sitasi. **Dukungan sitasi ICG:** `ICG:xxx` (kode) / `ICG:ctx:xxx` (konteks) jika skill ICG tersedia (F4 vendor).
- 📄 **Auto-generate file `.tex`** siap kompilasi (versi monolitik maupun modular per-bab) langsung ke folder kerja Anda di tahap akhir.

## 3. Cara Menggunakan

**Anda TIDAK PERLU** menaruh file di folder plugin. Plugin adalah "otak" di latar belakang.

**Langkah-langkah:**
1. Buat folder kerja **di mana saja** (misal: `D:\Tugas\PPD\Pertemuan-5\` atau `D:\Tugas\JaringanKomputer\Pertemuan-1\`).
2. Di dalamnya, siapkan:
   - `inisiasi.txt` — Catatan ringkas penjelasan Anda tentang alur praktikum dan tiap nomor screenshot (format **enriched** atau **legacy**).
   - Folder `gambar/` — Berkas screenshot bernomor (`1.png`, `2.png`, `T1.png`, `Na.png`, `TN-Na.png`, dst).
   - **Folder `_contoh/`** — Minimal satu laporan `.tex` riil yang sudah disetujui (di-anonimkan) untuk membuat gaya matkul via `/breakdown-matkul`.
   - (Opsional) Modul praktikum (PDF/PPT) pertemuan terkait.
3. Buka workspace di folder tersebut, lalu panggil:
   > `/make-laprak buatkan laporan [NAMA_MATKUL], saya sudah siapkan inisiasi.txt, folder gambar, dan _contoh/`
4. *Catatan Mode Universal:* Jika mata kuliah Anda belum punya gaya lokal di `matkul/`, AI akan menanyakan kelengkapan identitas (Nama, NIM, Dosen, Topik) di Tahap 1 sebelum melanjutkan ke penyusunan kerangka.

## 4. Alur Kerja (5 Tahap)

| Tahap | Apa yang AI Lakukan | Aksi Anda |
|-------|---------------------|-----------|
| **1 — Inisiasi** | Membaca referensi/template + `inisiasi.txt`, verifikasi kelengkapan identitas, merangkum pemahaman | Cek rangkuman & lengkapi data identitas → ACC |
| **2 — Outline** | Menyusun kerangka laporan (daftar bab/seksi/sub-seksi) | Cek outline → ACC / revisi |
| **3a — Hasil & Pembahasan** | Menulis draf bab pembahasan berdasarkan screenshot dan penjelasan input-output | Cek draf → ACC / revisi |
| **3b — Dasar Teori** | Menulis draf dasar teori relevan, formulasi matematis, dan diagram konsep | Cek draf → ACC / revisi |
| **4 — Finalisasi** | Menyusun Kesimpulan + Daftar Pustaka, lalu **langsung men-generate file fisik `.tex`** | Cek file hasil generate → revisi jika perlu |

## 5. Skill Pendukung

- `/breakdown-matkul` — Mengekstrak pedoman formatting dari file `.tex` contoh menjadi file `.md` pedoman matkul baru.
- `/make-laprak-info` — Menampilkan panduan dan status kapabilitas plugin ini.

## 6. Menambahkan Mata Kuliah Baru vs Menggunakan Template General

1. **Gunakan Langsung (General Template):** Anda tidak perlu repot menambahkan konfigurasi; cukup panggil `/make-laprak` untuk matkul apa pun, AI akan otomatis menerapkan `general.md` dan `template-master.tex`.
2. **Kustomisasi Khusus (Gaya Matkul Lokal):** Jika ingin gaya penulisan khusus permanen, **jangan taruh file di repo**. Lakukan di mesin Anda:
   - Siapkan `_contoh/` dengan laporan `.tex` riil yang sudah di-anonimkan.
   - Jalankan `/breakdown-matkul` → menghasilkan `matkul/<NAMA>/` **lokal** (diabaikan Git, tidak ikut ter-clone).
   - Clone bersih = hanya Mode Universal aktif. Gaya lokal aktif setelah *Anda* menjalankan `/breakdown-matkul`.

## 7. Dokumentasi & Kontribusi

- 📂 Repositori: [github.com/AcademyCity-RND/MyLaprak](https://github.com/AcademyCity-RND/MyLaprak)
- 📂 Repositori ICG (renaming + context): [github.com/AcademyCity-RND/AC-ImageContext-Generator](https://github.com/AcademyCity-RND/AC-ImageContext-Generator)
- 📝 Panduan kontribusi: lihat file `CONTRIBUTING.md` di repositori.

---

## Pitfalls

- Jangan mengubah, memparafrase, atau menambah kata pada teks panduan di atas — harus persis.
- Jangan memodifikasi file apa pun saat skill ini dipanggil.
- Jangan mencampurkan respons tambahan sebelum/sesudah teks panduan.

## Verification

- Teks yang tampil sama persis dengan blok di atas (karakter demi karakter).
- Tidak ada file yang berubah di disk.
- Tidak ada kata tambahan di luar blok panduan.