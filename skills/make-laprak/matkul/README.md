# `matkul/` — Pedoman Gaya Matkul (LOKAL, tidak dipush)

Folder ini **sengaja kosong di repositori publik**. Sejak v0.3.0, gaya penulisan
matkul (KEPL, PPD, PPG, PBO, dst.) adalah **milik user** dan dibuat di mesin
masing-masing — bukan bawaan plugin yang ikut ter-clone.

Isi folder ini diabaikan Git (kecuali `.gitkeep` dan README ini). Jadi, laporan
riil atau template pribadi Anda **tidak akan pernah masuk commit** selama aturan
`.gitignore` di root repo dipertahankan.

## Cara membuat gaya matkul sendiri

1. Siapkan folder kerja pertemuan, lalu taruh minimal satu laporan contoh yang
   sudah disetujui di `<folder kerja>/_contoh/` (mis. `_contoh/PBO1.tex`).
   - **Jangan** menaruh `.tex` riil di folder plugin ini.
   - File contoh sebaiknya sudah dianonimkan (nama, NIM, dll. dihapus).
2. Panggil `/breakdown-matkul` pada folder kerja tersebut. Skill akan membaca
   `_contoh/*.tex` dan menulis hasilnya ke folder **lokal** ini:
   ```
   skills/make-laprak/matkul/<NAMA_MATKUL>/
   ├── <NAMA_MATKUL>.md          ← pedoman formatting (dipakai /make-laprak)
   └── template-<NAMA_MATKUL>.tex ← template placeholder (privasi aman)
   ```
3. Panggil `/make-laprak`. Jika `matkul/<NAMA_MATKUL>/` ada, skill memakai gaya
   Anda (Mode A). Jika tidak ada, skill memakai `template-general/` (Mode B).

## Catatan

- Clone bersih = hanya Mode B yang aktif. Mode A baru aktif setelah Anda
  menjalankan `/breakdown-matkul` sendiri. Ini disengaja agar repo publik bebas
  dari data dan gaya pribadi siapa pun.
- Ingin berbagi gaya ke komunitas? Jangan push `.tex` riil. Bagikan `_contoh/`
  yang sudah dianonimkan lewat issue/PR, lalu orang lain menjalankan
  `/breakdown-matkul` di mesin mereka.
- Lihat `CONTRIBUTING.md` di root repo untuk detail kontribusi dan template
  pedoman `.md`.
