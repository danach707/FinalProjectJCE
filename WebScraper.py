import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


class WebScraper:

    def __init__(self):
        options = Options()
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-infobars")
        options.add_argument("--mute-audio")
        # options.add_argument("headless")
        self.driver = webdriver.Chrome(executable_path='./going_headless/chromedriver.exe', options=options)

    def login(self, email, password):
        try:
            self.driver.get("https://www.facebook.com")
            # driver.minimize_window()

            self.driver.find_element_by_id('email').send_keys(email)
            self.driver.find_element_by_id('pass').send_keys(password)
            self.driver.find_element_by_id('loginbutton').click()

        except:
            print("Please replace the Chrome Web Driver with the latest one from"
                  "\nhttp://chromedriver.chromium.org/downloads")
            exit()
            # magnifying_glass = driver.find_element_by_id("js-hf")
            # if magnifying_glass.is_displayed():
            #   magnifying_glass.get_property()
            #   print("found")
            # else:
            #   #menu_button = driver.find_element_by_css_selector(".menu-trigger.local")
            #   #menu_button.click()
            #   print("not found")

    def getabout(self, username):
        self.driver.get("https://www.facebook.com/%s/about" % username)


if __name__ == '__main__':

    email = 'ronrichard906@gmail.com'
    password = 'password1234'
    username = 'danac0o'

    scraper = WebScraper()
    scraper.login(email, password)
