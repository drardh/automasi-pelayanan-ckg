from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import os

class FormFiller:
    """Mengisi form di website Sehat Indonesiaku"""
    
    def __init__(self, chromedriver_path, headless=True, timeout=10, logger=None, debug=False):
        """
        Initialize FormFiller
        
        Args:
            chromedriver_path: Path ke chromedriver
            headless: Jalankan browser di background
            timeout: Timeout untuk wait element
            logger: Logger instance
            debug: Show browser (override headless)
        """
        self.chromedriver_path = chromedriver_path
        self.headless = headless and not debug
        self.timeout = timeout
        self.logger = logger
        self.driver = None
    
    def start_driver(self) -> bool:
        """
        Start Chrome driver
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            chrome_options = Options()
            
            if self.headless:
                chrome_options.add_argument("--headless")
            
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            
            self.driver = webdriver.Chrome(
                self.chromedriver_path,
                options=chrome_options
            )
            
            if self.logger:
                self.logger.info("Chrome driver started")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error starting Chrome driver: {str(e)}")
            return False
    
    def stop_driver(self):
        """Stop Chrome driver"""
        if self.driver:
            self.driver.quit()
            if self.logger:
                self.logger.info("Chrome driver stopped")
    
    def open_website(self, url) -> bool:
        """
        Buka website
        
        Args:
            url: URL website
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            self.driver.get(url)
            time.sleep(2)
            
            if self.logger:
                self.logger.info(f"Website terbuka: {url}")
            
            return True
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error membuka website: {str(e)}")
            return False
    
    def fill_nik(self, nik) -> bool:
        """
        Isi field NIK
        
        Args:
            nik: Nomor NIK
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            # Try multiple selectors
            selectors = [
                (By.ID, 'nik'),
                (By.NAME, 'nik'),
                (By.ID, 'input_nik'),
                (By.NAME, 'input_nik'),
                (By.CSS_SELECTOR, 'input[placeholder*="NIK"]'),
                (By.CSS_SELECTOR, 'input[type="text"][id*="nik"]'),
            ]
            
            element = None
            for by, selector in selectors:
                try:
                    element = WebDriverWait(self.driver, self.timeout).until(
                        EC.presence_of_element_located((by, selector))
                    )
                    break
                except:
                    continue
            
            if element:
                element.clear()
                element.send_keys(str(nik))
                time.sleep(1)
                
                if self.logger:
                    self.logger.info(f"NIK terisi: {nik}")
                
                return True
            else:
                if self.logger:
                    self.logger.warning(f"NIK field tidak ditemukan")
                return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error mengisi NIK: {str(e)}")
            return False
    
    def fill_medical_data(self, data) -> bool:
        """
        Isi data pemeriksaan kesehatan
        
        Args:
            data: Dictionary berisi data pemeriksaan
                  {
                    'tinggi_badan': float,
                    'berat_badan': float,
                    'lingkar_perut': float,
                    'tekanan_darah_sistol': float,
                    'tekanan_darah_diastol': float,
                    'gula_darah': float
                  }
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            filled_count = 0
            
            # Map data ke field selectors
            field_map = {
                'tinggi_badan': ['tinggi_badan', 'tinggi', 'height', 'tb'],
                'berat_badan': ['berat_badan', 'berat', 'weight', 'bb'],
                'lingkar_perut': ['lingkar_perut', 'lingkar', 'waist', 'lp'],
                'tekanan_darah_sistol': ['sistol', 'tekanan_sistol', 'systolic'],
                'tekanan_darah_diastol': ['diastol', 'tekanan_diastol', 'diastolic'],
                'gula_darah': ['gula_darah', 'gula', 'blood_sugar', 'glucose']
            }
            
            for field_key, field_names in field_map.items():
                if field_key not in data:
                    continue
                
                value = str(data[field_key])
                
                # Try multiple selectors for each field
                for field_name in field_names:
                    selectors = [
                        (By.ID, field_name),
                        (By.NAME, field_name),
                        (By.ID, f'input_{field_name}'),
                        (By.NAME, f'input_{field_name}'),
                        (By.CSS_SELECTOR, f'input[placeholder*="{field_name}"]'),
                    ]
                    
                    for by, selector in selectors:
                        try:
                            element = WebDriverWait(self.driver, self.timeout).until(
                                EC.presence_of_element_located((by, selector))
                            )
                            element.clear()
                            element.send_keys(value)
                            time.sleep(0.5)
                            filled_count += 1
                            
                            if self.logger:
                                self.logger.debug(f"Field {field_key} terisi: {value}")
                            
                            break
                        except:
                            continue
                    else:
                        continue
                    break
            
            if self.logger:
                self.logger.info(f"Data pemeriksaan terisi: {filled_count} field")
            
            return filled_count > 0
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error mengisi data pemeriksaan: {str(e)}")
            return False
    
    def submit_form(self, dry_run=False) -> bool:
        """
        Submit form
        
        Args:
            dry_run: Jika True, hanya test tanpa submit
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            if dry_run:
                if self.logger:
                    self.logger.info("DRY-RUN: Form tidak disubmit")
                return True
            
            # Try to find and click submit button
            submit_selectors = [
                (By.ID, 'submit'),
                (By.NAME, 'submit'),
                (By.CSS_SELECTOR, 'button[type="submit"]'),
                (By.CSS_SELECTOR, 'button[id*="submit"]'),
                (By.XPATH, '//button[contains(text(), "Submit")]'),
                (By.XPATH, '//button[contains(text(), "Kirim")]'),
            ]
            
            for by, selector in submit_selectors:
                try:
                    button = WebDriverWait(self.driver, self.timeout).until(
                        EC.element_to_be_clickable((by, selector))
                    )
                    button.click()
                    time.sleep(2)
                    
                    if self.logger:
                        self.logger.success("Form berhasil disubmit")
                    
                    return True
                except:
                    continue
            
            if self.logger:
                self.logger.warning("Submit button tidak ditemukan")
            
            return False
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error submit form: {str(e)}")
            return False
