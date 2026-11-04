# Pedoman Penulisan Laporan Mata Kuliah KEPL

Dokumen ini adalah panduan **wajib baca** bagi AI sebelum menyusun Laporan Praktikum KEPL (Konstruksi dan Evolusi Perangkat Lunak). Panduan diekstrak secara kumulatif dari 5 laporan riil: `KEPL1.tex` (Pertemuan 1), `KEPL2.tex` (Pertemuan 2), `KEPL3.tex` (Pertemuan 3), `KEPL4.tex` (Pertemuan 4), dan `KEPL5.tex` (Pertemuan 5).

> **ATURAN UTAMA:** Jangan mengarang format sendiri. Ikuti pola di bawah ini secara ketat. Gaya pada laporan terbaru (`KEPL5.tex`) adalah standar acuan mutakhir.

---

## 1. Struktur Bab (Wajib, Urut)

Setiap laporan praktikum KEPL memiliki hierarki bab utama sebagai berikut:

```latex
\chapter{Dasar Teori}
\chapter{Hasil dan Pembahasan}
\chapter{Kesimpulan}
\chapter{Daftar Pustaka}
```

### Aturan Hierarki & Pemisah Halaman:
- Di dalam setiap `\chapter`, gunakan `\section`, `\subsection`, dan (jika perlu) `\subsubsection` secara terstruktur.
- **WAJIB** gunakan `\clearpage` di antara `\section` besar (atau sebelum `\subsection` baru jika halaman sebelumnya padat dengan `figure`) agar gambar tidak menumpuk atau bergeser tak beraturan ke halaman berikutnya.
- Di awal `\section` yang kompleks (misalnya alur multi-lingkungan CI/CD, restrukturisasi arsitektur sistem, atau konfigurasi pipeline), sediakan 1 paragraf narasi pengantar sebelum langsung memecah ke `\subsection`.
- **Troubleshooting / Penanganan Isu:** Jika dalam praktikum terdapat kendala teknis, peringatan linter (*warning*), atau galat konfigurasi, buatkan `\subsection` khusus (misal: `\subsection{Troubleshooting dan Penanganan Isu ...}`) yang memaparkan akar masalah teknis beserta solusi implementasinya secara analitis.

---

## 2. Dasar Teori

- **Gaya Bahasa:** Ditulis akademis, analitis, naratif, padat, mendalam, dan *to the point*.
- **Pembagian Topik:** Dibagi per pilar konsep teknologi utama menggunakan `\section` dan `\subsection`.
- **Daftar Komponen / Parameter:** Ketika menjelaskan komponen bertahap (seperti *builder stage* vs *runtime stage*) atau parameter konfigurasi (seperti parameter probe `HEALTHCHECK`), gunakan `\begin{itemize}` dengan label tebal, misalnya:
  ```latex
  \begin{itemize}
      \item \textbf{Tahap Pembangun (\textit{Builder Stage}):} Dikonfigurasi dengan...
      \item \texttt{--interval}: Jarak waktu antar-pengujian (misalnya setiap 15 detik).
  \end{itemize}
  ```
- **Wajib Ilustrasi Gambar:** Setiap konsep teoretis utama **WAJIB** disertai gambar/diagram ilustrasi konsep (arsitektur sistem, alur *layer caching*, perbandingan VM vs kontainer, diagram alur *multi-stage build*, alur pipeline CI/CD).
  - Lebar gambar diagram teori berkisar antara `0.6\textwidth` hingga `0.7\textwidth` (rata-rata `0.65\textwidth`).
- **Sitasi Ilmiah:** **WAJIB** menyertakan sitasi ilmiah di dalam teks narasi menggunakan format `[\ref{label}]` (mengacu ke `\chapter{Daftar Pustaka}`), mencakup buku teks standar industri, publikasi NIST/standar keamanan, atau dokumentasi resmi vendor/framework.
- **Format Istilah & Kode:**
  - Istilah asing/teknis: `\textit{...}` (*italic*), misal `\textit{multi-stage build}`, `\textit{least privilege}`, `\textit{attack surface}`.
  - Perintah, nama berkas, ekstensi, variabel lingkungan: `\texttt{...}` (*monospace*), misal `\texttt{Dockerfile}`, `\texttt{php:8.3-cli-alpine}`, `\texttt{packages: write}`.

---

## 3. Hasil dan Pembahasan — Tata Letak Gambar

Penyusunan gambar dan pembahasannya adalah bagian paling krusial. Terdapat 3 gaya teruji, dengan **Gaya C** sebagai standar paling mutakhir dan dominan pada KEPL3, KEPL4, dan KEPL5:

### Gaya C — Naratif Individual (Standar Utama KEPL3, KEPL4, & KEPL5) — **DIREKOMENDASIKAN**
Cocok untuk: Mayoritas langkah praktikum di mana setiap gambar memerlukan ulasan teknis, penjelasan konfigurasi, instruksi CLI, atau analisis log sebelum pembaca melihat visualisasinya.

```latex
\subsection{Definisi Stage Builder (composer:2.7)}
Tahap pertama didefinisikan sebagai \textit{stage} \texttt{builder} menggunakan \textit{base image} resmi \texttt{composer:2.7}... (penjelasan naratif mendalam mencakup argumen perintah, flag optimasi, dan alasan arsitektural)...

\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{1.png}
    \caption{Konfigurasi tahap pertama (builder) pada Dockerfile berbasis image composer:2.7}
\end{figure}
```

**Aturan Gaya C:**
- Penjelasan ditulis **sebelum** blok `\begin{figure}[H]`, bukan setelahnya.
- Narasi harus komprehensif: sebutkan perintah lengkap (CLI), flag/parameter yang digunakan, serta arti dari hasil yang ditampilkan pada gambar.
- Setiap gambar berdiri sendiri dalam blok `figure` dengan posisi `[H]`.

---

### Gaya B — Naratif Berpasangan / Dikelompokkan (KEPL2, KEPL4, & KEPL5)
Cocok untuk: Dua gambar berurutan yang saling membuktikan atau berkaitan erat (misalnya: eksekusi di terminal CLI lalu diverifikasi di GUI Docker Desktop, atau dialog tinjauan *review deployment* yang berpasangan dengan status checks).

```latex
\subsection{Validasi Pipeline CI/CD dan Deployment Environment Protection}
Saat PR digabungkan ke \textit{branch} \texttt{main}, GitHub Actions secara otomatis memicu alur kerja...

\begin{figure}[H]
    \centering
    \includegraphics[width=0.9\textwidth]{12.png}
    \caption{Tampilan ringkasan checks pada branch main: 8 checks sukses dan 1 check rilis produksi menunggu persetujuan}

    \vspace{0.5cm}

    \includegraphics[width=0.9\textwidth]{13.png}
    \caption{Modal antarmuka Review pending deployments untuk otorisasi manual rilis ke lingkungan production}
\end{figure}
```

**Aturan Gaya B:**
- Maksimal 2 gambar dalam satu `\begin{figure}[H]`.
- Gambar dipisahkan dengan jeda vertikal `\vspace{0.5cm}`.
- Masing-masing gambar memiliki `\caption` sendiri.
- Penjelasan naratif ditaruh di awal subsection sebelum blok figure.

---

### Gaya A — Analitis Poin per Poin (KEPL1)
Cocok untuk: Gambar tunggal yang memerlukan inspeksi baris demi baris atau analisis konfigurasi/error yang sangat rinci dalam bentuk *bullet points*.

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.6\textwidth]{gambar.png}
    \caption{Judul Gambar}
    \label{fig:label}
\end{figure}
Penjelasan Gambar:
\begin{itemize}
    \item Poin analisis pertama: konfigurasi baris X berfungsi untuk...
    \item Poin analisis kedua: parameter Y memastikan...
\end{itemize}
```

**Aturan Gaya A:**
- Frasa `Penjelasan Gambar:` (tanpa bold/italic) ditulis tepat di bawah `\end{figure}`.
- Diikuti oleh lingkungan `\begin{itemize}`.
- Hanya digunakan jika konteks benar-benar memerlukan breakdown poin analitis granular.

---

### Gambar Komposit / Perbandingan (Side-by-Side Dual Window)
Jika gambar merupakan tangkapan komposit dari dua lingkungan (misal: perbandingan antarmuka repo pribadi dan repo organisasi):
1. **Model Pre-stitched (Standar Dominan KEPL4 & KEPL5):** Gambar disatukan sebelumnya dalam 1 berkas gambar berorientasi lanskap lebar (`0.9\textwidth`), dengan caption yang merinci kedua sisi:
   ```latex
   \begin{figure}[H]
       \centering
       \includegraphics[width=0.9\textwidth]{10.png}
       \caption{Pull Request \#15 integrasi fitur Tugas 5 dari branch feature ke dev (Kiri: repo pribadi, Kanan: repo KEPL2026)}
   \end{figure}
   ```
2. **Model Minipage (Side-by-Side LaTeX):**
   ```latex
   \begin{figure}[H]
       \centering
       \begin{minipage}[b]{0.48\textwidth}
           \centering
           \includegraphics[width=\textwidth]{gambar_kiri.png}
       \end{minipage}
       \hfill
       \begin{minipage}[b]{0.48\textwidth}
           \centering
           \includegraphics[width=\textwidth]{gambar_kanan.png}
       \end{minipage}
       \caption{Judul Gabungan (Kiri: Kondisi A, Kanan: Kondisi B)}
   \end{figure}
   ```

---

### Analisis Kuantitatif & Komparasi Matematis (Pola Baru KEPL5)
Jika praktikum melibatkan perbandingan efisiensi (misal: ukuran citra *before* vs *after*, memori, latensi, atau durasi build), sajikan data menggunakan lingkungan matematika LaTeX:
- **Format Desimal:** Gunakan koma kurung kurawal `{,}` agar spasi matematika tidak merenggang, contoh: `$949{,}94\text{ MB}$`, `$\mathbf{64{,}55\%}$`.
- **Selisih Penurunan:**
  `$$949{,}94\text{ MB} - 336{,}72\text{ MB} = \mathbf{613{,}22\text{ MB}}$$`
- **Rumus Persentase (Display Math):**
  $$\frac{613{,}22\text{ MB}}{949{,}94\text{ MB}} \times 100\% = \mathbf{64{,}55\%}$$
- Strukturkan perbandingan dalam `\begin{enumerate}` dengan sub-item `\begin{itemize}` yang merinci kondisi sebelum, sesudah, selisih penghematan, dan persentase efisiensi.

---

### Panduan Pemilihan Lebar Gambar

| Jenis Konten Visual | Rekomendasi Lebar | Contoh / Bukti |
|---|---|---|
| Diagram Teori / Arsitektur Konsep | `0.6\textwidth` – `0.7\textwidth` | Arsitektur multi-stage (`0.65\textwidth`), Keamanan non-root (`0.6\textwidth`), GHCR pipeline (`0.7\textwidth`) |
| Cuplikan Berkas Konfigurasi / Kode Pendek | `0.55\textwidth` – `0.6\textwidth` | `Dockerfile` stage builder & runtime (`0.55\textwidth`), `.dockerignore` (`0.5\textwidth`) |
| Cuplikan Workflow YAML / Linter Warning | `0.65\textwidth` – `0.7\textwidth` | `docker-publish.yml` (`0.7\textwidth`), Warning `env.IMAGE_NAME` (`0.65\textwidth`) |
| Log Terminal / Build CLI / Command Output | `0.8\textwidth` – `0.85\textwidth` | Log `docker build` (`0.8\textwidth`), `docker images` CLI (`0.85\textwidth`) |
| GUI Desktop / Browser / Dual-Repo / Full-Width UI | `0.9\textwidth` | Docker Desktop Images/Builds (`0.9\textwidth`), Pull Request Dual Window (`0.9\textwidth`), GHCR Package (`0.9\textwidth`) |

---

## 4. Kesimpulan

Format kesimpulan wajib mengikuti konvensi berikut:
1. **Kalimat Pembuka Standar:**
   ```latex
   \chapter{Kesimpulan}
   Berdasarkan praktikum mengenai [Topik Bahasan] yang telah dilakukan, dapat ditarik beberapa kesimpulan utama sebagai berikut:
   \begin{enumerate}
       \item ...
       \item ...
   \end{enumerate}
   ```
2. **Karakteristik Poin-poin:**
   - Gunakan `\begin{enumerate}` dengan penomoran angka.
   - Poin kesimpulan harus **kritis, substantif, dan berbasis data empiris praktikum**. Hindari kesimpulan normatif/generik seperti *"praktikan berhasil memahami Docker"*.
   - **WAJIB sertakan angka/data kuantitatif spesifik** dari hasil praktikum:
     - Efisiensi ukuran citra (misal: ruang disk terpangkas dari 949,94 MB menjadi 336,72 MB atau hemat `64,55%`; ukuran konten turun dari 234 MB ke 64,9 MB atau reduksi `72,26%`).
     - Durasi build / execution time (misal: 189,9 detik pada *cold build* vs 1,4 detik pada *cache hit*; test suite selesai dalam 50 detik).
     - Identitas pengguna runtime (`whoami` menampilkan `www-data` bukan `root`).
     - Konfigurasi parameter keandalan (`HEALTHCHECK` interval 15 detik pada rute `/up` berstatus `Up (healthy)`).
     - Konfigurasi CI/CD & Gating (izin `packages: write`, penandaan commit SHA, 8 checks sukses dan 1 check rilis produksi memerlukan *manual approval*).
   - Gunakan sub-item `\begin{itemize}` di dalam `\item` kesimpulan apabila merangkum perbandingan metrik multi-kategori (misal: disk usage vs content size).

---

## 5. Tautan Repositori & Artefak Rilis

Repositori kode sumber dan artefak paket dicantumkan pada **DUA tempat**:

1. **Sebagai `\section` terpisah di akhir `\chapter{Hasil dan Pembahasan}`:**
   Judul section: `\section{Tautan Repositori Kode Sumber dan Registry Package}` (atau Tautan Repositori Kode Sumber).
   ```latex
   \section{Tautan Repositori Kode Sumber dan Registry Package}

   Seluruh berkas konfigurasi, kode program aplikasi, dan artefak kontainer praktikum ini tersedia secara terbuka pada tautan berikut:
   \begin{itemize}
       \item Repositori Matkul KEPL2026 (v1):\\
       \url{https://github.com/KEPL2026/nama-repo-v1}

       \item Repositori Pribadi AcademyCity-RND (v2 - GitHub Actions Active):\\
       \url{https://github.com/AcademyCity-RND/nama-repo-v2}

       \item Halaman Paket GitHub Container Registry (GHCR):\\
       \url{https://github.com/AcademyCity-RND/nama-repo-v2/pkgs/container/nama-package}
   \end{itemize}
   ```

2. **Sebagai item penutup di `\chapter{Daftar Pustaka}`:**
   ```latex
   \item \label{sourcecode} Tautan Repositori Kode Sumber dan Paket Publik:
   \begin{itemize}
       \item Repositori Matkul KEPL2026 (v1):\\
       \url{https://github.com/KEPL2026/...}
       \item Repositori Pribadi AcademyCity-RND (v2 - GitHub Actions Active):\\
       \url{https://github.com/AcademyCity-RND/...}
       \item Paket GitHub Container Registry (GHCR):\\
       \url{https://github.com/AcademyCity-RND/.../pkgs/container/...}
   \end{itemize}
   ```

---

## 6. Daftar Pustaka

### Format Standar Mutakhir: Enumerate + `\label` + `\mbox{[Online]. Tersedia:}` (KEPL2 – KEPL5) — **WAJIB**
```latex
\chapter{Daftar Pustaka}

\begin{enumerate}
    \item \label{turnbull_docker} J. Turnbull. \textit{The Docker Book: Containerization Is the New Virtualization}. James Turnbull, 2014. \mbox{[Online]. Tersedia:} \url{https://www.dockerbook.com/}

    \item \label{docker_multistage} Docker, Inc. \textit{Multi-stage builds: Use multi-stage builds}. Docker Documentation, 2024. \mbox{[Online]. Tersedia:} \url{https://docs.docker.com/build/building/multi-stage/}

    \item \label{nist_container} M. Souppaya, J. Morello, \& K. Scarfone. \textit{Application Container Security Guide}. NIST Special Publication 800-190, National Institute of Standards and Technology, 2017. \mbox{[Online]. Tersedia:} \url{https://doi.org/10.6028/NIST.SP.800-190}

    \item \label{ghcr_docs} GitHub, Inc. \textit{Working with the Container Registry (GHCR)}. GitHub Docs, 2024. \mbox{[Online]. Tersedia:} \url{https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry}

    \item \label{sourcecode} Tautan Repositori Kode Sumber dan Paket Publik:
    \begin{itemize}
        \item Repositori Matkul KEPL2026 (v1):\\
        \url{https://github.com/KEPL2026/...}
        \item Repositori Pribadi AcademyCity-RND (v2 - GitHub Actions Active):\\
        \url{https://github.com/AcademyCity-RND/...}
        \item Paket GitHub Container Registry (GHCR):\\
        \url{https://github.com/AcademyCity-RND/.../pkgs/container/...}
    \end{itemize}
\end{enumerate}
```

- **Panggilan di Teks:** Menggunakan `[\ref{label}]`, contoh: `...menghasilkan efisiensi yang signifikan [\ref{docker_multistage}].`
- **Pencegahan Line Break:** Gunakan `\mbox{[Online]. Tersedia:}` agar frasa keterangan online tidak terpotong ke baris baru secara canggung.
- **Pola Penulisan Sumber Online:**
  `Penulis/Organisasi. \textit{Judul Dokumen/Artikel}. Penerbit/Platform/Publikasi, Tahun. \mbox{[Online]. Tersedia:} \url{URL}`

---

## 7. Konvensi Penulisan LaTeX

- **Istilah Asing:** `\textit{...}` — misal `\textit{multi-stage build}`, `\textit{single-stage build}`, `\textit{least privilege}`, `\textit{runner}`, `\textit{detached mode}`.
- **Nama Berkas, Perintah, Endpoint, Branch, Scope:** `\texttt{...}` — misal `\texttt{Dockerfile}`, `\texttt{docker build}`, `\texttt{packages: write}`, `\texttt{USER www-data}`, `\texttt{main}`.
- **Blok Perintah Panjang Terpusat:** Untuk perintah unduhan terminal yang panjang (seperti pull image dengan SHA lengkap), gunakan lingkungan `center`:
  ```latex
  \begin{center}
  \texttt{docker pull ghcr.io/academycity-rnd/\allowbreak evolusi-pl-24-542159-sv-25009-v2:\allowbreak ddc450a5143d842c62bdf70693dcf1ed08512c7b}
  \end{center}
  ```
- **URL & Endpoint Panjang di Teks:** Gunakan `\allowbreak` pada setiap garis miring agar teks tidak *overflow* margin dokumen:
  `\texttt{http://localhost:8000/\allowbreak api/portfolios}` atau berkas `\texttt{.github/workflows/\allowbreak docker-publish.yml}`.
- **Karakter Khusus (Escape):**
  - Underscore: `\_` (misal `\texttt{docker\_publish}`, `\texttt{pdo\_mysql}`).
  - Ampersand: `\&` (misal `Automated Unit \& Feature Tests`).
  - Dolar: `\$` (misal `\texttt{\$GITHUB\_ENV}`, `\texttt{\$\{\{ github.sha \}\}}`).
- **Penulisan Notasi Matematika:** Format desimal Indonesia menggunakan tanda kurung kurawal `{,}` (misal `$613{,}22\text{ MB}$` dan `$\mathbf{64{,}55\%}$`).
- **Posisi Gambar:** Semua blok `figure` wajib mencantumkan penempatan mutlak `[H]`.
- **Kerapian Layout:** Pasang `\clearpage` sebelum pergantian section utama atau sebelum bab baru agar dokumen terstruktur rapi tanpa penumpukan *floating figure*.

---

## 8. Instruksi Adaptasi untuk AI (`make-laprak`)

Saat AI menyusun laporan praktikum KEPL:
1. **Analisis Inisiasi & Gambar:** Pelajari `inisiasi.txt` dan cocokkan setiap nomor screenshot ke alur logis praktikum (konfigurasi $\to$ build CLI $\to$ verifikasi runtime/keamanan $\to$ alur GitHub/CI-CD $\to$ rilis/deployment).
2. **Prioritaskan Gaya C:** Susun pembahasan dengan narasi teknis komprehensif di paragraf sebelum gambar. Jelaskan perintah, flag, argumen, dan interpretasi output.
3. **Gunakan Gaya B secara Selektif:** Jika ada 2 gambar yang berpasangan erat (misal: status checks pipeline + dialog manual approval, atau inisiasi build + log penyelesaian build), kelompokkan dalam satu figure dengan `\vspace{0.5cm}`.
4. **Proporsi Gambar yang Presisi:** Ikuti tabel rekomendasi lebar (misal screenshot dual repo / Docker Desktop `0.9\textwidth`, terminal log `0.8\textwidth`–`0.85\textwidth`, diagram teori `0.65\textwidth`, berkas konfigurasi `0.55\textwidth`).
5. **Kalkulasi Metrik & Matematika:** Jika praktikum membandingkan efisiensi performa atau ukuran citra, hitung selisih dan persentase efisiensi secara matematis menggunakan format math LaTeX (`{,}` dan `\frac{...}{...}`).
6. **Dokumentasikan Troubleshooting:** Sertakan analisis akar masalah teknis dan solusinya apabila terdapat error atau warning linter pada alur praktikum.
7. **Kerapian Bab & Section:** Sisipkan `\clearpage` antar section besar agar kompilasi PDF rapi tanpa penumpukan gambar di dasar halaman.
8. **Kesimpulan Berbasis Data Empiris:** Ekstrak durasi waktu, status kode, versi library, hash komit, dan metrik kuantitatif dari screenshot/teks untuk dimasukkan ke poin kesimpulan.
9. **Pustaka & Sitasi:** Selalu gunakan format Enumerate dengan sitasi `[\ref{...}]`, `\mbox{[Online]. Tersedia:} \url{...}`, dan cantumkan tautan repo serta registry publik pada section akhir Hasil Pembahasan dan entri terakhir Daftar Pustaka.
