from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import os

class BrowserClient:
    def __init__(self):
        self.driver = self.init_chrome_driver()
        self.driver.maximize_window()

    def get_chrome_options(self):
        options = webdriver.ChromeOptions()
        home_dir_windows = os.environ['USERPROFILE']
        options.add_argument(r"user-data-dir={}\AppData\Local\Google\Chrome\Selenium Data".format(home_dir_windows))
        options.add_argument("--no-sandbox")
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        return options

    def init_chrome_driver(self, executable_paths=r".\chromedriver.exe"):
        service = webdriver.ChromeService(executable_path=executable_paths)
        options = self.get_chrome_options()
        driver = webdriver.Chrome(service=service, options=options)
        return driver

    def get(self, url):
        self.driver.get(url)

    def get_page_source(self):
        return self.driver.page_source

    def wait_for_element(self, by, value, timeout=20):
        WebDriverWait(self.driver, timeout).until(lambda d: d.find_element(by, value).is_displayed())

    def close(self):
        self.driver.close()
