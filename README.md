# 🚀 YouTube Data Pipeline Orchestration with Airflow & Docker

Proyek ini adalah sebuah *End-to-End Data Pipeline* (ETL) yang dirancang untuk mengekstrak data komentar dari YouTube secara otomatis, memprosesnya menjadi format terstruktur, dan menyimpannya ke dalam *cloud storage* AWS S3. Seluruh infrastruktur di-*deploy* di atas Amazon EC2, dikontainerisasi dengan Docker, dan diorkestrasi menggunakan Apache Airflow.

## 🏗️ Data Pipeline Architecture

<div align="center">
  <!-- Jika Anda mengunggah gambar tersebut ke repo, Anda bisa mengganti URL di bawah dengan path gambar Anda, misalnya: <img src="image_90db7f.png" alt="Architecture"> -->
  <img width="981" height="248" alt="Screenshot 2026-07-10 052805" src="https://github.com/user-attachments/assets/61a89124-af0c-416c-96d0-511c6ba613ba" />
</div>

## 🛠️ Tools & Technologies Used

Berikut adalah peran dan fungsi dari masing-masing teknologi dalam *pipeline* ini:

1. **YouTube Data API v3 (Data Source)**
   * Berfungsi sebagai sumber data mentah. Pipeline memanfaatkan API ini untuk mengekstrak (*Extract*) ribuan komentar dari sebuah video YouTube spesifik, lengkap dengan metadatanya (nama penulis, waktu *publish*, jumlah *like*, dan isi komentar).

2. **Python & Pandas (ETL Engine)**
   * Bertindak sebagai mesin pemroses utama. Skrip Python (`etl_youtube.py`) mengambil data JSON dari YouTube API, melakukan transformasi (*Transform*) data ke dalam format tabular menggunakan *library* Pandas `DataFrame`, dan memuatnya (*Load*) secara langsung ke media penyimpanan menggunakan `s3fs`.

3. **Amazon EC2 (Cloud Infrastructure)**
   * *Virtual server* (komputasi awan) yang berjalan 24/7. Server ini bertugas sebagai rumah/infrastruktur utama (*host*) tempat berjalannya seluruh sistem otomatisasi tanpa membebani memori komputer lokal.

4. **Docker & Docker Compose (Containerization)**
   * Membungkus seluruh sistem operasi Airflow (termasuk *Database* PostgreSQL untuk metadata dan Redis sebagai *message broker*) ke dalam *container* yang terisolasi. Ini memastikan lingkungan kerja tetap bersih, terhindar dari konflik *library* (*Dependency Hell*), dan membuat sistem sangat mudah di-*deploy* ulang (*reproducible*).

5. **Apache Airflow (Orchestration & Scheduling)**
   * Berperan sebagai "otak" atau manajer operasional. Airflow menjadwalkan kapan skrip Python harus berjalan (misalnya setiap hari pada jam tertentu menggunakan *Cron job*), memantau status tugas, dan melakukan percobaan ulang otomatis (*retry*) jika terjadi kegagalan jaringan saat menghubungi API.

6. **Amazon S3 (Data Storage/Data Lake)**
   * Destinasi akhir dari *pipeline*. Data yang sudah rapi disimpan di dalam AWS S3 *Bucket* dalam format `.csv`. Penyimpanan ini bertindak sebagai *Data Lake* yang aman, dapat diskalakan (*scalable*), dan siap digunakan untuk proses analisis lanjutan atau *Machine Learning*.

## 📁 Project Structure

```text
youtube-etl-pipeline/
├── dags/
│   └── dag_youtube.py          # Script orkestrasi Airflow (DAG definition)
├── scripts/
│   └── etl_youtube.py          # Script logika utama (Extract & Load ke S3)
├── docker-compose.yaml         # Konfigurasi container infrastruktur (Airflow, Postgres, Redis)
├── requirements.txt            # Daftar library Python tambahan (s3fs, google-api-python-client)
└── .env                        # Environment variables (AIRFLOW_UID, kredensial)

## connect to ec2
ssh -i "airflow_ec2_key.pem" ubuntu@ec2-(ip server).ap-southeast-2.compute.amazonaws.com

## update and install
- sudo apt get-update
- sudo apt update && sudo apt install python3-venv -y
- mkdir my_airflow && cd my_airflow
- python3 -m venv airflow_env
- source airflow_env/bin/activate
- pip install apache-airflow
