import pandas as pd
import os
from typing import List, Dict

class ExcelReader:
    """Membaca dan validasi data dari file Excel"""
    
    # Required columns
    REQUIRED_COLUMNS = ['NIK', 'NAMA', 'TINGGI_BADAN', 'BERAT_BADAN', 
                       'LINGKAR_PERUT', 'TEKANAN_DARAH_SISTOL', 
                       'TEKANAN_DARAH_DIASTOL', 'GULA_DARAH']
    
    def __init__(self, file_path, logger=None):
        """
        Initialize Excel reader
        
        Args:
            file_path: Path ke file Excel
            logger: Logger instance
        """
        self.file_path = file_path
        self.logger = logger
        self.df = None
    
    def read(self) -> bool:
        """
        Baca file Excel
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            if not os.path.exists(self.file_path):
                if self.logger:
                    self.logger.error(f"File tidak ditemukan: {self.file_path}")
                return False
            
            self.df = pd.read_excel(self.file_path)
            
            if self.logger:
                self.logger.success(f"File Excel berhasil dibaca: {self.file_path}")
                self.logger.info(f"Total baris data: {len(self.df)}")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error membaca Excel: {str(e)}")
            return False
    
    def validate(self) -> Dict[str, any]:
        """
        Validasi data
        
        Returns:
            Dictionary berisi hasil validasi
        """
        if self.df is None:
            return {'valid': False, 'errors': ['Data belum dibaca']}
        
        errors = []
        
        # Check required columns
        missing_columns = [col for col in self.REQUIRED_COLUMNS if col not in self.df.columns]
        if missing_columns:
            errors.append(f"Kolom yang hilang: {', '.join(missing_columns)}")
        
        # Validate data
        validation_errors = []
        for idx, row in self.df.iterrows():
            row_errors = self._validate_row(row, idx)
            validation_errors.extend(row_errors)
        
        if validation_errors:
            errors.extend(validation_errors)
        
        valid = len(errors) == 0
        
        if self.logger:
            if valid:
                self.logger.success("Validasi data berhasil")
            else:
                self.logger.warning(f"Validasi gagal dengan {len(errors)} error")
                for error in errors[:10]:  # Log max 10 errors
                    self.logger.warning(f"  - {error}")
        
        return {
            'valid': valid,
            'errors': errors,
            'total_errors': len(errors)
        }
    
    def _validate_row(self, row, idx) -> List[str]:
        """Validasi satu baris data"""
        errors = []
        nik = str(row.get('NIK', ''))
        
        # Validasi NIK
        if not nik or len(nik) != 16 or not nik.isdigit():
            errors.append(f"Baris {idx+1}: NIK tidak valid (harus 16 digit)")
        
        # Validasi NAMA
        if not row.get('NAMA') or str(row.get('NAMA')).strip() == '':
            errors.append(f"Baris {idx+1}: Nama tidak boleh kosong")
        
        # Validasi numerik
        try:
            tinggi = float(row.get('TINGGI_BADAN', 0))
            if not (100 <= tinggi <= 250):
                errors.append(f"Baris {idx+1}: Tinggi badan harus 100-250 cm")
        except:
            errors.append(f"Baris {idx+1}: Tinggi badan harus angka")
        
        try:
            berat = float(row.get('BERAT_BADAN', 0))
            if not (20 <= berat <= 200):
                errors.append(f"Baris {idx+1}: Berat badan harus 20-200 kg")
        except:
            errors.append(f"Baris {idx+1}: Berat badan harus angka")
        
        try:
            lingkar = float(row.get('LINGKAR_PERUT', 0))
            if not (50 <= lingkar <= 200):
                errors.append(f"Baris {idx+1}: Lingkar perut harus 50-200 cm")
        except:
            errors.append(f"Baris {idx+1}: Lingkar perut harus angka")
        
        try:
            sistol = float(row.get('TEKANAN_DARAH_SISTOL', 0))
            if not (60 <= sistol <= 200):
                errors.append(f"Baris {idx+1}: Tekanan sistol harus 60-200 mmHg")
        except:
            errors.append(f"Baris {idx+1}: Tekanan sistol harus angka")
        
        try:
            diastol = float(row.get('TEKANAN_DARAH_DIASTOL', 0))
            if not (40 <= diastol <= 150):
                errors.append(f"Baris {idx+1}: Tekanan diastol harus 40-150 mmHg")
        except:
            errors.append(f"Baris {idx+1}: Tekanan diastol harus angka")
        
        try:
            gula = float(row.get('GULA_DARAH', 0))
            if not (40 <= gula <= 500):
                errors.append(f"Baris {idx+1}: Gula darah harus 40-500 mg/dL")
        except:
            errors.append(f"Baris {idx+1}: Gula darah harus angka")
        
        return errors
    
    def get_data(self) -> List[Dict]:
        """
        Get data as list of dictionaries
        
        Returns:
            List of dictionaries containing row data
        """
        if self.df is None:
            return []
        
        return self.df.to_dict(orient='records')
