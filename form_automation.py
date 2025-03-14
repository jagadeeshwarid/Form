import yaml
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import time
import sys
from logger import setup_logger

class FormAutomation:
    def __init__(self, config_path='config.yaml'):
        self.logger = setup_logger()
        self.load_config(config_path)
        self.setup_browser()

    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as file:
                self.config = yaml.safe_load(file)
        except Exception as e:
            self.logger.error(f"Failed to load config: {str(e)}")
            sys.exit(1)

    def setup_browser(self):
        """Initialize Chrome WebDriver"""
        try:
            chrome_options = Options()
            # Required options for running in Replit
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--headless")  # Run in headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-extensions")
            
            # Add chrome_profile_path if it exists in config
            if 'chrome_profile_path' in self.config.get('browser', {}):
                chrome_options.add_argument(f"--user-data-dir={self.config['browser']['chrome_profile_path']}")
                self.logger.info("Using custom Chrome profile")

            service = Service(self.config['browser']['chrome_driver_path'])
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.logger.info("Browser initialized successfully")
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            sys.exit(1)

    def open_forms(self):
        """Open all configured forms in new tabs"""
        try:
            # First open a blank page
            self.driver.get("about:blank")

            # Open doubts forms
            for form in self.config['forms']['doubts']:
                self.driver.execute_script(f"window.open('{form['form_url']}', '_blank');")
                self.logger.info(f"Opened doubts form: {form['name']}")
                time.sleep(0.5)  # Reduced delay to prevent overwhelming the browser

            # Open feedback form
            feedback = self.config['forms']['feedback']
            self.driver.execute_script(f"window.open('{feedback['form_url']}', '_blank');")
            self.logger.info(f"Opened feedback form: {feedback['name']}")

            self.logger.info("Successfully opened all forms")
        except Exception as e:
            self.logger.error(f"Error opening forms: {str(e)}")
            return False
        return True

    def open_sheets(self):
        """Open all associated Google Sheets"""
        try:
            # Open sheets for doubts forms
            for form in self.config['forms']['doubts']:
                self.driver.execute_script(f"window.open('{form['sheet_url']}', '_blank');")
                self.logger.info(f"Opened sheet for: {form['name']}")
                time.sleep(0.5)  # Reduced delay to prevent overwhelming the browser

            # Open feedback sheet
            feedback = self.config['forms']['feedback']
            self.driver.execute_script(f"window.open('{feedback['sheet_url']}', '_blank');")
            self.logger.info(f"Opened feedback sheet: {feedback['name']}")

            self.logger.info("Successfully opened all sheets")
        except Exception as e:
            self.logger.error(f"Error opening sheets: {str(e)}")
            return False
        return True

    def cleanup(self):
        """Clean up browser resources"""
        try:
            self.logger.info("All Google Sheets have been opened successfully.")

            if hasattr(self, 'driver'):
                self.driver.quit()
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Google Forms and Sheets Automation')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    parser.add_argument('--forms-only', action='store_true', help='Open only forms, skip sheets')
    parser.add_argument('--sheets-only', action='store_true', help='Open only sheets, skip forms')
    args = parser.parse_args()

    automation = FormAutomation(args.config)

    try:
        if not args.sheets_only:
            automation.open_forms()
        if not args.forms_only:
            automation.open_sheets()
    except Exception as e:
        automation.logger.error(f"Unexpected error: {str(e)}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()
