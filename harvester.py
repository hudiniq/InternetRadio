import os
import pathlib
from io import BytesIO
import time
import requests
from bs4 import BeautifulSoup
from selenium import webdriver

current_folder = pathlib.Path(__file__).parent.absolute()
url = 'https://rockradio.si'

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
driver = webdriver.Chrome(str(current_folder) + "\\Chrome\\chromedriver.exe", chrome_options=options)


def fetch():
    driver.get(url)

def fetch_img():
    res = requests.get(url)
    html_page = res.content
    soup = BeautifulSoup(html_page, "lxml")

    output_link = soup.find("img", {"class":"music-track-cover"})
    # output_link = driver.find_element_by_css_selector('.music-track-cover').get_attribute('innerHTML')
    img_tag = str(output_link).split()

    img_url = img_tag[-1][5:]
    img_url = img_url[:-3]
    
    response = requests.get(img_url)
    img_data = BytesIO(response.content)

    return img_data

def fetch_song():
    artist = str(driver.find_elements_by_css_selector('.music-track-artist')[1].text)
    song = str(driver.find_elements_by_css_selector('.music-track-title')[1].text)
    return artist + " - " + song

def kill():
    driver.close()
    driver.quit()