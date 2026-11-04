# Pedoman Penulisan Laporan Mata Kuliah PPD

Dokumen ini adalah panduan **wajib baca** bagi AI sebelum menyusun Laporan Praktikum PPD (Praktikum Penambangan Data). Panduan diekstrak secara kumulatif dan komprehensif dari 5 laporan riil:
- `PPD1.tex` (Pertemuan 1: Dasar NumPy dan Pandas, 103 figur)
- `PPD2.tex` (Pertemuan 2: Exploratory Data Analysis & Data Preprocessing, 62 figur)
- `PPD3.tex` (Pertemuan 3: Classification — LogReg, KNN, Decision Tree, Random Forest, AdaBoost, Confusion Matrix, 33 figur)
- `PPD4.tex` (Pertemuan 4: Regression — Linear Regression, Decision Tree, Random Forest, Evaluasi RMSE & $R^2$, 34 figur)
- `PPD5.tex` (Pertemuan 5: Time Series Forecasting — Sliding Window, Rekayasa Fitur Statistik, MLP, KNN, Decision Tree, Random Forest, Evaluasi RMSE & Korelasi Pearson $r$, 23 figur kombinasi)

> **ATURAN UTAMA:** Jangan mengarang format sendiri. Ikuti pola di bawah ini secara ketat. Gaya pada laporan terbaru (`PPD5.tex`, `PPD4.tex`, dan `PPD3.tex`) adalah standar acuan mutakhir.

---

## 1. Struktur Bab (Wajib, Urut)

Setiap laporan praktikum PPD **WAJIB** memiliki hierarki bab utama berikut:

```latex
\chapter{Dasar Teori}
\chapter{Hasil dan Pembahasan}
  \section{Hasil Praktikum}
  \clearpage
  \section{Tugas Praktikum}
\chapter{Kesimpulan}
\chapter{Daftar Pustaka}
```

### Aturan Hierarki & Pemisah Halaman:
1. **Bab Utama Selalu Sama:** Selalu gunakan `\chapter{Hasil dan Pembahasan}` (bukan "Dokumentasi Praktikum").
2. **Dua Section Wajib:** Di dalam `\chapter{Hasil dan Pembahasan}`, **WAJIB** terbagi menjadi 2 bagian besar:
   - `\section{Hasil Praktikum}`: Dokumentasi panduan modul terbimbing / langkah hands-on.
   - `\section{Tugas Praktikum}`: Penyelesaian studi kasus mandiri / penugasan dataset baru.
3. **Pemisah `\clearpage`:**
   - **WAJIB** menyisipkan `\clearpage` tepat sebelum `\section{Tugas Praktikum}` agar alur penugasan mandiri dimulai rapi pada halaman baru.
   - Disarankan menyisipkan `\clearpage` sebelum evaluasi performa model (`\subsection{Evaluasi Performa Model}`) atau sebelum transisi antar tugas besar (`\subsection{Tugas 2: ...}`) agar tabel/grafik metrik tidak terpotong canggung antar halaman.
4. **Komentar Pemisah (Banner Comments):** Kode LaTeX selalu menggunakan banner komentar untuk menandai batas bab dan section:
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

## 2. Dasar Teori

Dasar Teori pada PPD memiliki standar penulisan akademis, analitis, mendalam, dan terstruktur secara matematis:

### A. Gaya Bahasa & Kedalaman Konten
- Ditulis analitis dalam bahasa Indonesia baku yang mengalir, bukan sekadar rangkuman definisi singkat.
- Wajib membedah kelebihan, kelemahan, serta trade-off teknis dari algoritma/metode:
  - *NumPy vs Pandas:* efisiensi alokasi memori berbaris vs pengindeksan berbasis label.
  - *Decision Tree vs Random Forest:* kerentanan partisi ortogonal pohon tunggal terhadap *overfitting* vs pereduksian variansi dan derau melalui agregasi ansambel (*bagging*).
  - *KNN:* keterbatasan ekstrapolasi (*extrapolation limitation*) pada deret waktu bernilai di luar rentang data historis.
  - *Multilayer Perceptron (MLP):* fleksibilitas aproksimasi fungsi non-linear kontinu melalui propagasi balik (*backpropagation*).
  - *Pencegahan Data Leakage:* pentingnya pembagian data kronologis berurutan (`shuffle=False`) pada data sekuensial temporal.
- Setiap konsep utama dibahas dalam `\section` terpisah, dan sub-metode/metrik evaluasi dipecah dalam `\subsection` atau `\begin{enumerate}` dengan judul poin tebal `\textbf{...}`.

### B. Persamaan Matematika (Equations)
Bila materi praktikum melibatkan rumus, transformasi data, atau metrik evaluasi numerik, **WAJIB** menyertakan persamaan matematis menggunakan lingkungan `\begin{equation} ... \end{equation}` beserta rincian variabelnya:

1. **Metode Sliding Window (PPD5):**
   ```latex
   \begin{equation}
       X_i = [s_i, s_{i+1}, \dots, s_{i+n\_steps\_in-1}], \quad y_i = s_{i+n\_steps\_in+n\_steps\_out-1}
   \end{equation}
   ```

2. **Root Mean Squared Error / RMSE (PPD4, PPD5):**
   ```latex
   \begin{equation}
       RMSE = \sqrt{\frac{1}{n}\sum_{i=1}^{n}\left(y_{i} - \hat{y}_{i}\right)^2}
   \end{equation}
   ```

3. **Pearson Correlation Coefficient / $r$ (PPD5):**
   ```latex
   \begin{equation}
       r = \frac{\sum_{i=1}^{n}(y_{i} - \bar{y})(\hat{y}_{i} - \bar{\hat{y}})}{\sqrt{\sum_{i=1}^{n}(y_{i} - \bar{y})^2 \sum_{i=1}^{n}(\hat{y}_{i} - \bar{\hat{y}})^2}}
   \end{equation}
   ```

4. **Regresi Linier Berganda (PPD4):**
   ```latex
   \begin{equation}
       y = b_0 + b_1x_1 + b_2x_2 + \dots + b_nx_n
   \end{equation}
   ```
   Dimana:
   ```latex
   \begin{itemize}
       \item $y$ = target/prediksi
       \item $b_0$ = \textit{intercept} (nilai dasar)
       \item $b_n$ = koefisien regresi
       \item $x_n$ = nilai fitur
   \end{itemize}
   ```

5. **Akurasi & F1-Score Klasifikasi (PPD3):**
   ```latex
   \begin{equation}
       Accuracy = \frac{TP + TN}{TP + TN + FP + FN}
   \end{equation}
   ```
   ```latex
   \begin{equation}
       F1\text{-}Score = 2 \times \frac{Precision \times Recall}{Precision + Recall}
   \end{equation}
   ```

### C. Ekstraksi Fitur & Transformasi Data
Jika materi mencakup rekayasa fitur (seperti ekstraksi fitur statistik deret waktu pada PPD5), jabarkan indikator spesifik yang dihitung menggunakan `\begin{itemize}`:
- Nilai minimum (`min`) dan maksimum (`max`).
- Rentang selisih (`diff` = $\max - \min$).
- Standar deviasi (`std`) dan rata-rata aritmatika (`mean`).
- Nilai tengah (`median`).
- Keruncingan distribusi (`kurtosis`) dan kemiringan distribusi (`skewness`).

### D. Ilustrasi Gambar di Dasar Teori
- Pada materi konseptual/arsitektural, Dasar Teori boleh menyertakan gambar pendukung (diagram alur, taksonomi ML, diagram EDA, arsitektur array).
- Lebar gambar diagram teori: `0.5\textwidth` hingga `0.65\textwidth` (posisi `[H]`).
- Caption wajib mencantumkan sumber referensi: `\caption{... (Sumber: [\ref{label}])}` atau deskripsi ilmiah konsep.

### E. Sitasi Wajib
- Seluruh klaim konsep, modul, dan definisi algoritma **WAJIB** disitasi ke daftar pustaka menggunakan format `[\ref{label}]` (seperti `[\ref{modulPraktikum}]`, `[\ref{retnoningsih}]`, `[\ref{chai}]`, `[\ref{benesty}]`, `[\ref{geron}]`).

---

## 3. Hasil dan Pembahasan — Tata Letak Gambar

PPD adalah matkul berbasis komputasi data (Google Colab / Jupyter Notebook). Penyajian gambar berorientasi pada **Source Code (Input)** dan **Luaran/Grafik/Tabel (Output)**.

Terdapat 5 gaya tata letak yang ditemukan di seluruh referensi:

---

### Gaya 1 — Modular Inset List (Standar PPD4) — **DIREKOMENDASIKAN UNTUK EDA BERTAHAP**
Digunakan untuk mengelompokkan beberapa sub-langkah yang saling berkaitan erat (seperti rangkaian inspeksi EDA atau tahapan eksekusi model) di dalam satu list `itemize`:

```latex
\subsection{Exploratory Data Analysis}
\begin{itemize}
    \item \textbf{EDA (Input \& Output):} 
    \begin{figure}[H]
        \centering
        \includegraphics[width=0.8\textwidth]{3.png}
        \caption{Output Exploratory Data Analysis}
        \label{fig:3}
    \end{figure}
    \begin{itemize}
        \item \textbf{df head:} Memanggil dan menampilkan 5 sampel baris teratas dari dataset harga rumah.
        \item \textbf{df tail:} Memanggil dan menampilkan 5 sampel baris terbawah.
        \item \textbf{df describe:} Memanggil dan mencetak ringkasan nilai statistik dari semua atribut numerik.
    \end{itemize}

    \item \textbf{Histogram (Input \& Output):}
    \begin{figure}[H]
        \centering
        \includegraphics[width=0.7\textwidth]{4.png}
        \caption{Plot Histogram}
        \label{fig:4}
    \end{figure}
    Menjalankan perintah pembuatan histogram dan menampilkan kumpulan grafik distribusi frekuensi dari tiap variabel numerik.
\end{itemize}
```

---

### Gaya 2 — Gambar Tunggal + Penjelasan Input & Output (Standar Dominan PPD2, PPD3, PPD4, PPD5)
Digunakan saat satu tangkapan layar memuat satu fungsi kode atau luaran spesifik:

```latex
\subsection{Import Library}
\begin{figure}[H]
    \centering
    \includegraphics[width=0.55\textwidth]{1.png}
    \caption{Source Code Import Library}
    \label{fig:1}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Input:} Mengimpor pustaka dasar manipulasi data (\texttt{numpy}, \texttt{pandas}), pustaka visualisasi grafik (\texttt{matplotlib.pyplot}), modul regresi dari \texttt{sklearn}, serta fungsi statistik pendukung.
    \item \textbf{Output:} Seluruh pustaka berhasil dimuat ke dalam memori lingkungan kerja Google Colab tanpa terjadi kesalahan dependensi.
\end{itemize}
```

---

### Gaya 3 — Berpasangan Code + Output Terpisah (Dominan PPD1, PPD2)
Digunakan jika gambar tangkapan layar kode dan gambar keluaran/tabel dipisah menjadi 2 berkas yang berbeda:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.6\textwidth]{2.png}
    \caption{Source Code Load dataset}
    \label{fig:2}
    
    \vspace{0.2cm}
    
    \includegraphics[width=0.8\textwidth]{3.png}
    \caption{Output Load dataset}
    \label{fig:3}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Input:} Mengunduh dataset melalui pustaka \texttt{gdown} dan membacanya ke dalam \texttt{DataFrame}.
    \item \textbf{Output:} Menampilkan log terminal pengunduhan 100\% serta ukuran dimensi tabel data (\texttt{df.shape}).
\end{itemize}
```

---

### Gaya 4 — Minipage Komparasi Side-by-Side (Standar PPD3)
Digunakan khusus untuk membandingkan output visual antar model secara sejajar, misalnya matriks konfusi (*Confusion Matrix*) atau diagram metrik:

#### Format 2 Kolom (2 Model Berdampingan):
```latex
\begin{figure}[H]
    \centering
    \begin{minipage}{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T13.png}
        \caption{CM Logistic Regression}
        \label{fig:t13}
    \end{minipage}\hfill
    \begin{minipage}{0.45\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T14.png}
        \caption{CM K-Nearest Neighbors}
        \label{fig:t14}
    \end{minipage}
\end{figure}
```

#### Format 3 Kolom (3 Model Berdampingan):
```latex
\begin{figure}[H]
    \centering
    \begin{minipage}{0.32\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T15.png}
        \caption{CM Decision Tree}
        \label{fig:t15}
    \end{minipage}\hfill
    \begin{minipage}{0.32\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T16.png}
        \caption{CM Random Forest}
        \label{fig:t16}
    \end{minipage}\hfill
    \begin{minipage}{0.32\textwidth}
        \centering
        \includegraphics[width=\textwidth]{T17.png}
        \caption{CM AdaBoost}
        \label{fig:t17}
    \end{minipage}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Output:} Matriks plot \textit{Confusion Matrix} hasil prediksi masing-masing algoritma klasifikasi dalam mendeteksi True Positive, True Negative, False Positive, dan False Negative pada data uji.
\end{itemize}
```

---

### Gaya 5 — Stacked Sub-figures Vertikal dengan Spasi (Standar Baru PPD5) — **DIREKOMENDASIKAN UNTUK SUB-LANGKAH/MODEL BERPASANGAN**
Digunakan saat menampilkan dua sub-langkah yang saling melengkapi (misal load dataset + ekstraksi target, verifikasi matriks + plot tren, atau plot prediksi model berpasangan) dalam satu blok lingkungan figure tunggal:

```latex
\begin{figure}[H]
    \centering
    \includegraphics[width=0.50\textwidth]{T1-8a.png}
    \caption{Plot Visualisasi Hasil Prediksi Model MLP dan KNN pada Tugas 1}
    \label{fig:t1_8a}
    
    \vspace{0.1cm} % atau 0.3cm
    
    \includegraphics[width=0.50\textwidth]{T1-8b.png}
    \caption{Plot Visualisasi Hasil Prediksi Model DT dan RF pada Tugas 1}
    \label{fig:t1_8b}
\end{figure}
Penjelasan Gambar :
\begin{itemize}
    \item \textbf{Input:} Perintah plotting kurva deret waktu harga penutupan riil bersanding dengan estimasi model MLP dan KNN (Gambar \ref{fig:t1_8a}), serta model Decision Tree dan Random Forest (Gambar \ref{fig:t1_8b}).
    \item \textbf{Output:} Gambar \ref{fig:t1_8a} memperlihatkan kurva MLP dan KNN yang mampu mengikuti pergerakan umum harga saham. Gambar \ref{fig:t1_8b} menunjukkan bahwa Random Forest menghasilkan kurva prediksi yang paling mulus dan konsisten mendekati data aktual dibandingkan Decision Tree yang memiliki deviasi tajam pada titik balik pasar.
\end{itemize}
```

*Catatan:* Pada Gaya 5, setiap sub-figur memiliki `\caption` dan `\label` sendiri. Uraian pada `Penjelasan Gambar :` secara eksplisit membedah Gambar `\ref{fig:...a}` dan `\ref{fig:...b}`.

---

### Panduan Lebar Gambar (`width=...`)

Gunakan panduan lebar berikut berdasarkan tipe visualisasi:

| Jenis Konten Tangkapan Layar | Rentang Lebar | Rekomendasi | Contoh Konten |
|---|---|---|---|
| **Kode Ringkas / Pustaka** | `0.35\textwidth` - `0.55\textwidth` | `0.55\textwidth` | Import library, load dataset ringkas, isolasi fitur |
| **Kode Fungsi / Pipeline / Windowing** | `0.40\textwidth` - `0.65\textwidth` | `0.55\textwidth` | Fungsi `split_sequences`, `stats_features`, training loops |
| **Kode Kompleks / Full Workflow** | `0.7\textwidth` - `0.8\textwidth` | `0.8\textwidth` | Loop pemodelan masif, fungsi evaluasi lengkap |
| **Output Ramping / Log Bentuk Matriks** | `0.3\textwidth` - `0.45\textwidth` | `0.35\textwidth` | Verifikasi shape array, `df.shape`, sampel baris ringkas |
| **Output Tabel Lebar** | `0.8\textwidth` - `0.9\textwidth` | `0.85\textwidth` | Pratinjau `df.head()`, `df.tail()`, `df.describe()` |
| **Plot Distribusi / Grafik Standar** | `0.55\textwidth` - `0.7\textwidth` | `0.6\textwidth` | Histogram, Scatter Plot, Plot Historis Deret Waktu |
| **Plot Prediksi Kurva Deret Waktu (Stacked)** | `0.50\textwidth` - `0.55\textwidth` | `0.50\textwidth` | Perbandingan grafik Real vs Prediksi (2 kurva per baris) |
| **Output Log Evaluasi Metrik** | `0.55\textwidth` - `0.65\textwidth` | `0.6\textwidth` | Log cetak RMSE, Pearson $r$, MAE, atau tabel evaluasi |
| **Tabel Rekapitulasi Performa Model** | `0.85\textwidth` - `0.95\textwidth` | `0.9\textwidth` | Ringkasan DataFrame evaluasi semua model penantang |
| **Minipage Side-by-Side (2 Kolom)** | `0.45\textwidth` per minipage | `width=\textwidth` di dalam | Confusion Matrix 2 model berdampingan |
| **Minipage Side-by-Side (3 Kolom)** | `0.32\textwidth` per minipage | `width=\textwidth` di dalam | Confusion Matrix 3 model berdampingan |
| **Diagram Konsep Dasar Teori** | `0.5\textwidth` - `0.65\textwidth` | `0.6\textwidth` | Taksonomi ML, diagram sliding window, alur preprocessing |

---

## 4. Konvensi Penamaan Gambar & Label

1. **Hasil Praktikum:**
   - Berkas: `1.png`, `2a.png`, `2b.png`, `3.png`, `4.png`, `5a.png`, ...
   - Label: `\label{fig:1}`, `\label{fig:2a}`, `\label{fig:2b}`, `\label{fig:3}`, ...
2. **Tugas Praktikum:**
   - **Kasus A: Tugas Tunggal (Standar PPD3 & PPD4):**
     - Berkas: Menggunakan prefiks `T`: `T1.png`, `T2.png`, `T3.png`, ...
     - Label: `\label{fig:t1}`, `\label{fig:t2}`, `\label{fig:t3}`, ...
   - **Kasus B: Multi-Tugas / Beberapa Studi Kasus (Standar Mutakhir PPD5):**
     - Berkas: Menggunakan prefiks hierarkis tugas `T[NomorTugas]-[NomorLangkah][Sub].png`:
       - Tugas 1: `T1-1,2a.png` (label `\label{fig:t1_1}`), `T1-2b.png`, `T1-3,4.png`, `T1-5a.png`, `T1-5b.png`, `T1-5c.png`, `T1-6.png`, `T1-7.png`, `T1-8a.png`, `T1-8b.png`, `T1-9.png`.
       - Tugas 2: `T2-1.png` (label `\label{fig:t2_1}`), `T2-2,3.png`, `T2-4,5.png`, `T2-6.png`, `T2-7a.png`, `T2-7b.png`, `T2-8.png`.
   - *Penting:* Jangan melanjutkan nomor akhir dari Hasil Praktikum di Tugas Praktikum. Gunakan selalu awalan `T` atau `T[N]-`.
3. **Dasar Teori (jika ada gambar ilustrasi):**
   - Menggunakan berkas khusus (misal `101.png`, `60.jpg`, atau `21.png`).
4. **Caption Standar:**
   - `\caption{Source Code [Aktivitas]}` untuk screenshot kode.
   - `\caption{Output [Aktivitas]}` atau `\caption{Plot [Nama Grafik]}` untuk screenshot output/visualisasi.
   - `\caption{Source Code dan Output [Aktivitas]}` jika keduanya berada dalam satu gambar.

---

## 5. Khusus: Struktur Bagian "Tugas Praktikum"

Tugas Praktikum pada mata kuliah PPD menuntut jawaban analitis terhadap studi kasus dataset baru. Struktur `\section{Tugas Praktikum}` wajib mengikuti pola komprehensif berikut:

1. **Pemisah Halaman Wajib:**
   ```latex
   % ==========================================
   % TUGAS PRAKTIKUM
   % ==========================================
   \clearpage
   \section{Tugas Praktikum}
   ```

2. **Pembagian Berdasarkan Jumlah Tugas:**
   - **Jika Satu Penugasan Mandiri (Pola PPD3 & PPD4):**
     Langsung susun dalam `\subsection` terstruktur: Deskripsi Dataset/Tujuan Atribut, Korelasi Fitur, Prapemrosesan, Pemodelan, Tabel Performa, dan Pembahasan Model Terbaik.
   - **Jika Beberapa Studi Kasus / Multi-Tugas (Pola PPD5):**
     Bagi menjadi sub-bab per penugasan:
     - `\subsection{Tugas 1: [Judul Studi Kasus 1, misal: Univariat Target Close]}`
     - `\subsection{Tugas 2: [Judul Studi Kasus 2, misal: Multivariat Target Close + Open]}`

3. **Sub-langkah Terstandarisasi per Tugas (Menggunakan `\subsubsection`):**
   Pada setiap penugasan mandiri (seperti terlihat pada PPD5), terapkan alur teknis yang konsisten:
   - `\subsubsection{Import Library dan Pemuatan Dataset [Nama Dataset]}`
   - `\subsubsection{Penyesuaian Format Data / Isolasi Fitur}`
   - `\subsubsection{Implementasi Prapemrosesan / Sliding Window / Fitur Statistik}`
   - `\subsubsection{Prapemrosesan Data dan Pembagian Dataset}`
   - `\subsubsection{Pelatihan Model Machine Learning}`
   - `\subsubsection{Pengujian dan Prediksi}`
   - `\subsubsection{Visualisasi Hasil Prediksi Model}`
   - `\subsubsection{Evaluasi Performa Model [Tugas N]}`

4. **Wajib: Analisis Komparatif (PPD5):**
   Jika terdapat beberapa perlakuan tugas (misal perbandingan univariat vs multivariat, atau perbandingan antar kelompok fitur), **WAJIB** menyertakan sub-bab perbandingan analitis di akhir penugasan:
   ```latex
   \subsection{Analisis Komparatif: Dampak [Faktor Perbedaan, misal: Penambahan Fitur Open] (Tugas 1 vs Tugas 2)}
   \begin{enumerate}
       \item \textbf{Pengayaan Informasi Pasar / Data:} [Analisis keuntungan informasional dari fitur tambahan]...
       \item \textbf{Stabilitas Prediksi Algoritma Ensemble:} [Analisis mengapa Random Forest / model ensemble lebih tangguh memanfaatkan fitur tambahan]...
       \item \textbf{Kelemahan Model Kaku:} [Analisis mengapa Decision Tree tunggal atau KNN tetap mengalami kendala]...
   \end{enumerate}
   ```

---

## 6. Kesimpulan

Format kesimpulan PPD telah stabil dan terbukti sangat konsisten sejak PPD2 hingga PPD5:

```latex
\chapter{Kesimpulan}
\label{chap:kesimpulan}
Berdasarkan praktikum mengenai [Topik Praktikum] berbasis [paradigma/metode] yang telah dilaksanakan—[keterangan ruang lingkup eksperimen pada bagian Hasil Praktikum dan studi kasus Tugas Praktikum]—diperoleh beberapa simpulan penting sebagai berikut:

\begin{enumerate}
    \item \textbf{Efektivitas Rekayasa Fitur / Data Preprocessing:} [Penjelasan analisis prapemrosesan, sliding window, scaling, atau ekstraksi fitur statistik lokal]...
    
    \item \textbf{Keunggulan Algoritma Ensemble dan Jaringan Saraf Tiruan:} [Komparasi performa model terunggul seperti Random Forest atau MLP dalam menangkap tren/pola non-linear]...
    
    \item \textbf{Kelemahan Inheren Model Pohon Keputusan Tunggal dan Pembanding:} [Ulasan spesifik mengenai kerentanan overfitting Decision Tree atau keterbatasan ekstrapolasi KNN]...
    
    \item \textbf{Dampak Positif Eksplorasi Fitur / Multi-Variabel:} [Temuan empiris dari perbandingan perlakuan fitur pada Tugas Praktikum]...
    
    \item \textbf{Pentingnya Kombinasi Metrik Evaluasi Komplementer:} [Refleksi penggunaan kombinasi metrik numerik dan arah tren, misal RMSE dan Pearson Correlation r, atau RMSE dan R^2]...
\end{enumerate}
```

### Aturan Kesimpulan:
- **Tepat 4–5 Poin:** Menggunakan lingkungan `\begin{enumerate}` (bukan `itemize`).
- **Judul Poin Tebal:** Setiap item **WAJIB** diawali frasa judul tebal `\item \textbf{Judul Poin / Aspek Analisis:}`.
- **Kedalaman Reflektif:** Mengulas wawasan teknis substantif dari hasil pengujian data riil, bukan sekadar rangkuman mekanis aktivitas praktikum.

---

## 7. Tautan Repositori & Source Code

Berbeda dengan beberapa matkul lain yang memiliki section repositori khusus, pada PPD tautan repositori/Google Colab **TIDAK** diletakkan sebagai bab terpisah. 

Tautan kode notebook mahasiswa **WAJIB** dicantumkan sebagai salah satu entri di dalam `\chapter{Daftar Pustaka}` dengan format:

```latex
\item \label{colabLaporan} H. C. A. Paliling, \textit{S5-PPD-542159 (Source Code Laporan Praktikum Pertemuan [X] - [Topik])}. Google Colaboratory, 2026. [Online]. Tersedia: \url{https://colab.research.google.com/drive/...}.
```

---

## 8. Daftar Pustaka

### Format Wajib
Menggunakan format penomoran `\begin{enumerate}` dengan label `\label{...}`, yang dipanggil di dalam teks menggunakan `[\ref{...}]`:

```latex
\chapter{Daftar Pustaka}
\begin{enumerate}
    \item \label{modulPraktikum} Dr. Eng. Ir. Ganjar Alfian, S.T., M. Eng., dan Tim Asisten. \textit{Modul Praktikum Penambangan Data: Pertemuan [X] [Topik]}. Yogyakarta: Departemen Teknik Elektro dan Informatika, Sekolah Vokasi, Universitas Gadjah Mada, [Tahun].
    
    \item \label{jurnalSatu} E. Retnoningsih and R. Pramudita, "Mengenal Machine Learning Dengan Teknik Supervised dan Unsupervised Learning Menggunakan Python," \textit{Bina Insani ICT Journal}, vol. 7, no. 2, pp. 156--165, 2020. [Online]. Tersedia: \url{https://doi.org/...}.
    
    \item \label{jurnalDua} T. Chai and R. R. Draxler, "Root mean square error (RMSE) or mean absolute error (MAE)? Arguments against avoiding RMSE in the literature," \textit{Geoscientific Model Development}, vol. 7, no. 3, pp. 1247--1250, 2014. Tersedia: \url{https://doi.org/...}.
    
    \item \label{bukuReferensi} J. Benesty, J. Chen, Y. Huang, and I. Cohen, "Pearson Correlation Coefficient," in \textit{Noise Reduction in Speech Processing}, Berlin, Heidelberg: Springer, 2009, pp. 1--4. [Online]. Tersedia: \url{https://doi.org/...}.
    
    \item \label{kaggleDataset} [Nama Pembuat], \textit{[Nama Dataset]}. Kaggle, [Tahun]. [Online]. Tersedia: \url{https://www.kaggle.com/datasets/...}.
    
    \item \label{colabLaporan} H. C. A. Paliling, \textit{S5-PPD-542159 (Source Code Laporan Praktikum Pertemuan [X] - [Topik])}. Google Colaboratory, 2026. [Online]. Tersedia: \url{https://colab.research.google.com/drive/...}.
\end{enumerate}
```

### Entri Standar yang Selalu Muncul:
1. **Modul Praktikum PPD:** Dosen pengampu `Dr. Eng. Ir. Ganjar Alfian, S.T., M. Eng., dan Tim Asisten`, instansi `Departemen Teknik Elektro dan Informatika, Sekolah Vokasi, Universitas Gadjah Mada`.
2. **Artikel Jurnal Ilmiah (IEEE Format):** Penulis, judul dalam tanda kutip `"..."`, nama jurnal `\textit{...}`, volume, nomor, halaman, tahun, dan link DOI `\url{...}`.
3. **Pustaka Klasik / Buku Teks:** Buku acuan Data Science & ML (Wes McKinney, Aurélien Géron, Bishop, Springer).
4. **Tautan Kaggle:** Sumber dataset tugas praktikum yang digunakan.
5. **Google Colab Mahasiswa:** Identitas `H. C. A. Paliling`, kode `S5-PPD-542159`.

---

## 9. Konvensi Penulisan LaTeX

1. **Monospace (`\texttt{...}`):**
   - Nama library: `\texttt{pandas}`, `\texttt{numpy}`, `\texttt{scikit-learn}`, `\texttt{scipy.stats}`.
   - Nama fungsi/metode: `\texttt{df.head()}`, `\texttt{train\_test\_split}`, `\texttt{split\_sequences}`, `\texttt{stats\_features}`, `\texttt{fit()}`, `\texttt{predict()}`, `\texttt{pearsonr}`.
   - Nama class model: `\texttt{MLPRegressor}`, `\texttt{KNeighborsRegressor}`, `\texttt{DecisionTreeRegressor}`, `\texttt{RandomForestRegressor}`, `\texttt{StandardScaler}`.
   - Nama parameter kode: `\texttt{shuffle=False}`, `\texttt{n\_steps\_in}`, `\texttt{n\_steps\_out}`, `\texttt{random\_state=42}`.
   - Nama kolom/variabel kode: `\texttt{cnt}`, `\texttt{Close}`, `\texttt{Open}`, `\texttt{Date}`, `\texttt{price}`, `\texttt{min}`, `\texttt{max}`, `\texttt{std}`, `\texttt{mean}`.
   - Nama file/ekstensi: `\texttt{bikesharing\_day.csv}`, `\texttt{TSLA.csv}`, `\texttt{kc\_house\_data.csv}`.
2. **Italic (`\textit{...}`):**
   - Istilah bahasa asing/teknis: `\textit{machine learning}`, `\textit{supervised learning}`, `\textit{time series}`, `\textit{forecasting}`, `\textit{sliding window}`, `\textit{stride}`, `\textit{data leakage}`, `\textit{lag}`, `\textit{feedforward artificial neural network}`, `\textit{hidden layers}`, `\textit{backpropagation}`, `\textit{instance-based learning}`, `\textit{Euclidean distance}`, `\textit{ensemble learning}`, `\textit{bagging}`, `\textit{bootstrap aggregating}`, `\textit{noise}`, `\textit{overfitting}`, `\textit{seasonality}`, `\textit{bullish}`, `\textit{step-like function}`, `\textit{price surge}`, `\textit{feature bagging}`, `\textit{orthogonal splits}`, `\textit{extrapolation limitation}`.
3. **Karakter Escape Khusus:**
   - **Underscore (`\_`):** Sangat sering muncul di kode Python dan parameter, **WAJIB** di-escape (contoh: `n\_steps\_in`, `n\_steps\_out`, `train\_test\_split`, `random\_state=42`, `df\_churning`).
   - **Persen (`\%`):** Nilai persentase wajib di-escape (contoh: `80\%`, `20\%`, `100\%`).
   - **Ampersand (`\&`):** Digunakan pada label `\textbf{Input \& Output:}`.
4. **Notasi Matematika:**
   - Variabel temporal: `$t$`, `$t-1$`, `$t+1$`, `$t+2$`, `$t+h$`.
   - Simbol metrik & korelasi: `$r$`, `$R^2$`, `$RMSE$`, `$y_i$`, `$\hat{y}_i$`.
   - Pertidaksamaan: `$r > 0.95$`, `$0 \le R^2 \le 1$`.
5. **Posisi Figure:** Semua figure **WAJIB** menggunakan penempatan `[H]`.

---

## 10. Evolusi Gaya (PPD1 → PPD2 → PPD3 → PPD4 → PPD5)

- **PPD1 (Dasar Manipulasi Array & Dataframe):**
  - Jumlah gambar sangat masif (103 figur) karena hampir setiap eksekusi dipisah menjadi gambar kode dan gambar output.
  - Penomoran gambar tugas bersambung langsung dari nomor hasil praktikum (`95.png`).
  - Label keterangan masih bervariasi (`Penjelasan Kode :`).
- **PPD2 (EDA & Preprocessing):**
  - Gambar mulai diefisienkan (62 figur). Tangkapan layar yang menyatukan kode dan output mulai digunakan (`Source Code dan Output ...`).
  - Tugas praktikum diberi penomoran blok baru mulai `50.png`.
  - Label keterangan stabil menjadi `Penjelasan Gambar :`.
- **PPD3 (Klasifikasi):**
  - Jumlah gambar menjadi sangat efisien dan terfokus (33 figur).
  - Mulai menggunakan prefiks `T` untuk seluruh gambar Tugas Praktikum (`T1.png` – `T18.png`).
  - Memperkenalkan teknik perbandingan side-by-side menggunakan lingkungan `minipage` untuk matriks konfusi (*Confusion Matrix*).
- **PPD4 (Regresi):**
  - Struktur paling terorganisir dan matang (34 figur).
  - Menerapkan Gaya 1 (Modular Inset List) untuk langkah-langkah EDA dan pengujian model.
  - Dasar Teori diperkaya dengan rumus matematika komprehensif (`equation`) dan penjabaran variabel.
  - Tugas praktikum terstruktur rapi: menjawab pertanyaan analitis dataset, korelasi fitur, tabel komparasi performa, dan justifikasi model terbaik.
- **PPD5 (Time Series Forecasting — Standar Mutakhir):**
  - Jumlah gambar semakin ringkas dan efisien (23 figur kombinasi).
  - Memperkenalkan skema penamaan multi-penugasan hierarkis: `T1-X` untuk Tugas 1 dan `T2-X` untuk Tugas 2.
  - Mengadopsi Gaya 5 (*Stacked Sub-figures* Vertikal dengan `\vspace{0.1cm}` hingga `0.3cm`) di dalam satu blok `figure [H]` untuk sub-langkah berpasangan (misal load data + target, verifikasi + plot tren, kurva prediksi model).
  - Penjelasan gambar (`Penjelasan Gambar :`) membedah secara spesifik peran masing-masing sub-figur (`Pada Gambar \ref{fig:...a}, ... Pada Gambar \ref{fig:...b}, ...`).
  - Setiap tugas mandiri memiliki sub-langkah `\subsubsection` yang sistematis dan seragam.
  - Menghadirkan `\subsection{Analisis Komparatif: ...}` wajib di akhir penugasan untuk mengevaluasi dampak perlakuan fitur (misal univariat vs multivariat) secara teoritis dan empiris.
  - Metrik evaluasi mencakup perpaduan RMSE dan Koefisien Korelasi Pearson ($r$).

---

## 11. Instruksi Adaptasi untuk AI (`make-laprak`)

Saat AI menggunakan skill `make-laprak` untuk menyusun laporan PPD baru berdasarkan `inisiasi.txt`:

1. **Susun Tepat 4 Bab Wajib:** `Dasar Teori`, `Hasil dan Pembahasan`, `Kesimpulan`, dan `Daftar Pustaka`.
2. **Pisahkan Bagian:** Wajib memisahkan `\section{Hasil Praktikum}` dan `\section{Tugas Praktikum}` dengan jeda halaman `\clearpage`.
3. **Gunakan Prefiks `T` untuk Tugas:**
   - Jika penugasan tunggal: `T1.png`, `T2.png`, dst.
   - Jika penugasan bertingkat / multi-tugas: gunakan format hierarkis `T1-X` dan `T2-X`.
4. **Sertakan Persamaan di Dasar Teori:** Jika topik praktikum mencakup algoritma, transformasi (seperti *sliding window*), atau metrik baru ($r$, RMSE, $R^2$, F1-score), sertakan rumus matematisnya (`\begin{equation}`) beserta rincian variabelnya.
5. **Gunakan Gaya 5 (Stacked Sub-figures) untuk Sub-langkah Berpasangan:** Gunakan dua `\includegraphics` dalam satu `figure [H]` dengan `\vspace{0.1cm}` s.d. `0.3cm` jika ada dua grafik komplementer atau kode dan output terkait.
6. **Sediakan Analisis Komparatif:** Jika Tugas Praktikum menguji beberapa perlakuan (misal variasi fitur atau komparasi model), sertakan sub-bab analisis komparatif dengan poin `\begin{enumerate}` yang membahas wawasan data, keunggulan ensemble, dan kelemahan model kaku.
7. **Tulis Kesimpulan Tepat 5 Poin:** Buat dalam bentuk `\begin{enumerate}` dengan frasa pembuka baku dan judul poin tebal analitis (`\item \textbf{...:}`).
8. **Cantumkan Sitasi Lengkap:** Masukkan modul dosen (Dr. Eng. Ir. Ganjar Alfian, S.T., M. Eng.), jurnal ilmiah bereputasi, buku teks acuan, sumber dataset Kaggle, serta tautan Colab mahasiswa di Daftar Pustaka.
