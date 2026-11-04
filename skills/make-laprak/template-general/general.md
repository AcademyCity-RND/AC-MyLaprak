# Pedoman Penulisan Laporan Praktikum Universal (General Template)

Dokumen ini adalah panduan **wajib baca** bagi AI sebelum menyusun Laporan Praktikum untuk mata kuliah apa pun yang **belum memiliki** pedoman spesifik di folder `matkul/`. Panduan ini dirancang secara komprehensif, universal, dan fleksibel berdasarkan sintesis standar pelaporan terbaik dari 5 laporan riil (`ref1.tex` s.d. `ref5.tex`).

> **ATURAN UTAMA:** Jika mata kuliah yang diminta pengguna belum terdaftar di `skills/make-laprak/matkul/`, AI **WAJIB** menggunakan pedoman `general.md` ini dan memanfaatkan berkas acuan di `template-general/`.

---

## 0. Protokol Prasyarat: Pengumpulan Metadata & Konteks (Tahap 0)

Sebelum memulai penyusunan kerangka (Outline) pada laporan mata kuliah umum, AI **WAJIB** memastikan kelengkapan data administratif dan preferensi teknis pengguna.

### Informasi yang Wajib Dikumpulkan / Dikonfirmasi:
1. **Identitas Mahasiswa:**
   - Nama Lengkap (misal: `Hilarius Christiano Avin Paliling`)
   - NIM (misal: `24/542159/SV/25009`)
   - Kelas / Rombel (misal: `PL5B1`)
2. **Informasi Mata Kuliah & Praktikum:**
   - Nama Lengkap Mata Kuliah (misal: `Praktikum Penambangan Data`, `Rekayasa Perangkat Lunak`, dll)
   - Pertemuan ke-berapa (misal: `Pertemuan 1`)
   - Topik / Judul Praktikum (misal: `Pengenalan Lingkungan dan Manipulasi Data`)
   - Nama Dosen Pengampu & Tim Asisten Praktikum
3. **Identitas Institusi:**
   - Program Studi (default: `D-IV TEKNOLOGI REKAYASA PERANGKAT LUNAK`)
   - Departemen (default: `DEPARTEMEN TEKNIK ELEKTRO DAN INFORMATIKA`)
   - Fakultas / Sekolah (default: `SEKOLAH VOKASI`)
   - Universitas (default: `UNIVERSITAS GADJAH MADA`)
   - Kota & Tahun (default: `YOGYAKARTA`, `2026`)
4. **Pilihan Format Luaran Dokumen:**
   - **Mode Monolitik (Default):** Seluruh laporan dihasilkan dalam satu file `.tex` utuh (menggunakan basis `template-master.tex`).
   - **Mode Modular:** Laporan dipecah menjadi file per-bab yang dipanggil menggunakan `\input{...}` atau `\include{...}`.
5. **Pemeriksaan Kelengkapan Bahan Praktikum:**
   - Berkas `inisiasi.txt` (catatan alur langkah dan penomoran gambar).
   - Folder tangkapan layar/screenshot (biasanya di `gambar/`).
   - (Opsional) Berkas modul praktikum (PDF/PPT/Word) jika pengguna menyediakannya.

> **ATURAN TAHAP 0:** Jika pengguna belum menyebutkan identitas di atas pada pesan awal atau `inisiasi.txt`, tanyakan secara sopan dan terstruktur dalam bentuk form ringkas pada respon pertama sebelum masuk ke Tahap 2 (Outline).

---

## 1. Struktur Bab Standar (Wajib, Urut)

Setiap laporan praktikum berbasis template universal memiliki hierarki bab utama berikut:

```latex
\chapter{Tujuan Praktikum}
\chapter{Dasar Teori}
\chapter{Hasil dan Pembahasan}
  \section{Hasil Praktikum}
  \clearpage
  \section{Tugas Praktikum}
\chapter{Kesimpulan}
\chapter{Daftar Pustaka}
```

### Aturan Hierarki & Pemisah Halaman:
1. **Bab Utama:** Selalu gunakan `\chapter{Hasil dan Pembahasan}` untuk mendokumentasikan kegiatan praktikum.
2. **Dua Section Wajib:** Di dalam bab Hasil dan Pembahasan, **WAJIB** terbagi menjadi:
   - `\section{Hasil Praktikum}`: Dokumentasi panduan modul praktikum / hands-on terbimbing.
   - `\section{Tugas Praktikum}`: Dokumentasi tugas mandiri / studi kasus penugasan tambahan.
3. **Pemisah `\clearpage`:**
   - **WAJIB** menyisipkan `\clearpage` tepat sebelum `\section{Tugas Praktikum}`.
   - Disarankan menyisipkan `\clearpage` sebelum evaluasi performa model / rangkuman metrik atau transisi antar tugas mandiri.
4. **Komentar Pembatas (Banner Comments):**
   ```latex
   % ==========================================
   % NAMA SECTION
   % ==========================================
   ```
   dan
   ```latex
   % ------------------------------------------
   % NAMA SUBSECTION / SUBSUBSECTION
   % ------------------------------------------
   ```

---

## 2. Tujuan Praktikum & Dasar Teori

### A. Tujuan Praktikum
- Menggunakan lingkungan `\begin{enumerate}` dengan 3–5 poin capaian kompetensi.
- Ditulis menggunakan kata kerja operasional terukur (misal: *Mahasiswa mampu memahami...*, *Mahasiswa dapat mengimplementasikan...*, *Mahasiswa mampu menganalisis...*).

### B. Dasar Teori (Naratif, Komparatif, dan Matematis)
- Ditulis analitis dalam bahasa Indonesia baku yang mengalir, bukan sekadar kutipan definisi singkat.
- Bedah kelebihan, kelemahan, serta *trade-off* teknis dari metode/alat/pustaka yang digunakan.
- **Persamaan Matematika:** Bila topik melibatkan rumus atau metrik numerik, **WAJIB** menggunakan lingkungan `\begin{equation} ... \end{equation}` lengkap dengan keterangan variabelnya (`Dimana: \begin{itemize} ... \end{itemize}`).
- **Ilustrasi Konseptual:** Boleh menyertakan diagram konsep/arsitektur dengan lebar `0.5\textwidth` – `0.65\textwidth` (posisi `[H]`) disertai caption ilmiah dan sumber sitasi.
- **Sitasi Wajib:** Setiap klaim ilmiah dan definisi wajib disitasi menggunakan format `[\ref{label}]`.

---

## 3. Hasil dan Pembahasan — Tata Letak Gambar

Dokumentasikan setiap langkah kerja secara sistematis dengan orientasi pada **Source Code (Input)** dan **Luaran / Tampilan Antarmuka (Output)**.

Gunakan 5 gaya tata letak gambar berikut sesuai karakteristik materi:

---

### Gaya 1 — Modular Inset List (Tahapan Eksplorasi Bertahap)
Cocok untuk rangkaian inspeksi data atau eksekusi fungsi berseri:
```latex
\subsection{Pemeriksaan Struktur Data}
\begin{itemize}
    \item \textbf{Inspeksi Baris dan Kolom (Input \& Output):} 
    \begin{figure}[H]
        \centering
        \includegraphics[width=0.75\textwidth]{3.png}
        \caption{Output Pemeriksaan Sampel Data}
        \label{fig:3}
    \end{figure}
    \begin{itemize}
        \item \textbf{df.head():} Menampilkan 5 baris data teratas untuk mengamati struktur nilai awal.
        \item \textbf{df.info():} Memeriksa tipe data masing-masing kolom serta mendeteksi nilai kosong.
    \end{itemize}
\end{itemize}
```

---

### Gaya 2 — Gambar Tunggal + Penjelasan Input & Output (Standar Dominan)
Paling sering digunakan untuk satu langkah kode atau satu keluaran spesifik:
```latex
\subsection{Inisialisasi Lingkungan dan Import Library}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{1.png}
    \caption{Source Code Import Library}
    \label{fig:1}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Input:} Mengimpor pustaka dasar manipulasi data (\texttt{numpy}, \texttt{pandas}) dan modul visualisasi (\texttt{matplotlib.pyplot}).
    \item \textbf{Output:} Seluruh dependensi berhasil dimuat ke dalam memori sesi kerja tanpa kendala.
\end{itemize}
```

---

### Gaya 3 — Berpasangan Code + Output Terpisah
Digunakan jika tangkapan layar kode dan tangkapan layar output disimpan dalam 2 file terpisah:
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.6\textwidth]{2.png}
    \caption{Source Code Pemuatan Data}
    \label{fig:2}
    
    \vspace{0.2cm}
    
    \includegraphics[width=0.8\textwidth]{3.png}
    \caption{Output Pemuatan Data}
    \label{fig:3}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Input:} Membaca berkas data menggunakan fungsi pembacaan tabel dan menetapkan indeks.
    \item \textbf{Output:} Menampilkan log konfirmasi pemuatan dan dimensi ukuran baris serta kolom tabel.
\end{itemize}
```

---

### Gaya 4 — Minipage Komparasi Side-by-Side (Berdampingan Horisontal)
Digunakan untuk membandingkan 2 atau 3 grafik/output secara sejajar:
```latex
\begin{figure}[H]
    \centering
    \begin{minipage}{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T1.png}
        \caption{Visualisasi Metode A}
        \label{fig:t1}
    \end{minipage}\hfill
    \begin{minipage}{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T2.png}
        \caption{Visualisasi Metode B}
        \label{fig:t2}
    \end{minipage}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Output:} Perbandingan hasil grafik antara Metode A dan Metode B pada himpunan data uji yang sama.
\end{itemize}
```

---

### Gaya 5 — Stacked Sub-figures Vertikal dengan Spasi (Sub-langkah Berpasangan)
Digunakan ketika dua sub-tahapan yang berkaitan erat ditampilkan bertumpuk vertikal dalam satu blok `figure [H]`:
```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.50\textwidth]{T1-8a.png}
    \caption{Plot Visualisasi Model A}
    \label{fig:t1_8a}
    
    \vspace{0.2cm}
    
    \includegraphics[width=0.50\textwidth]{T1-8b.png}
    \caption{Plot Visualisasi Model B}
    \label{fig:t1_8b}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Input:} Perintah plotting kurva perbandingan untuk mengevaluasi respons model terhadap data aktual.
    \item \textbf{Output:} Gambar \ref{fig:t1_8a} memperlihatkan adaptasi Model A yang stabil. Gambar \ref{fig:t1_8b} memperlihatkan respons Model B yang cenderung fluktuatif pada nilai ekstrem.
\end{itemize}
```

---

### Panduan Lebar Gambar (`width=...`)

| Jenis Konten Tangkapan Layar | Rentang Lebar | Rekomendasi |
|---|---|---|
| **Kode Ringkas / Pustaka / Fungsi Tunggal** | `0.35\textwidth` - `0.55\textwidth` | `0.55\textwidth` |
| **Kode Kompleks / Full Pipeline** | `0.65\textwidth` - `0.80\textwidth` | `0.75\textwidth` |
| **Output Ramping / Log Terminal / Nilai Array** | `0.30\textwidth` - `0.45\textwidth` | `0.35\textwidth` |
| **Output Tabel Lebar / DataFrame Preview** | `0.80\textwidth` - `0.90\textwidth` | `0.85\textwidth` |
| **Plot Distribusi / Grafik Standar Tunggal** | `0.55\textwidth` - `0.70\textwidth` | `0.65\textwidth` |
| **Plot Komparasi Bertumpuk Vertikal (Gaya 5)** | `0.45\textwidth` - `0.55\textwidth` | `0.50\textwidth` |
| **Minipage Berdampingan (2 Kolom)** | `0.45\textwidth` per minipage | `width=\textwidth` di dalam |
| **Minipage Berdampingan (3 Kolom)** | `0.32\textwidth` per minipage | `width=\textwidth` di dalam |
| **Diagram Konsep Dasar Teori** | `0.50\textwidth` - `0.65\textwidth` | `0.60\textwidth` |

---

## 4. Konvensi Penamaan Berkas Gambar & Label

1. **Hasil Praktikum:**
   - Berkas: `1.png`, `2.png`, atau bertingkat `2a.png`, `2b.png`, dst.
   - Label: `\label{fig:1}`, `\label{fig:2}`, `\label{fig:2a}`, dst.
2. **Tugas Praktikum:**
   - **Tugas Tunggal:** Gunakan awalan `T`: `T1.png`, `T2.png`, dst.
   - **Multi-Tugas:** Gunakan awalan hierarkis `T[NomorTugas]-[NomorLangkah][Sub].png` (misal: `T1-1.png`, `T1-2a.png`, `T2-1.png`).
3. **Caption Standar:**
   - `\caption{Source Code [Aktivitas]}` untuk screenshot kode.
   - `\caption{Output [Aktivitas]}` atau `\caption{Plot [Nama Grafik]}` untuk screenshot hasil luaran.
   - `\caption{Source Code dan Output [Aktivitas]}` jika menyatu.

---

## 5. Khusus: Struktur Bagian "Tugas Praktikum"

1. **Pemisah Wajib:**
   ```latex
   % ==========================================
   % TUGAS PRAKTIKUM
   % ==========================================
   \clearpage
   \section{Tugas Praktikum}
   ```
2. **Sub-langkah Terstruktur:**
   Setiap tugas mandiri disusun sistematis (misal via `\subsection` atau `\subsubsection`):
   - Deskripsi Masalah / Persiapan Data
   - Prapemrosesan / Konfigurasi
   - Eksekusi / Implementasi Solusi
   - Visualisasi / Pengujian
   - Evaluasi Hasil
3. **Analisis Komparatif (Jika Ada Perbandingan Kasus/Model):**
   Sediakan sub-bab perbandingan analitis di akhir tugas praktikum untuk membedah kelebihan, kelemahan, dan wawasan teknis substantif.

---

## 6. Kesimpulan

Format kesimpulan menggunakan lingkungan `\begin{enumerate}` dengan 4–5 poin substantif:

```latex
\chapter{Kesimpulan}
\label{chap:kesimpulan}
Berdasarkan praktikum mengenai [Topik Praktikum] yang telah dilaksanakan—[keterangan ruang lingkup eksperimen terbimbing dan tugas mandiri]—diperoleh beberapa simpulan penting sebagai berikut:

\begin{enumerate}
    \item \textbf{Efektivitas Metode/Teknologi yang Diterapkan:} [Penjelasan analisis penerapan metode/alat utama]...
    
    \item \textbf{Performa dan Perbandingan Hasil:} [Evaluasi hasil komparasi solusi atau algoritma yang diuji]...
    
    \item \textbf{Kendala Teknis dan Mitigasi:} [Ulasan kendala seperti overfitting, keterbatasan data, atau galat sistem beserta solusinya]...
    
    \item \textbf{Relevansi dan Manfaat Praktis:} [Refleksi manfaat luaran praktikum terhadap kebutuhan riil rekayasa perangkat lunak / data]...
\end{enumerate}
```

---

## 7. Tautan Repositori & Source Code

Tautan repositori (GitHub / GitLab / Google Colab) mahasiswa **TIDAK** diletakkan sebagai bab tersendiri, melainkan dicantumkan sebagai salah satu entri di dalam `\chapter{Daftar Pustaka}` dengan format:

```latex
\item \label{sourceCode} [Nama Mahasiswa], \textit{[Kode/Identitas Repositori Laporan Praktikum]}. [Online]. Tersedia: \url{https://...}.
```

---

## 8. Daftar Pustaka

Menggunakan lingkungan `\begin{enumerate}` dengan label `\item \label{...}` dan disitasi di teks dengan `[\ref{...}]`:

```latex
\chapter{Daftar Pustaka}
\begin{enumerate}
    \item \label{modulPraktikum} [Nama Dosen Pengampu dan Tim Asisten]. \textit{Modul Praktikum [Nama Mata Kuliah]: [Topik Pertemuan]}. Yogyakarta: Departemen Teknik Elektro dan Informatika, Sekolah Vokasi, Universitas Gadjah Mada, [Tahun].
    
    \item \label{bukuTeks} [Penulis Buku]. \textit{[Judul Buku]}, [Edisi] ed. [Kota Terbit]: [Penerbit], [Tahun].
    
    \item \label{jurnalIlmiah} [Penulis Artikel], "[Judul Artikel]," \textit{[Nama Jurnal]}, vol. [x], no. [y], pp. [xxx--xxx], [Tahun]. [Online]. Tersedia: \url{https://doi.org/...}.
    
    \item \label{sumberDataset} [Penyedia/Kaggle], \textit{[Nama Dataset]}. [Tahun]. [Online]. Tersedia: \url{https://...}.
    
    \item \label{sourceCode} [Nama Mahasiswa], \textit{[Kode Praktikum (Source Code)]}. Google Colaboratory / GitHub, [Tahun]. [Online]. Tersedia: \url{https://...}.
\end{enumerate}
```

---

## 9. Konvensi Penulisan LaTeX

1. **Monospace (`\texttt{...}`):** Nama pustaka, fungsi, class, parameter, nama file, dan perintah terminal.
2. **Italic (`\textit{...}`):** Istilah bahasa asing, konsep teknis khusus, dan nama terbitan jurnal.
3. **Escape Characters:** Karakter `\_` (underscore pada variabel/nama fungsi), `\%` (persen nilai numerik), dan `\&` (ampersand pada teks) **WAJIB** di-escape.
4. **Notasi Matematika:** Gunakan mode inline `$x$` untuk variabel dan lingkungan `\begin{equation}` untuk rumus penting.
5. **Posisi Figure:** Semua figure **WAJIB** menggunakan opsi `[H]` agar posisi presisi pada urutan dokumen.

---

## 10. Panduan Berkas Template `.tex` di `template-general/`

Direktori `template-general/` menyediakan dua pendekatan implementasi:

1. **Pendekatan Monolitik (`template-master.tex`):**
   - Berisi satu dokumen utuh dari `\documentclass` hingga `\end{document}`.
   - Cocok untuk laporan ringkas hingga menengah yang mudah dikelola dalam satu file.
2. **Pendekatan Modular (Pecahan per-Bab):**
   - `template-dependencies-dan-style.tex`: Preamble, paket, konfigurasi style kode & margin.
   - `template-tujuanpraktikum.tex`: Bab Tujuan Praktikum.
   - `template-dasarteori.tex`: Bab Dasar Teori.
   - `template-hasilpembahasan.tex`: Bab Hasil dan Pembahasan.
   - `template-kesimpulan.tex`: Bab Kesimpulan.
   - `template-daftarpustaka.tex`: Bab Daftar Pustaka.
   - Dipanggil oleh master menggunakan `\input{...}`.

---

## 11. Instruksi Adaptasi untuk AI (`make-laprak`)

Saat menggunakan template universal ini:
1. **Lakukan Pre-Flight Check:** Konfirmasi identitas mahasiswa, mata kuliah, dosen pengampu, dan topik sebelum masuk ke pembuatan outline.
2. **Gunakan Gaya Bahasa Akademis & Analitis:** Jangan sekadar menyebutkan judul screenshot; selalu jelaskan maksud input dan makna output secara komprehensif.
3. **Jaga Konsistensi Nomor Gambar:** Sesuaikan nomor pada `\includegraphics` dan `\caption` dengan catatan pada `inisiasi.txt`.
4. **Auto-generate Berkas Fisik `.tex`:** Di tahap finalisasi (Tahap 4), langsung buatkan file `.tex` siap kompilasi di folder kerja pengguna.
