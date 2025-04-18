# 🛠️ **Reconify Roadmap (Python-based)**

## 📍 **Stage 1: Setup Awal**
- [x] Inisialisasi project: struktur direktori, virtualenv, requirements.txt
- [x] Tentukan arsitektur project (folder `core/`, `modules/`, `utils/`, `cli/`, dll)
- [x] Tulis workflow dasar di `docs/WORKFLOW.md`

---

## ⚙️ **Stage 2: Input Handler**
- [x] Implement parser:
  - [x] `--config config.yml` → baca file YAML
  - [x] CLI flags → argparse / click
  - [x] Wizard → mode interaktif CLI (pakai `InquirerPy` atau `questionary`)
- [ ] Validasi input user
- [x] Merge logic: jika config & flag keduanya aktif → flag override config
- [x] Simpan hasil parsing ke struktur data internal (`ctx`, `Session`, dsb)

---

## 🚦 **Stage 3: Mode Handler**
- [x] Definisikan mode `--mode`:
  - `passive`: hanya tahap pasif (tanpa nmap, wpscan, dll)
  - `light`: passive + sedikit active (e.g., nmap singkat)
  - `standard`: semua recon aktif (tidak terlalu intensif)
  - `full`: recon + VA lengkap (semua tool dijalankan)
  - `custom`: jalankan berdasarkan YAML / flag pilihan user
- [x] Mapping setiap mode ke langkah workflow tertentu
- [x] Implementasi filtering langkah berdasarkan mode

---

## 🧱 **Stage 4: Directory Builder**
- [x] Fungsi pembuatan struktur direktori otomatis saat project dimulai
- [x] Folder berdasarkan domain, IP, subdomain
- [ ] Pembuatan symlink untuk subdomain shared IP
- [x] Folder khusus untuk output tool, logs, email, report, dll

---

## 🔧 **Stage 5: Modular Workflow Executor**
- [x] Buat `TaskRunner` atau semacam pipeline executor
- [x] Pisah tiap tool ke modul Python terpisah di folder `modules/`
- [x] Modul `recon.py` dan `scan.py` dasar
- [x] Logging helper (`utils/logger.py`) dan file helper (`utils/file_helper.py`)
- [ ] Tambah modul lain: `whois`, `dig`, `nmap`, `wpscan`, dll
- [ ] Setiap modul menerima `target`, menyimpan hasil, dan return status
- [ ] Logging per-task + error handling

---

## 🧠 **Stage 6: Intelligence Layer (Opsional)**
- [ ] Deteksi WordPress / Joomla → jalankan tool tertentu (conditional logic)
- [ ] Deteksi subdomain mati → tandai di notes
- [ ] Deteksi WAF → konfirmasi dulu sebelum lanjut scan

---

## 📊 **Stage 7: Reporting**
- [ ] Kumpulkan semua output dari setiap modul
- [ ] Generate report HTML otomatis
- [ ] Sertakan: struktur domain, IP, subdomain, email, hasil tools, potensi kerentanan
- [ ] Link ke file hasil mentah (output asli tool)

---

## 🧪 **Stage 8: Testing & CLI Polish**
- [ ] Uji semua mode: passive, light, standard, full, custom
- [ ] Uji semua metode input (config, flags, wizard)
- [ ] Tambahkan `--dry-run`, `--debug`, `--resume` (opsional)
- [ ] Tambahkan CLI UX polishing (spinner, progress, warna)

---

## 🚀 **Stage 9: Rilis & Dokumentasi**
- [ ] Setup repo GitHub
- [ ] Tambahkan README, usage examples, screenshots
- [ ] Tambahkan `reconify.yml.sample`
- [ ] Buat file LICENSE (MIT/GPL)
- [ ] Rilis versi 1.0.0