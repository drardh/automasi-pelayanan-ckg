# 🏥 Automasi Entri Pelayanan Cek Kesehatan Gratis

Program automasi untuk mengisi form entri pelayanan cek kesehatan gratis di **Sehat Indonesiaku** (https://sehatindonesiaku.kemkes.go.id).

## 📋 Fitur

- ✅ Membaca data dari file Excel/Spreadsheet
- ✅ Automasi pengisian form dengan Selenium
- ✅ Validasi data sebelum disubmit
- ✅ Logging dan tracking progress
- ✅ Error handling dan retry mechanism
- ✅ Report summary hasil automasi

## 🗂️ Struktur Project

```
automasi-pelayanan-ckg/
├── data/
│   ├── data_ckg.xlsx (file data Anda)
│   └── data_ckg_template.xlsx (template contoh)
├── drivers/
│   └── chromedriver (download chromedriver di sini)
├── logs/
│   └── automasi_[tanggal].log (file log otomatis)
├── modules/
│   ├── __init__.py
│   ├── logger.py (sistem logging)
│   ├── excel_reader.py (membaca Excel)
│   └── form_filler.py (pengisi form)
├── main.py (script utama)
├── requirements.txt (dependencies)
├── .env.example (template environment variables)
├── .gitignore
└── README.md
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/drardh/automasi-pelayanan-ckg.git
cd automasi-pelayanan-ckg
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Download ChromeDriver

1. Cek versi Chrome Anda: **Chrome Menu → Settings → About Chrome**
2. Download ChromeDriver sesuai versi: https://chromedriver.chromium.org/
3. Extract dan letakkan di folder `drivers/`

**Contoh struktur:**
```
drivers/
├── chromedriver (Linux/Mac)
└── chromedriver.exe (Windows)
```

### 4. Setup Environment
```bash
cp .env.example .env
# Edit .env jika perlu mengubah URL atau pengaturan
```

### 5. Siapkan Data Excel

Buat file `data/data_ckg.xlsx` dengan kolom berikut:

| NIK | NAMA | TINGGI_BADAN | BERAT_BADAN | LINGKAR_PERUT | TEKANAN_DARAH_SISTOL | TEKANAN_DARAH_DIASTOL | GULA_DARAH |
|-----|------|--------------|-------------|---------------|----------------------|----------------------|-----------|
| 1234567890123456 | Budi Santoso | 170 | 75 | 85 | 120 | 80 | 110 |
| 1234567890123457 | Siti Nurhaliza | 165 | 65 | 80 | 115 | 75 | 105 |

### 6. Jalankan Program

```bash
# Mode normal
python main.py --file data/data_ckg.xlsx

# Mode debug (tampilkan browser)
python main.py --file data/data_ckg.xlsx --debug

# Mode dry-run (test tanpa submit)
python main.py --file data/data_ckg.xlsx --dry-run
```

## 📊 Format Data Excel

### Kolom Wajib:
- **NIK** - Nomor Identitas (16 digit)
- **NAMA** - Nama lengkap
- **TINGGI_BADAN** - dalam cm
- **BERAT_BADAN** - dalam kg
- **LINGKAR_PERUT** - dalam cm
- **TEKANAN_DARAH_SISTOL** - angka sistol (mmHg)
- **TEKANAN_DARAH_DIASTOL** - angka diastol (mmHg)
- **GULA_DARAH** - nilai gula darah (mg/dL)

### Validasi Data:
- NIK harus 16 digit angka
- NAMA tidak boleh kosong
- TINGGI_BADAN: 100-250 cm
- BERAT_BADAN: 20-200 kg
- LINGKAR_PERUT: 50-200 cm
- TEKANAN_DARAH: 60-200 mmHg
- GULA_DARAH: 40-500 mg/dL

## 🔧 Konfigurasi Environment (.env)

```
WEBSITE_URL=https://sehatindonesiaku.kemkes.go.id/ckg-pelayanan
DETAIL_URL=https://sehatindonesiaku.kemkes.go.id/ckg-pelayanan/detail-pemeriksaan
HEADLESS=true
TIMEOUT=10
CHROMEDRIVER_PATH=./drivers/chromedriver
```

## 📝 Command Line Options

```
python main.py [OPTIONS]

OPTIONS:
  --file FILE          Path ke file Excel (default: data/data_ckg.xlsx)
  --debug              Tampilkan browser saat running
  --dry-run            Test tanpa submit ke website
  --verbose            Verbose logging mode
  -h, --help           Tampilkan help
```

## 📂 Output

Setelah program selesai, Anda akan mendapatkan:

### 1. Log File
```
logs/automasi_2024-05-27_14-30-45.log
```

### 2. Summary Report
```
✅ AUTOMASI SELESAI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total Data: 100
Berhasil: 95
Gagal: 5
Success Rate: 95.0%
Durasi: 12 menit 30 detik
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Gagal:
- NIK: 1234567890123456 - Error: NIK tidak ditemukan
- NIK: 1234567890123457 - Error: Connection timeout
```

## ⚠️ Troubleshooting

### ChromeDriver tidak ditemukan
```bash
# Pastikan path benar di .env atau letakkan di folder drivers/
# Linux/Mac: chmod +x drivers/chromedriver
```

### Connection timeout
```bash
# Naikkan timeout di .env
TIMEOUT=20
```

### Element tidak ditemukan
```bash
# Buka website di browser dan inspect element (F12)
# Update selector di modules/form_filler.py sesuai struktur HTML aktual
```

### Excel file error
```bash
# Pastikan kolom tepat sesuai format
# Periksa di logs/ untuk error detail
```

## 🛠️ Development

### Edit Form Filler
File `modules/form_filler.py` berisi selector dan logic pengisian form. Jika website berubah struktur:

1. Buka DevTools (F12)
2. Inspect element form
3. Update selector di `modules/form_filler.py`

## 📞 Support & Issues

Jika ada masalah:
1. Lihat log file di `logs/`
2. Cek error message di console
3. Buka issue di GitHub

## 📄 License

MIT License

## 🤝 Kontribusi

Pull requests welcome!

---

**Dibuat dengan ❤️ untuk kemudahan administrasi kesehatan Indonesia**
