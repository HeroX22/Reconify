# Reconify Pentesting Project

**Reconify** adalah framework pentesting otomatis yang mengorganisir seluruh alur pengerjaan pentest dalam sebuah proyek yang terstruktur dengan baik. Setiap bagian dari hasil reconnaissance, eksploitasi, hingga post-exploitation dapat disimpan dengan rapi dalam folder yang telah diatur sedemikian rupa.

## Struktur Direktori

Berikut adalah struktur direktori dari proyek yang dihasilkan oleh **Reconify**:

```
{project_name}/
│
├── project.yml                     # Metadata internal (nama project, scope, dll)
│
├── Credentials/
│   ├── Usernames/                  # Hasil enumerasi/leak
│   ├── Passwords/                  # Brute/leak password
│   ├── Databases/                  # Dump DB (kalau ada)
│   ├── Personal-Informations/      # NIK, alamat, dsb
│   └── Emails/                     # Hasil scraping/email leak
│
├── Global/
│   ├── Tools/
│   │   ├── Third-Party/            # Tools pihak ketiga (binaries)
│   │   └── Custom-Scripts/
│   │       ├── Recon/              # Script recon buatan sendiri
│   │       └── Exploitation/       # Script exploit custom
│   └── Scripts/                    # Workflow helper script umum
│
├── {domain1}/
│   ├── Info-Gathering/
│   │   ├── Passive/
│   │   │   ├── Whois-{domain1}.txt
│   │   │   ├── Dig-{domain1}.txt
│   │   │   ├── Host-{domain1}.txt
│   │   │   ├── DnsEnum-{domain1}.txt
│   │   │   ├── GeoIP-{ip-public}.txt
│   │   │   └── Subfinder-{domain1}.txt
│   │   ├── Active/
│   │   │   ├── Nmap/
│   │   │   │   └── nmap-{domain1}.gnmap
│   │   │   ├── TLSSled/
│   │   │   │   └── tlssled-{domain1}.txt
│   │   │   ├── WhatWeb-{domain1}.txt
│   │   │   ├── WPScan-{domain1}.txt
│   │   │   ├── JoomScan-{domain1}.txt
│   │   │   ├── WAFW00F-{domain1}.txt
│   │   │   ├── Sitemap-{domain1}.txt
│   │   │   └── LoadBalancer-{domain1}.txt
│   │
│   ├── Vulnerability-Scan/
│   │   ├── Skipfish/
│   │   ├── WATOBO/
│   │   ├── Uniscan/
│   │   ├── Wapiti/
│   │   ├── XSSer/
│   │   ├── Nikto/
│   │   ├── Nuclei/
│   │   └── Other-Scans/
│   │
│   ├── IPs/
│   │   ├── {ip-public1}/
│   │   │   ├── Info-Gathering/
│   │   │   │   ├── Passive/
│   │   │   │   │   ├── Whois-{ip-public}.txt
│   │   │   │   │   └── GeoIP-{ip-public}.txt
│   │   │   │   ├── Active/
│   │   │   │   │   ├── Nmap/
│   │   │   │   │   │   └── nmap-{ip-public}.gnmap
│   │   │   │   │   ├── WhatWeb-{ip-public}.txt
│   │   │   │   │   └── LoadBalancer-{ip-public}.txt
│   │   │   └── Subdomains/
│   │   │       ├── {sub}.{domain1}/
│   │   │       │   ├── Active/
│   │   │       │   │   ├── WhatWeb-{sub}.txt
│   │   │       │   │   ├── WPScan-{sub}.txt
│   │   │       │   │   ├── JoomScan-{sub}.txt
│   │   │       │   │   ├── WAFW00F-{sub}.txt
│   │   │       │   │   └── Hakrawler-{sub}.txt
│   │   │       │   ├── Vulnerability-Scan/
│   │   │       │   │   ├── Skipfish/
│   │   │       │   │   ├── Uniscan/
│   │   │       │   │   ├── Wapiti/
│   │   │       │   │   ├── XSSer/
│   │   │       │   │   ├── Nikto/
│   │   │       │   │   ├── Nuclei/
│   │   │       │   │   └── Other-Scans/
│
│   ├── Exploitation/
│   │   ├── Exploits/              # PoC / modifikasi exploit
│   │   └── Payloads/              # Payload yang disesuaikan
│
│   ├── Post-Exploitation/
│   │   ├── Persistence/
│   │   ├── Privilege-Escalation/
│   │   └── Lateral-Movement/
│
│   ├── Screenshots/              # Bukti visual panel, bug, dll
│   ├── Timeline.md               # Kronologi aktivitas selama pentest
│   ├── log.txt                   # Log kerja teknikal (opsional)
│   └── Notes.txt                 # Catatan isian bebas (dead subdomain dll)
│
└── README.md                     # Penjelasan umum project dan struktur
```

## Penjelasan Struktur Direktori

### 1. **project.yml**
   Berisi metadata internal mengenai project, seperti nama, deskripsi, dan scope pentesting yang dilakukan.

### 2. **Credentials**
   Folder ini menyimpan berbagai informasi kredensial yang ditemukan selama pentest, seperti usernames, passwords, database dumps, informasi pribadi, dan email.

### 3. **Global**
   Menyimpan alat bantu dan skrip umum yang digunakan di seluruh proyek, baik itu tools pihak ketiga atau custom-script buatan tim.

### 4. **{domain1}**
   Setiap domain yang dipilih untuk pentest akan memiliki folder ini, yang memuat hasil pengumpulan informasi baik secara pasif maupun aktif, termasuk hasil scan untuk setiap subdomain, IP, atau server.

### 5. **Exploitation**
   Folder untuk menyimpan hasil eksploitasi, termasuk script exploit custom, payload yang disesuaikan, dan hasil lainnya.

### 6. **Post-Exploitation**
   Memuat dokumentasi tentang aksi-aksi setelah eksploitasi, termasuk persistence, privilege escalation, dan lateral movement.

### 7. **Screenshots**
   Menyimpan bukti visual atau screenshot yang diambil selama pentest untuk digunakan dalam dokumentasi atau laporan.

### 8. **Timeline.md**
   Mengandung kronologi aktivitas yang terjadi selama pentest. Ini penting untuk merekam urutan kegiatan dan hasil yang didapat.

### 9. **log.txt**
   Opsional, berisi log teknikal dari pelaksanaan pentest yang dilakukan oleh berbagai tools. Dapat digunakan untuk debugging atau audit.

### 10. **Notes.txt**
   Tempat untuk menulis catatan tambahan terkait temuan-temuan penting atau dead subdomains, atau hal-hal lainnya yang perlu dicatat selama pentest.

---

## Setup & Penggunaan

Untuk menjalankan **Reconify**, pertama pastikan semua dependensi sudah diinstall. Jalankan perintah berikut untuk setup:

```bash
pip install -r requirements.txt
```

Setelah itu, kamu bisa mulai dengan menjalankan perintah berikut untuk melakukan konfigurasi awal dan mulai pentest:

```bash
python reconify.py --config config.yml --mode full
```

### Menggunakan Config File
Misalnya, berikut adalah contoh format dari `config.yml`:

```yaml
project: "Pentest Example"
domains:
  - "example.com"
mode: "full"
```

### Menambahkan dan Menjalankan Mode
- `passive`: Hanya melakukan scanning pasif
- `light`: Scanning pasif dan sedikit aktif
- `standard`: Semua recon aktif dengan intensitas sedang
- `full`: Semua recon aktif dengan intensitas penuh
- `custom`: Menjalankan mode custom berdasarkan YAML yang diberikan