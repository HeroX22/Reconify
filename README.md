# Reconify

Reconify adalah alat otomatisasi reconnaissance yang memudahkan pengumpulan informasi target secara menyeluruh. Proyek ini dirancang untuk melakukan:

- **Passive Info-Gathering**  
  Mengumpulkan data pasif dari target, seperti:
  - Whois, Dig, Host (untuk domain dan IP)
  - GeoIP (menggunakan `curl https://ipinfo.io/{ip}/json` – saat ini dinonaktifkan)
  - Subdomain enumeration menggunakan [Subfinder](https://github.com/projectdiscovery/subfinder)

- **Active Info-Gathering**  
  Rencana untuk melakukan scanning aktif (misalnya Nmap, WhatWeb, tlssled, dll) untuk mengumpulkan data lebih detail.

- **Vulnerability Scan**  
  Rencana untuk mengintegrasikan berbagai tool vulnerability scan (Skipfish, WATOBO, Uniscan, Wapiti, XSSer, Nikto, dll) untuk mendeteksi celah keamanan.

- **Struktur Output Terorganisir**  
  Semua hasil scanning disimpan secara terstruktur berdasarkan:
  - Nama Proyek
  - Domain target
  - IP address (hasil resolve dari subdomain)
  - Subdomain (dengan folder untuk Active Scan dan Vulnerability Scan)

## Fitur

- **Automated Reconnaissance**:  
  Menggabungkan passive dan active info-gathering dalam satu alat.
- **Organized Output**:  
  Struktur direktori yang rapi memudahkan analisis hasil.
- **Multi-Domain Processing**:  
  Mendukung pemrosesan beberapa domain secara paralel.
- **Extensible**:  
  Mudah dikembangkan untuk mengintegrasikan tool atau teknik scanning lainnya.
- **Mode Debug/Verbose**:  
  Log detail pembuatan file dan direktori dapat diaktifkan dengan flag `-v`.

## Persyaratan

- **Python 3.x**
- Tools command line yang diperlukan:
  - `subfinder`
  - `whois`
  - `dig`
  - `host`
  - (Opsional) `curl` untuk GeoIP (fitur saat ini dinonaktifkan)
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

   Tanpa mode debug:

   ```bash
   python reconify.py
   ```

   Dengan mode debug (menampilkan log detail):

   ```bash
   python reconify.py -v
   ```

3. **Input yang Diperlukan**

   - Nama proyek
   - Jumlah domain yang akan diproses
   - Daftar domain (misalnya: `example.com`, `target.com`, dst)

## Struktur Direktori

Setelah menjalankan script, output hasil scanning akan tersimpan dengan struktur direktori sebagai berikut:

```
{project_name}/ 
│
├── Credentials/
│   ├── Usernames/
│   ├── Passwords/
│   ├── databases/
│   ├── Personal-Informations/
│   └── Emails/
│
├── Global/
│   ├── Tools/
│   │   ├── Third-Party/
│   │   └── Custom-Scripts/
│   │       ├── Recon/
│   │       └── Exploitation/
│   └── Scripts/
│
├── {domain1}.com/
│   ├── Info-Gathering/
│   │   ├── Passive/
│   │   │   ├── Whois-{domain1}.txt
│   │   │   ├── Dig-{domain1}.txt
│   │   │   ├── Host-{domain1}.txt
│   │   │   ├── DnsEnum-{domain1}.txt  *(dinonaktifkan)*
│   │   │   ├── GeoIP-{ip-public}.txt   *(dinonaktifkan untuk domain)*
│   │   │   └── Subfinder-{domain1}.txt
│   │   ├── Active/
│   │   │   ├── Nmap/
│   │   │   │   └── nmap-{domain1}.txt
│   │   │   ├── tlssled/
│   │   │   │   └── [hasil scan]
│   │   │   ├── WhatWeb-{domain1}.txt
│   │   │   ├── JoomScan-{domain1}.txt   *(jika terdeteksi Joomla)*
│   │   │   ├── WPScan-{domain1}.txt       *(jika terdeteksi WordPress)*
│   │   │   ├── WAFW00F-{domain1}.txt
│   │   │   ├── Sitemap-{domain1}.txt      *(Hakrawler)*
│   │   │   └── LoadBalancer-{domain1}.txt *(ldb)*
│   ├── Vulnerability-Scan/ *(rencana scan vulnerability)*
│   │   ├── Skipfish/
│   │   ├── WATOBO/
│   │   ├── Uniscan/
│   │   ├── Wapiti/
│   │   ├── XSSer/
│   │   ├── Nikto/
│   │   └── Other-Scans/
│   ├── IPs/
│   │   ├── {ip-public1}/
│   │   │   ├── Info-Gathering/
│   │   │   │   ├── Passive/
│   │   │   │   │   ├── Whois-{ip-public}.txt
│   │   │   │   │   ├── Dig-{ip-public}.txt
│   │   │   │   │   ├── Host-{ip-public}.txt
│   │   │   │   │   ├── DnsEnum-{ip-public}.txt  *(dinonaktifkan)*
│   │   │   │   │   └── GeoIP-{ip-public}.txt       *(dinonaktifkan)*
│   │   │   ├── Active/
│   │   │   │   ├── WhatWeb/
│   │   │   │   ├── LoadBalancer/
│   │   │   │   ├── Nmap/
│   │   │   │   │   └── nmap-{domain1}.txt
│   │   │   │   └── LoadBalancer-{domain1}.txt *(ldb)*
│   │   │   └── Subdomains/
│   │   │       ├── {sub}.{domain1}.com/
│   │   │       │   ├── Active/
│   │   │       │   │   ├── WhatWeb-{sub}.{domain1}.txt
│   │   │       │   │   ├── JoomScan-{sub}.{domain1}.txt *(jika terdeteksi Joomla)*
│   │   │       │   │   ├── WPScan-{sub}.{domain1}.txt   *(jika terdeteksi WordPress)*
│   │   │       │   │   ├── WAFW00F-{sub}.{domain1}.txt
│   │   │       │   │   ├── Hakrawler-{sub}.{domain1}.txt
│   │   │       │   ├── Vulnerability-Scan/
│   │   │       │   │   ├── Skipfish/
│   │   │       │   │   ├── WATOBO/
│   │   │       │   │   ├── Uniscan/
│   │   │       │   │   ├── Wapiti/
│   │   │       │   │   ├── XSSer/
│   │   │       │   │   ├── Nikto/
│   │   │       │   │   └── Other-Scans/
│   ├── Exploitation/
│   │   ├── Exploits/
│   │   └── Payloads/
│   ├── Post-Exploitation/
│   │   ├── Persistence/
│   │   ├── Privilege-Escalation/
│   │   └── Lateral-Movement/
│   ├── Logs/
│   └── Notes.txt
│
└── README.md
```

## Rencana Pengembangan

- **Integrasi Active Recon**  
  Menambahkan modul untuk scanning aktif (Nmap, WhatWeb, tlssled, dll).
- **Integrasi Vulnerability Scan**  
  Menyediakan modul vulnerability scan menggunakan tool seperti Skipfish, WATOBO, Uniscan, Wapiti, XSSer, Nikto, dan lainnya.
- **Reporting & Analisis**  
  Mengembangkan fitur reporting untuk mengagregasi hasil scan.
- **Konfigurasi yang Lebih Fleksibel**  
  Menambahkan opsi konfigurasi untuk mengatur parameter scanning dan output.
