import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from random import randint
from time import sleep
import re

class Webscraper:

    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--start-maximized")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")
        self.driver = webdriver.Chrome(executable_path='./driver/chromedriver.exe', options=options)
        self.data_clean_regex = re.compile(r'^[\w]+[A-Za-z0-9|\W]*[\w]+$')

    def wait_random(self):
        sleep(randint(2, 15))

