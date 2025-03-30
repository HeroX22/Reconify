# Reconify

Reconify adalah alat otomatisasi reconnaissance yang memudahkan pengumpulan informasi target secara menyeluruh. Proyek ini dirancang untuk melakukan:

- **Passive Info-Gathering**  
  Mengumpulkan data pasif dari target seperti:
  - Whois, Dig, dan Host untuk domain dan IP
  - (GeoIP untuk IP, menggunakan `curl https://ipinfo.io/{ip}/json` – saat ini dinonaktifkan)
  - Struktur hasil disimpan secara terorganisir dalam direktori proyek

- **Active Info-Gathering**  
  Melakukan scanning aktif, misalnya:
  - Menggunakan [Subfinder](https://github.com/projectdiscovery/subfinder) untuk enumerasi subdomain
  - Pengecekan HTTP/TCP untuk memastikan layanan target aktif
  - Menjalankan tool seperti Nmap, WhatWeb, tlssled, dan lain-lain untuk mengumpulkan data detail (rencana untuk diintegrasikan)

- **Vulnerability Scan**  
  Menyediakan opsi untuk menjalankan berbagai tool vulnerability scan seperti Skipfish, WATOBO, Uniscan, Wapiti, XSSer, Nikto, dan lainnya.  
  (Modul ini direncanakan untuk dikembangkan lebih lanjut agar dapat mendeteksi celah keamanan yang mungkin ada.)

- **Struktur Output Terorganisir**  
  Hasil scanning disimpan dalam struktur direktori yang rapi berdasarkan:
  - Nama Proyek
  - Domain target
  - IP address (hasil resolve dari subdomain)
  - Subdomain dengan folder untuk Active Scan dan Vulnerability Scan

## Fitur

- **Otomatisasi Reconnaissance**  
  Menggabungkan pengumpulan data pasif dan aktif dalam satu alat.
- **Output yang Terstruktur**  
  Struktur direktori yang memudahkan analisis hasil dan pengelompokan berdasarkan domain, IP, dan subdomain.
- **Multi-Domain Processing**  
  Mendukung pemrosesan lebih dari satu domain secara paralel.
- **Extensible**  
  Mudah dikembangkan untuk mengintegrasikan tool atau teknik baru dalam active scan maupun vulnerability scan.
- **Mode Debug/Verbose**  
  Menampilkan log detail (misalnya pembuatan direktori, resolving subdomain, dan eksekusi perintah) dengan flag `-v`.

## Persyaratan

- **Python 3.x**
- Tools command line yang dibutuhkan:
  - `subfinder`
  - `whois`
  - `dig`
  - `host`
  - (Opsional) `curl` untuk GeoIP (saat ini fitur GeoIP dinonaktifkan)
- Library Python:
  - `requests`

Instalasi library yang diperlukan:

```bash
pip install requests
```

## Instalasi & Cara Penggunaan

1. **Clone Repository**

   ```bash
   git clone https://github.com/username/Reconify.git
   cd Reconify
   ```

2. **Jalankan Script**

   Untuk menjalankan tanpa mode debug:

   ```bash
   python3 reconify.py
   ```

   Untuk menjalankan dengan mode debug (menampilkan log detail):

   ```bash
   python3 reconify.py -v
   ```

3. **Input yang Diperlukan**

   - Nama proyek
   - Jumlah domain yang akan diproses
   - Daftar domain (misalnya, `example.com`, `target.com`, dst)

Hasil scanning akan disimpan dalam struktur direktori seperti berikut:

```
Reconify_Project/
├── Credentials/
├── Global/
├── target.com/
│   ├── Info-Gathering/
│   │   ├── Passive/
│   │   │   ├── Whois-target.com.txt
│   │   │   ├── Dig-target.com.txt
│   │   │   └── Host-target.com.txt
│   │   └── Active/
│   │       └── Nmap/
│   │           └── nmap-target.com.txt
│   ├── IPs/
│   │   ├── 192.0.2.1/
│   │   │   ├── Info-Gathering/
│   │   │   │   └── Passive/
│   │   │   │       ├── Whois-192.0.2.1.txt
│   │   │   │       ├── Dig-192.0.2.1.txt
│   │   │   │       └── Host-192.0.2.1.txt
│   │   │   └── Subdomains/
│   │   │       └── sub.target.com/
│   │   │           ├── Active/
│   │   │           └── Vulnerability-Scan/
│   ├── Vulnerability-Scan/
│   │   └── (Tool output disesuaikan)
│   └── Notes.txt
└── README.md
```

## Rencana Pengembangan

- **Integrasi Active Recon**  
  Menambahkan modul untuk scanning aktif seperti Nmap, WhatWeb, tlssled, dan sebagainya.
- **Integrasi Vulnerability Scan**  
  Mengembangkan modul untuk menjalankan vulnerability scan menggunakan tool seperti Skipfish, WATOBO, Uniscan, Wapiti, XSSer, Nikto, dan lainnya.
- **Reporting**  
  Menyediakan fitur reporting atau agregasi hasil scan untuk memudahkan analisis.
- **Pengaturan Konfigurasi**  
  Menambahkan file konfigurasi untuk mengatur opsi-opsi scanning dan output.
