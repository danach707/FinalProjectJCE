import WebScraper as ws
import Lists as l
from selenium.common import exceptions as seleniumExceptions


class FacebookScraper(ws.Webscraper):

    def __init__(self, email, password, username):
        ws.Webscraper.__init__(self)
        self.login(email, password)
        self.username = username
        self.lists = l.Lists()

    def login(self, email, password):
        try:
            self.driver.get("https://www.facebook.com")
            # driver.minimize_window()

            self.driver.find_element_by_id('email').send_keys(email)
            self.driver.find_element_by_id('pass').send_keys(password)
            self.driver.find_element_by_id('loginbutton').click()
        except:
            print("Cannot log in to Facebook")

    def get_education(self):
        self.driver.get("https://www.facebook.com/%s/about?section=education" % self.username)
        try:
            tmp = self.driver.find_element_by_class_name("profileLink")
            self.lists.words.append(tmp.get_attribute('innerText'))
            print(tmp.get_attribute('innerText'))
        except seleniumExceptions.NoSuchElementException:
            print("No such element in this profile")

    def get_family_members(self):
        self.driver.get("https://www.facebook.com/%s/about?section=relationship" % self.username)
        try:
            parent = self.driver.find_element_by_class_name("uiList fbProfileEditExperiences _4kg _4ks")
            child1 = parent.find_element_by_class_name()
            self.lists.words.append(tmp.get_attribute('innerText'))
            print(tmp.get_attribute('innerText'))
        except seleniumExceptions.NoSuchElementException:
            print("No such element in this profile")


if __name__ == '__main__':

    with open('creds.txt', 'r') as cr:
        email = cr.readline()
        password = cr.readline()
        username = cr.readline()

        scraper = FacebookScraper(email, password, username)
        scraper.get_education()
        scraper.get_family_members()

