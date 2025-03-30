import os
import subprocess
import socket
import requests
import threading
import argparse

# Variabel global untuk mode debug
DEBUG_MODE = False

def debug_print(msg):
    if DEBUG_MODE:
        print(f"[DEBUG] {msg}")

def info_print(msg):
    print(f"[INFO] {msg}")

# Fungsi untuk membuat direktori (pesan hanya tampil di debug)
def create_dir(path):
    os.makedirs(path, exist_ok=True)
    debug_print(f"Direktori dibuat: {path}")

# Fungsi untuk menjalankan command dan menyimpan output ke file
def run_passive_command(command, output_file):
    try:
        result = subprocess.run(command, capture_output=True, text=True)
        output = result.stdout.strip()
    except Exception as e:
        output = f"Error menjalankan {' '.join(command)}: {e}"
    with open(output_file, "w") as f:
        f.write(output)
    debug_print(f"File dibuat: {output_file}")

# Fungsi untuk menjalankan passive info gathering untuk domain
def run_passive_info(domain_dir, domain):
    passive_folder = os.path.join(domain_dir, "Info-Gathering", "Passive")
    
    # Whois
    info_print(f"Menjalankan Whois untuk domain: {domain}")
    whois_file = os.path.join(passive_folder, f"Whois-{domain}.txt")
    run_passive_command(["whois", domain], whois_file)
    
    # Dig
    info_print(f"Menjalankan Dig untuk domain: {domain}")
    dig_file = os.path.join(passive_folder, f"Dig-{domain}.txt")
    run_passive_command(["dig", domain], dig_file)
    
    # Host
    info_print(f"Menjalankan Host untuk domain: {domain}")
    host_file = os.path.join(passive_folder, f"Host-{domain}.txt")
    run_passive_command(["host", domain], host_file)
    
    # Perintah dnsenum dimatikan
    # info_print(f"Menjalankan DnsEnum untuk domain: {domain}")
    # dnsenum_file = os.path.join(passive_folder, f"DnsEnum-{domain}.txt")
    # run_passive_command(["dnsenum", domain], dnsenum_file)

# Fungsi untuk menjalankan passive info gathering untuk IP address
def run_ip_passive_info(ip_folder, ip):
    passive_folder = os.path.join(ip_folder, "Info-Gathering", "Passive")
    
    info_print(f"Menjalankan Whois untuk IP: {ip}")
    whois_file = os.path.join(passive_folder, f"Whois-{ip}.txt")
    run_passive_command(["whois", ip], whois_file)
    
    info_print(f"Menjalankan Dig untuk IP: {ip}")
    dig_file = os.path.join(passive_folder, f"Dig-{ip}.txt")
    run_passive_command(["dig", ip], dig_file)
    
    info_print(f"Menjalankan Host untuk IP: {ip}")
    host_file = os.path.join(passive_folder, f"Host-{ip}.txt")
    run_passive_command(["host", ip], host_file)
    
    # Perintah dnsenum dimatikan
    # info_print(f"Menjalankan DnsEnum untuk IP: {ip}")
    # dnsenum_file = os.path.join(passive_folder, f"DnsEnum-{ip}.txt")
    # run_passive_command(["dnsenum", ip], dnsenum_file)
    
    # Proses GeoIP (dinonaktifkan dulu)
    # info_print(f"Menjalankan GeoIP untuk IP: {ip}")
    # geoip_file = os.path.join(passive_folder, f"GeoIP-{ip}.txt")
    # run_passive_command(["curl", f"https://ipinfo.io/{ip}/json"], geoip_file)

# Fungsi untuk membuat struktur direktori umum untuk proyek
def create_common_structure(project_name):
    base_dir = project_name
    dirs_to_create = [
        os.path.join(base_dir, "Credentials", "Usernames"),
        os.path.join(base_dir, "Credentials", "Passwords"),
        os.path.join(base_dir, "Credentials", "databases"),
        os.path.join(base_dir, "Credentials", "Personal-Informations"),
        os.path.join(base_dir, "Credentials", "Emails"),
        os.path.join(base_dir, "Global", "Tools", "Third-Party"),
        os.path.join(base_dir, "Global", "Tools", "Custom-Scripts", "Recon"),
        os.path.join(base_dir, "Global", "Tools", "Custom-Scripts", "Exploitation"),
        os.path.join(base_dir, "Global", "Scripts")
    ]
    
    for d in dirs_to_create:
        create_dir(d)
    
    readme_path = os.path.join(base_dir, "README.md")
    if not os.path.exists(readme_path):
        with open(readme_path, "w") as f:
            f.write("# README\n")
        debug_print(f"File dibuat: {readme_path}")
    
    return base_dir

# Fungsi untuk membuat struktur direktori khusus untuk sebuah domain
def create_domain_structure(base_dir, domain):
    domain_dir = os.path.join(base_dir, domain)
    dirs_to_create = [
        os.path.join(domain_dir, "Info-Gathering", "Passive"),
        os.path.join(domain_dir, "Info-Gathering", "Active", "Nmap"),
        os.path.join(domain_dir, "Info-Gathering", "Active", "tlssled"),
        os.path.join(domain_dir, "Vulnerability-Scan", "Skipfish"),
        os.path.join(domain_dir, "Vulnerability-Scan", "WATOBO"),
        os.path.join(domain_dir, "Vulnerability-Scan", "Uniscan"),
        os.path.join(domain_dir, "Vulnerability-Scan", "Wapiti"),
        os.path.join(domain_dir, "Vulnerability-Scan", "XSSer"),
        os.path.join(domain_dir, "Vulnerability-Scan", "Nikto"),
        os.path.join(domain_dir, "Vulnerability-Scan", "Other-Scans"),
        os.path.join(domain_dir, "IPs"),  # Folder untuk IP akan diisi nanti
        os.path.join(domain_dir, "Exploitation", "Exploits"),
        os.path.join(domain_dir, "Exploitation", "Payloads"),
        os.path.join(domain_dir, "Post-Exploitation", "Persistence"),
        os.path.join(domain_dir, "Post-Exploitation", "Privilege-Escalation"),
        os.path.join(domain_dir, "Post-Exploitation", "Lateral-Movement"),
        os.path.join(domain_dir, "Logs")
    ]
    
    for d in dirs_to_create:
        create_dir(d)
    
    notes_path = os.path.join(domain_dir, "Notes.txt")
    if not os.path.exists(notes_path):
        with open(notes_path, "w") as f:
            f.write("Catatan:\n")
        debug_print(f"File dibuat: {notes_path}")
    
    return domain_dir

# Fungsi menjalankan Subfinder dan menyimpan output ke file
def run_subfinder(domain, output_file):
    try:
        info_print(f"Menjalankan Subfinder untuk domain: {domain}")
        result = subprocess.run(["subfinder", "-d", domain], capture_output=True, text=True)
        if result.returncode != 0:
            debug_print(f"Subfinder gagal dijalankan untuk {domain}")
            return []
        subdomains = result.stdout.strip().splitlines()
        with open(output_file, "w") as f:
            f.write("\n".join(subdomains))
        info_print(f"Output Subfinder disimpan di: {output_file}")
        return subdomains
    except Exception as e:
        debug_print(f"Error saat menjalankan Subfinder untuk {domain}: {e}")
        return []

# Fungsi untuk mengecek HTTP dan TCP (port 80)
def check_http_tcp(subdomain):
    url = f"http://{subdomain}"
    try:
        response = requests.get(url, timeout=5)
        status_code = response.status_code
    except Exception as e:
        return False, f"HTTP error: {e}"
    
    if status_code in [200, 301]:
        try:
            s = socket.create_connection((subdomain, 80), timeout=5)
            s.close()
            return True, f"HTTP {status_code} dan TCP port 80 terbuka"
        except Exception as e:
            return False, f"TCP error: {e}"
    else:
        return False, f"HTTP status code {status_code}"

# Fungsi untuk membuat struktur direktori untuk IP pada sebuah domain
def create_ip_structure(domain_dir, ip):
    ip_folder = os.path.join(domain_dir, "IPs", ip)
    dirs_to_create = [
        os.path.join(ip_folder, "Info-Gathering", "Passive"),
        os.path.join(ip_folder, "Info-Gathering", "Active", "Nmap"),
        os.path.join(ip_folder, "Subdomains")
    ]
    for d in dirs_to_create:
        create_dir(d)
    
    # Jalankan passive info gathering untuk IP (hanya saat folder baru dibuat)
    run_ip_passive_info(ip_folder, ip)
    return ip_folder

# Fungsi untuk memproses setiap subdomain pada sebuah domain
def process_subdomains(domain_dir, domain, subdomains):
    notes_file = os.path.join(domain_dir, "Notes.txt")
    
    for sub in subdomains:
        try:
            ip = socket.gethostbyname(sub)
            debug_print(f"{sub} resolved ke {ip}")
        except Exception as e:
            msg = f"Subdomain {sub} tidak dapat diresolve: {e}"
            debug_print(msg)
            with open(notes_file, "a") as f:
                f.write(msg + "\n")
            continue
        
        success, detail = check_http_tcp(sub)
        if not success:
            msg = f"Subdomain {sub} dengan IP {ip} gagal cek HTTP/TCP: {detail}"
            debug_print(msg)
            with open(notes_file, "a") as f:
                f.write(msg + "\n")
            continue
        
        ip_folder = os.path.join(domain_dir, "IPs", ip)
        if not os.path.exists(ip_folder):
            ip_folder = create_ip_structure(domain_dir, ip)
        
        subdomain_dir = os.path.join(ip_folder, "Subdomains", sub)
        active_dir = os.path.join(subdomain_dir, "Active")
        vuln_dir = os.path.join(subdomain_dir, "Vulnerability-Scan")
        create_dir(active_dir)
        create_dir(vuln_dir)
        
        whatweb_file = os.path.join(active_dir, f"WhatWeb-{sub}.txt")
        with open(whatweb_file, "w") as f:
            f.write(f"Hasil scan WhatWeb untuk {sub}\n")
        debug_print(f"Direktori dan file untuk subdomain {sub} dibuat di {subdomain_dir}.")

# Fungsi untuk memproses satu domain secara lengkap
def process_domain(domain, base_dir):
    info_print(f"=== Memproses domain: {domain} ===")
    domain_dir = create_domain_structure(base_dir, domain)
    
    # Jalankan passive info gathering untuk domain
    run_passive_info(domain_dir, domain)
    
    subfinder_output_file = os.path.join(domain_dir, "Info-Gathering", "Passive", f"Subfinder-{domain}.txt")
    subdomains = run_subfinder(domain, subfinder_output_file)
    if not subdomains:
        debug_print(f"Tidak ada subdomain yang ditemukan untuk {domain}.")
        return
    process_subdomains(domain_dir, domain, subdomains)
    info_print(f"=== Selesai memproses domain: {domain} ===\n")

def main():
    global DEBUG_MODE
    
    parser = argparse.ArgumentParser(description="Script untuk membuat struktur project dan scanning domain.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Aktifkan mode debug")
    args = parser.parse_args()
    DEBUG_MODE = args.verbose
    
    project_name = input("Masukkan nama project: ").strip()
    base_dir = create_common_structure(project_name)
    
    try:
        jumlah_domain = int(input("Masukkan jumlah domain dalam proyek: ").strip())
    except ValueError:
        debug_print("Input jumlah domain harus berupa angka!")
        return
    
    domains = []
    for i in range(jumlah_domain):
        domain = input(f"Masukkan domain ke-{i+1} (contoh: example.com): ").strip()
        domains.append(domain)
    
    threads = []
    for domain in domains:
        t = threading.Thread(target=process_domain, args=(domain, base_dir))
        t.start()
        threads.append(t)
    
    for t in threads:
        t.join()
    
    info_print("Proses semua domain selesai.")

if __name__ == "__main__":
    main()
