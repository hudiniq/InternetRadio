import os
import pathlib
from io import BytesIO
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

current_folder = pathlib.Path(__file__).parent.absolute()

options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--incognito')
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--proxy-server='direct://'")
options.add_argument("--proxy-bypass-list=*")
options.add_argument("--start-maximized")
options.add_argument('--headless')

class Harvester():

    def __init__(self):
        self.url = 'https://rockradio.si'
        self.driver = webdriver.Chrome(str(current_folder) + "\\Chrome\\chromedriver.exe", chrome_options=options)
        self.driver.get(self.url)

        self.res = requests.get(self.url)
        self.html_page = self.res.content
        self.soup = BeautifulSoup(self.html_page, "lxml")
        

    def fetch_img(self):
        self.output_link = self.soup.find("img", {"class":"music-track-cover"})
        # self.output_link = self.driver.find_element_by_css_selector('.music-track-cover').get_attribute('innerHTML')
        self.img_tag = str(self.output_link).split()

        self.img_url = self.img_tag[-1][5:]
        self.img_url = self.img_url[:-3]
        
        self.response = requests.get(self.img_url)
        self.img_data = BytesIO(self.response.content)

        return self.img_data

    def fetch_song(self):
        self.artist = str(self.driver.find_elements_by_css_selector('.music-track-artist')[1].text)
        self.song = str(self.driver.find_elements_by_css_selector('.music-track-title')[1].text)
        return self.artist + " - " + self.song

    def kill(self):
        self.driver.close()
        self.driver.quit()