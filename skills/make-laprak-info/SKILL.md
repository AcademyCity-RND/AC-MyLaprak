---
name: make-laprak-info
description: >-
  Gunakan skill ini jika pengguna mengetik command "/make-laprak-info" atau meminta informasi tentang apa itu plugin/skill make-laprak.
---

# INSTRUKSI: TAMPILKAN TEKS DI BAWAH INI APA ADANYA

Jika skill ini dipanggil, Anda **WAJIB menyalin dan menampilkan** teks di bawah garis ini **persis seperti yang tertulis**. Jangan memodifikasi, memparafrase, atau menambahkan kata-kata sendiri. Jangan memodifikasi file apapun. Langsung tampilkan:

---

# 📋 Plugin `/make-laprak` — Panduan Penggunaan

## 1. Apa itu `/make-laprak`?

Plugin AI (Antigravity Skill) yang membantu menyusun **Laporan Praktikum** tingkat Universitas dalam format **LaTeX**. AI bekerja secara **iteratif** — selangkah demi selangkah, selalu meminta persetujuan (ACC) Anda sebelum lanjut ke tahap berikutnya.

## 2. Fitur Utama

- 📖 Membaca `inisiasi.txt` dan mencocokkan instruksi dengan screenshot bernomor.
- 🌐 **Dukungan Dual-Mode:**
  - **Mode Matkul Terdaftar:** Menggunakan aturan penulisan spesifik mata kuliah (misal: `KEPL`, `PPD`, `PPG`).
  - **Mode Universal (General Fallback):** Mendukung penyusunan laporan untuk mata kuliah praktikum **apa pun** secara instan menggunakan basis `template-general/`.
- ✍️ Menyusun Tujuan Praktikum, Dasar Teori analitis, Hasil & Pembahasan terstruktur, Kesimpulan bernomor, hingga Daftar Pustaka IEEE.
- 🔍 Sitasi nyata — AI wajib memverifikasi referensi melalui modul atau pencarian literatur daring, bukan mengarang sitasi.
- 📄 **Auto-generate file `.tex`** siap kompilasi (versi monolitik maupun modular per-bab) langsung ke folder kerja Anda di tahap akhir.

## 3. Cara Menggunakan

**Anda TIDAK PERLU** menaruh file di folder plugin. Plugin adalah "otak" di latar belakang.

**Langkah-langkah:**
1. Buat folder kerja **di mana saja** (misal: `D:\Tugas\PPD\Pertemuan-5\` atau `D:\Tugas\JaringanKomputer\Pertemuan-1\`).
2. Di dalamnya, siapkan:
   - `inisiasi.txt` — Catatan ringkas penjelasan Anda tentang alur praktikum dan tiap nomor screenshot.
   - Folder `gambar/` — Berkas screenshot bernomor (`1.png`, `2.png`, `T1.png`, dst).
   - (Opsional) Modul praktikum (PDF/PPT) pertemuan terkait.
3. Buka workspace di folder tersebut, lalu panggil:
   > `/make-laprak buatkan laporan [NAMA_MATKUL], saya sudah siapkan inisiasi.txt dan folder gambar`
4. *Catatan Mode Universal:* Jika mata kuliah Anda belum terdaftar di plugin, AI akan menanyakan kelengkapan identitas (Nama, NIM, Dosen, Topik) di Tahap 1 sebelum melanjutkan ke penyusunan kerangka.

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
2. **Kustomisasi Khusus (Matkul Baru Permanen):** Jika ada gaya penulisan khusus yang ingin dijadikan standar permanen:
   - Buat sub-folder di `skills/make-laprak/matkul/<NAMA_MATKUL>/` dan letakkan file `.tex` contoh.
   - Jalankan `/breakdown-matkul` untuk membentuk pedoman `<NAMA_MATKUL>.md`.

## 7. Dokumentasi & Kontribusi

- 📂 Repositori: [github.com/AcademyCity-RND/MyLaprak](https://github.com/AcademyCity-RND/MyLaprak)
- 📝 Panduan kontribusi: lihat file `CONTRIBUTING.md` di repositori.
