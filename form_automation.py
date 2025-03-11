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
        """Initialize Chrome WebDriver with your profile"""
        try:
            chrome_options = Options()
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--disable-notifications")
            chrome_options.add_argument("--disable-software-rasterizer")
            chrome_options.add_argument("--disable-extensions")

            # ✅ Use your existing Chrome profile
            chrome_options.add_argument(f"--user-data-dir={self.config['browser']['chrome_profile_path']}")

            # Load ChromeDriver path from config
            service = Service(self.config['browser']['chrome_driver_path'])
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.logger.info("Browser initialized successfully with your Chrome Profile")
        except WebDriverException as e:
            self.logger.error(f"Failed to initialize browser: {str(e)}")
            sys.exit(1)

    def open_sheets(self):
        """Open all associated Google Sheets only"""
        try:
            # Open sheets for doubts forms
            for form in self.config['forms']['doubts']:
                self.driver.execute_script(f"window.open('{form['sheet_url']}', '_blank');")
                self.logger.info(f"Opened sheet for: {form['name']}")
                time.sleep(0.5)

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
        """Keep browser open until user manually closes it"""
        try:
            self.logger.info("All Google Sheets have been opened successfully.")
            self.logger.info("Close the browser manually when done.")
            input("Press Enter to close the browser once you're done...")

            if hasattr(self, 'driver'):
                self.driver.quit()
                self.logger.info("Browser closed successfully")
        except Exception as e:
            self.logger.error(f"Error during cleanup: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Google Sheets Automation')
    parser.add_argument('--config', default='config.yaml', help='Path to configuration file')
    args = parser.parse_args()

    # Initialize Automation
    automation = FormAutomation(args.config)

    try:
        automation.open_sheets()
    except Exception as e:
        automation.logger.error(f"Unexpected error: {str(e)}")
    finally:
        automation.cleanup()

if __name__ == "__main__":
    main()
