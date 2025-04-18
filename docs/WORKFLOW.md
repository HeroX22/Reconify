# 🔍 **Automated Recon & Vulnerability Assessment Workflow**

---

## **1. Input Awal**
1.1. Meminta input **nama proyek**  
1.2. Meminta input **jumlah domain utama**  
1.3. Meminta input **daftar domain utama**

---

## **2. Setup Direktori**
2.1. Membuat struktur direktori dasar berdasarkan nama proyek  
2.2. Membuat folder:  
- `Credentials/Wordlists/`  
- `Custom-Payloads/`  
- `Report/`

2.3. Untuk setiap domain: buat sub-folder berdasarkan IP dan subdomain yang aktif

---

## **3. Passive Information Gathering - Domain Utama**
3.1. Jalankan: `whois {domain}` → simpan output  
3.2. Jalankan: `dig {domain}` → simpan output  
3.3. Jalankan: `host {domain}` → simpan output  
3.4. *(Nonaktif dulu)* Jalankan: `dnsenum --enum {domain} -o /path/to/dnsenum-{domain}.xml`  
3.5. *(Nonaktif dulu)* Jalankan: `curl https://ipinfo.io/{IP_Address}/json` → simpan output  
3.6. Jalankan: `subfinder -silent -d {domain}` → simpan daftar subdomain  
3.7. Jalankan: `curl https://www.shodan.io/domain/{domain}` → ambil seluruh IP yang terdeteksi  
3.8. **[BARU]** Resolve domain → IP: `dig +short {domain} > resolved-ip.txt`
→ Simpan ke: `{project}/{domain}/resolved-ip.txt`

---

## **4. Validasi Subdomain**
4.1. Cek setiap subdomain:
- ❌ Jika **tidak bisa di-resolve DNS**, abaikan  
- ⚠️ Jika bisa resolve tapi **tidak bisa diakses via HTTP/HTTPS**, simpan ke `Notes.txt`  
- ✅ Jika bisa resolve dan bisa diakses, lanjut:  
  - **Cek IP mana yang bisa di-ping dan bisa diakses via HTTP/HTTPS**
  - Buat direktori subdomain di bawah IP yang aktif:`{project}/{domain}/IPs/{active-ip}/Subdomains/{subdomain}/`
  - Untuk IP lainnya yang juga resolve ke subdomain tersebut tapi tidak aktif:
    - Buat **symlink** ke direktori subdomain utama:
      ```bash
      ln -s ../../{active-ip}/Subdomains/{subdomain} \
            {project}/{domain}/IPs/{secondary-ip}/Subdomains/{subdomain}
      ```

---

## **5. Passive Information Gathering - IP Address**
5.1. Jalankan: `whois {IP_Address}` → simpan output  
5.2. *(Nonaktif dulu)* Jalankan: `curl https://ipinfo.io/{IP_Address}/json`

---

## **6. Active Information Gathering - Domain Utama**
6.1. Jalankan: `nmap -p- -sV -sC -T4 -A -O -oA /path/to/nmap-{domain}`  
6.2. Jalankan: `whatweb {domain}`  
6.3. Jalankan: `tlssled {domain} 443` *(jalankan dari direktori `tlssled/`)*  
6.4. Jalankan: `wafw00f -o /path/to/wafw00f-{domain} {domain}`  
6.5. Jalankan: `lbd {domain}`  
6.6. Jalankan: `echo "https://{domain}" | hakrawler -u -s -d 7`  
6.7. Ambil email dari hasil sitemap → simpan di folder `/emails`  

🟡 *Jika `whatweb` mendeteksi WordPress:*  
6.8. Jalankan: `wpscan --url {domain} -o /path/to/{domain}.txt --random-user-agent`  
 ➤ *Jika `wafw00f` deteksi WAF, konfirmasi dulu sebelum jalanin*

🔴 *Jika `whatweb` mendeteksi Joomla:*  
6.9. Jalankan: `joomscan -u http(s)://{domain} -ec`  
 ➤ Hasil dari `/usr/share/joomscan/reports/{domain}/` → pindahkan ke folder proyek

---

## **7. Deteksi Amazon S3 Bucket**
7.1. Cek CNAME dari subdomain, jika mengarah ke `s3.amazonaws.com` → tandai  
7.2. Jalankan: `curl -I https://{domain}` → cari header seperti `AmazonS3`, `AccessDenied`, dll  
7.3. Jalankan: `s3scanner -bucket {domain} -enumerate -w /path/to/common-buckets.txt`

---

## **8. Active Information Gathering - IP Address**
8.1. Jalankan: `nmap -p- -sV -sC -T4 -A -O -oA /path/to/nmap-{IP}`  
8.2. Jalankan: `whatweb {IP}`  
8.3. Jalankan: `lbd {IP}`

---

## **9. Active Information Gathering - Subdomain**
9.1. Jalankan: `whatweb {subdomain}`  
9.2. Jalankan: `wafw00f -o /path/to/wafw00f-{subdomain} {subdomain}`  
9.3. Jalankan: `echo "https://{subdomain}" | hakrawler -u -s -d 7`  
9.4. Ambil email dari hasil sitemap → simpan di `/emails`  

🟡 *Jika WordPress terdeteksi:*  
9.5. Jalankan: `wpscan --url {subdomain} -o /path/to/{subdomain}.txt --random-user-agent`  
 ➤ Konfirmasi jika WAF terdeteksi

🔴 *Jika Joomla terdeteksi:*  
9.6. Jalankan: `joomscan -u http(s)://{subdomain} -ec`  
 ➤ Ambil hasil dari `/usr/share/joomscan/reports/{subdomain}/`

---

## **10. Vulnerability Assessment - Domain Utama**
10.1. Jalankan: `skipfish -u -U -o /path/to/skipfish http(s)://{domain}`  
10.2. Jalankan: `uniscan -u http(s)://{domain}/ -qwedsj`  
 ➤ Ambil hasil dari `/usr/share/uniscan/report/{domain}.html`  
10.3. Jalankan: `wapiti -u http(s)://{domain}/ -d 16 -o /path/to/{domain}`  
10.4. Jalankan: `xsser -u http(s)://{domain} -c 16 --auto --xml {domain}.xml`  
 ➤ Ambil dari `/usr/share/xsser/{domain}.xml`  
10.5. Jalankan: `nikto -host {domain} -o /path/to/{domain}.txt`  
10.6. Jalankan: `nuclei -target {domain} -o /path/to/{domain}.txt`

---

## **11. Vulnerability Assessment - Subdomain**
11.1. Jalankan: `skipfish -u -U -o /path/to/skipfish http(s)://{subdomain}`  
11.2. Jalankan: `uniscan -u http(s)://{subdomain}/ -qwedsj`  
 ➤ Ambil dari `/usr/share/uniscan/report/{subdomain}.html`  
11.3. Jalankan: `wapiti -u http(s)://{subdomain}/ -d 16 -o /path/to/{subdomain}`  
11.4. Jalankan: `xsser -u http(s)://{subdomain} -c 16 --auto --xml {subdomain}.xml`  
 ➤ Ambil dari `/usr/share/xsser/{subdomain}.xml`  
11.5. Jalankan: `nikto -host {subdomain} -o /path/to/{subdomain}.txt`  
11.6. Jalankan: `nuclei -target {subdomain} -o /path/to/{subdomain}.txt`

---

## **12. Report Final**
12.1. Gabungkan semua hasil ke dalam satu laporan HTML  
12.2. Isi report:
- 📌 Daftar domain & subdomain aktif
- 🛡️ Deteksi WAF & teknologi
- 🧨 Potensi kerentanan dari hasil tools
- 🔗 Link semua output tools
- 📦 Bucket S3 yang terdeteksi (jika ada)
- 📧 Email yang ditemukan dari hakrawler
- 📸 Screenshots hasil testing
- 📝 Catatan subdomain mati/unreachable
12.3. Simpan laporan akhir ke: `{project}/Report/{domain}-summary.html`
