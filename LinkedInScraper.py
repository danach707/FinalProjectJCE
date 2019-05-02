import WebScraper as ws
import Lists as l
from selenium.common import exceptions as seleniumExceptions
import re


class LinkedinScraper(ws.Webscraper):

    def __init__(self, email, password):
        ws.Webscraper.__init__(self)
        self.loggedin = self.login(email, password)
        self.lists = l.Lists()
        self.regex = re.compile()

    def login(self, email, password):
        try:
            self.driver.get("https://www.linkedin.com")
            self.driver.maximize_window()

            # add nav__button-secondary for the times it not getting to linkedin login page
            self.driver.find_element_by_class_name('login-email').send_keys(email)
            self.wait_random()
            self.driver.find_element_by_class_name('login-password').send_keys(password)
            self.wait_random()
            self.driver.find_element_by_xpath('//*[@type="submit"]').click()
            self.wait_random()
            return True
        except seleniumExceptions.NoSuchElementException:
            try:
                self.driver.get("https://www.linkedin.com/uat/signin")
                self.driver.find_element_by_id('username').send_keys(email)
                self.driver.find_element_by_id('password').send_keys(password)
                self.driver.find_element_by_xpath('//*[@type="submit"]').click()
            except seleniumExceptions.NoSuchElementException:
                print("No such element in the web page:\n"
                      "Cannot log in to LinkedIn")
        except:
            print("Cannot log in to LinkedIn.. maybe you entered wrong credentials?")
        return False

    def scrap(self, profile_url):
        self.driver.get(profile_url)
        try:
            current_job = self.driver.find_element_by_css_selector(".pv-top-card-v2-section__company-name").get_attribute('innerHTML')
            current_job = current_job.strip()
            arr = current_job.split('\n')
            arr = filter()
            print(arr)
        except seleniumExceptions.NoSuchElementException:
            print("No job element in the web page")
        try:
            location = self.driver.find_element_by_css_selector(".pv-top-card-section__location").get_attribute('innerHTML')
            print(location)
        except seleniumExceptions.NoSuchElementException:
            print("No location element in the web page")
        try:
            college = self.driver.find_element_by_css_selector(".pv-top-card-v2-section__school-name").get_attribute('innerHTML')
            print(college)
        except seleniumExceptions.NoSuchElementException:
            print("No college element in the web page")
        try: # he doesnt like me here....
            experience = self.driver.find_elements_by_id("experience-section")
            print(experience)
        except seleniumExceptions.NoSuchElementException:
            print("No experience element in the web page")


    # def get_experience(self, exp_list):








































if __name__ == '__main__':

        email = 'ronrichard907@gmail.com'
        password = 'qawsed1029'
        username = 'ron-richard-338201186'

        scraper = LinkedinScraper(email, password)
        if scraper.loggedin is True:
            scraper.scrap('https://www.linkedin.com/in/dana-cohen-957954143/')