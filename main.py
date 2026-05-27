#!/usr/bin/env python3
"""
Automasi Entri Pelayanan Cek Kesehatan Gratis
Program untuk mengotomatisasi pengisian form entry pelayanan cek kesehatan gratis
di website Sehat Indonesiaku
"""

import argparse
import sys
import time
import os
from dotenv import load_dotenv
from datetime import datetime

from modules.logger import Logger
from modules.excel_reader import ExcelReader
from modules.form_filler import FormFiller

# Load environment variables
load_dotenv()

class AutomasiCKG:
    """Main automation class"""
    
    def __init__(self, debug=False, dry_run=False):
        """
        Initialize automasi
        
        Args:
            debug: Show browser
            dry_run: Test tanpa submit
        """
        self.debug = debug
        self.dry_run = dry_run
        self.logger = Logger("AutomasiCKG")
        self.stats = {
            'total': 0,
            'success': 0,
            'failed': 0,
            'errors': []
        }
    
    def run(self, excel_file):
        """
        Run automation
        
        Args:
            excel_file: Path ke file Excel
        
        Returns:
            Status automasi
        """
        start_time = datetime.now()
        
        self.logger.info("=" * 60)
        self.logger.info("🏥 AUTOMASI ENTRI PELAYANAN CEK KESEHATAN GRATIS")
        self.logger.info("=" * 60)
        
        # Read and validate Excel
        self.logger.info("\n📊 STEP 1: Membaca dan validasi data Excel")
        self.logger.info("-" * 60)
        
        reader = ExcelReader(excel_file, self.logger)
        
        if not reader.read():
            self.logger.error("Gagal membaca file Excel")
            return False
        
        validation_result = reader.validate()
        if not validation_result['valid']:
            self.logger.error(f"Validasi gagal: {validation_result['total_errors']} error ditemukan")
            return False
        
        data_list = reader.get_data()
        self.stats['total'] = len(data_list)
        self.logger.info(f"Total data yang akan diproses: {self.stats['total']}")
        
        # Initialize form filler
        self.logger.info("\n🌐 STEP 2: Inisialisasi browser")
        self.logger.info("-" * 60)
        
        chromedriver_path = os.getenv('CHROMEDRIVER_PATH', './drivers/chromedriver')
        website_url = os.getenv('WEBSITE_URL', 'https://sehatindonesiaku.kemkes.go.id/ckg-pelayanan')
        detail_url = os.getenv('DETAIL_URL', 'https://sehatindonesiaku.kemkes.go.id/ckg-pelayanan/detail-pemeriksaan')
        headless = os.getenv('HEADLESS', 'true').lower() == 'true'
        timeout = int(os.getenv('TIMEOUT', '10'))
        
        filler = FormFiller(
            chromedriver_path,
            headless=headless,
            timeout=timeout,
            logger=self.logger,
            debug=self.debug
        )
        
        if not filler.start_driver():
            self.logger.error("Gagal menjalankan Chrome driver")
            return False
        
        if self.dry_run:
            self.logger.warning("MODE DRY-RUN: Tidak akan submit data ke website")
        
        # Process each data
        self.logger.info("\n✍️  STEP 3: Mengisi dan submit form")
        self.logger.info("-" * 60)
        
        try:
            for idx, row_data in enumerate(data_list, 1):
                self.logger.info(f"\nData {idx}/{self.stats['total']}")
                
                nik = str(row_data.get('NIK', '')).strip()
                nama = str(row_data.get('NAMA', '')).strip()
                
                self.logger.info(f"  NIK: {nik}, Nama: {nama}")
                
                # Open website
                if not filler.open_website(website_url):
                    self.logger.error(f"Gagal membuka website")
                    self.stats['failed'] += 1
                    self.stats['errors'].append({
                        'nik': nik,
                        'error': 'Gagal membuka website'
                    })
                    continue
                
                # Fill NIK
                if not filler.fill_nik(nik):
                    self.logger.error(f"Gagal mengisi NIK")
                    self.stats['failed'] += 1
                    self.stats['errors'].append({
                        'nik': nik,
                        'error': 'Gagal mengisi NIK'
                    })
                    continue
                
                # Try to navigate to detail form
                try:
                    time.sleep(1)
                    filler.driver.get(detail_url)
                    time.sleep(2)
                except:
                    self.logger.warning("Navigasi ke detail form gagal, lanjut ke step berikutnya")
                
                # Fill medical data
                medical_data = {
                    'tinggi_badan': row_data.get('TINGGI_BADAN', 0),
                    'berat_badan': row_data.get('BERAT_BADAN', 0),
                    'lingkar_perut': row_data.get('LINGKAR_PERUT', 0),
                    'tekanan_darah_sistol': row_data.get('TEKANAN_DARAH_SISTOL', 0),
                    'tekanan_darah_diastol': row_data.get('TEKANAN_DARAH_DIASTOL', 0),
                    'gula_darah': row_data.get('GULA_DARAH', 0),
                }
                
                if not filler.fill_medical_data(medical_data):
                    self.logger.warning("Sebagian data pemeriksaan gagal diisi")
                
                # Submit form
                if not filler.submit_form(dry_run=self.dry_run):
                    self.logger.error("Gagal submit form")
                    self.stats['failed'] += 1
                    self.stats['errors'].append({
                        'nik': nik,
                        'error': 'Gagal submit form'
                    })
                    continue
                
                self.stats['success'] += 1
                self.logger.success(f"Data berhasil diproses")
                
                # Delay antar request
                time.sleep(2)
        
        except Exception as e:
            self.logger.error(f"Error saat processing: {str(e)}")
        
        finally:
            filler.stop_driver()
        
        # Print summary
        end_time = datetime.now()
        duration = end_time - start_time
        
        self.logger.info("\n" + "=" * 60)
        self.logger.info("📈 SUMMARY AUTOMASI")
        self.logger.info("=" * 60)
        self.logger.info(f"Total Data: {self.stats['total']}")
        self.logger.info(f"Berhasil: {self.stats['success']}")
        self.logger.info(f"Gagal: {self.stats['failed']}")
        
        if self.stats['total'] > 0:
            success_rate = (self.stats['success'] / self.stats['total']) * 100
            self.logger.info(f"Success Rate: {success_rate:.1f}%")
        
        self.logger.info(f"Durasi: {str(duration).split('.')[0]}")
        
        if self.stats['errors']:
            self.logger.info(f"\n❌ Data yang gagal ({len(self.stats['errors'])}):")
            for error_data in self.stats['errors'][:10]:
                self.logger.info(f"  - NIK {error_data['nik']}: {error_data['error']}")
            
            if len(self.stats['errors']) > 10:
                self.logger.info(f"  ... dan {len(self.stats['errors']) - 10} error lainnya")
        
        self.logger.info("=" * 60)
        
        if self.dry_run:
            self.logger.info("✅ DRY-RUN SELESAI (Data tidak disubmit)")
        else:
            self.logger.info("✅ AUTOMASI SELESAI")
        
        self.logger.info(f"Log file: {self.logger.log_file}")
        self.logger.info("=" * 60)
        
        return self.stats['failed'] == 0

def main():
    """Main function"""
    parser = argparse.ArgumentParser(
        description='Automasi Entri Pelayanan Cek Kesehatan Gratis',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Contoh penggunaan:
  python main.py --file data/data_ckg.xlsx
  python main.py --file data/data_ckg.xlsx --debug
  python main.py --file data/data_ckg.xlsx --dry-run
        """
    )
    
    parser.add_argument(
        '--file', '-f',
        type=str,
        default='data/data_ckg.xlsx',
        help='Path ke file Excel (default: data/data_ckg.xlsx)'
    )
    
    parser.add_argument(
        '--debug', '-d',
        action='store_true',
        help='Tampilkan browser saat running'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Test tanpa submit ke website'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Verbose logging mode'
    )
    
    args = parser.parse_args()
    
    # Validate file exists
    if not os.path.exists(args.file):
        print(f"❌ File tidak ditemukan: {args.file}")
        sys.exit(1)
    
    # Run automation
    automasi = AutomasiCKG(debug=args.debug, dry_run=args.dry_run)
    
    try:
        success = automasi.run(args.file)
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        automasi.logger.warning("\nAutomasi dihentikan oleh user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
