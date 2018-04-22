from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class Browser():
    def __init__(self):
        print('starting browser')
        chrome_options = Options()  
        chrome_options.add_argument('--headless')  
        chrome_options.binary_location = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'    
        self.browser = webdriver.Chrome('chromedriver', chrome_options = chrome_options)

        #self.browser = webdriver.Chrome('chromedriver')

    def close_browser(self):
        print('closing browser')
        self.browser.quit()
        print('closed')

    def get_page(self, url):
        print('getting page')
        self.browser.get(url)

    def find_by_xpath(self, xpath):
        return self.browser.find_elements_by_xpath(xpath)
