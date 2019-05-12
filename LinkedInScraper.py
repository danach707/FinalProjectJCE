import WebScraper as ws
import Lists as l
from selenium.common import exceptions as seleniumExceptions
import StringOperations as s
import Enums as e
import traceback
import re

class LinkedinScraper(ws.Webscraper):

    def __init__(self, email, password):
        ws.Webscraper.__init__(self)
        self.loggedin = self.login(email, password)
        self.lists = l.Lists()
        # self.regex = re.compile()

    """ login function to linkedIn """
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
                self.driver.get("https://www.linkedin.com/uas/login")
                self.driver.find_element_by_id('username').send_keys(email)
                self.driver.find_element_by_id('password').send_keys(password)
                self.driver.find_element_by_xpath('//*[@type="submit"]').click()
            except seleniumExceptions.NoSuchElementException:
                print("No such element in the web page:\n"
                      "Cannot log in to LinkedIn")
        except:
            print("Cannot log in to LinkedIn.. maybe you entered wrong credentials?")
        return False



    """ scrap function. gets the user linkedin URL and scrap the information about this user """
    def scrap(self, profile_url):

        # gets the username and opens the linkedin URL:
        self.username = self.get_username(profile_url)
        self.driver.get(profile_url)

        # =============== first and last name ===============
        try:
            name = self.driver.find_element_by_css_selector(".pv-top-card-section__name").get_attribute('innerHTML')
            name = s.clean_data(name)
            self.lists.words.extend(name)
        except seleniumExceptions.NoSuchElementException:
            print("No name element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== current job ===============
        try:
            current_job = self.driver.find_element_by_css_selector(".pv-top-card-v2-section__company-name").get_attribute('innerHTML')
            current_job = s.clean_data(current_job)
            self.lists.words.extend(current_job)
        except seleniumExceptions.NoSuchElementException:
            print("No job element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== location of the job or where the user lives ===============
        try:
            location = self.driver.find_element_by_css_selector(".pv-top-card-section__location").get_attribute('innerHTML')
            location = s.clean_data(location)
            self.lists.words.extend(location)
        except seleniumExceptions.NoSuchElementException:
            print("No location element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== college ===============
        try:
            college = self.driver.find_element_by_css_selector(".pv-top-card-v2-section__school-name").get_attribute('innerHTML')
            college = s.clean_data(college)
            self.lists.words.extend(college)
        except seleniumExceptions.NoSuchElementException:
            print("No college element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== former experience ===============
        # try: # he doesnt like me here....
        #     experience = self.driver.find_elements_by_id("experience-section")
        #     experience = self.clean_result(experience)
        # except seleniumExceptions.NoSuchElementException:
        #     print("No experience element in the web page")

        # =============== Email ===============
        try:
            self.driver.get('https://www.linkedin.com/in/%s/detail/contact-info/' % self.username)
            email = self.driver.find_element_by_xpath(
                "//section[contains(@class,'ci-email')]/div/a").get_attribute('innerHTML')
            email = s.clean_data(email)
            self.lists.words.extend(s.parse_email(''.join(email), e.Mode_Words))
            self.lists.numbers.extend(s.parse_email(''.join(email), e.Mode_Numbers))

        except seleniumExceptions.NoSuchElementException:
            print("No email element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== date of birth ===============
        try:
            dob = self.driver.find_element_by_xpath(
                "//section[contains(@class,'ci-birthday')]/div/span").get_attribute('innerHTML')
            dob = s.clean_data(dob)
            self.lists.numbers.extend(self.handle_dob(dob))
        except seleniumExceptions.NoSuchElementException:
            print("No date of birth element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== phone number ===============
        try:
            phone = self.driver.find_element_by_xpath(
                "//section[contains(@class,'ci-phone')]/ul/li/span[contains(@class, 't-black']").get_attribute('innerHTML')
            phone = s.clean_data(phone)
            self.lists.numbers.extend(phone)
        except seleniumExceptions.NoSuchElementException:
            print("No phone element in the web page")
        except Exception:
            traceback.print_exc()

    """ gets the linkedin URL and returns the username """
    def get_username(self, url):
        l = url.split('/')
        if l[-1] == '':
            del l[-1]
        return l[-1]

    """ the the date of birth in format 'month day' and returns the matching numbers """
    def handle_dob(self, dob):

        try:
            month_word = dob[0]
            day = dob[1]
        except IndexError:
            print("Error parsing date of birth")
            return []

        for month_num, month in enumerate(e.months, start=1):
            if month == month_word:
                return [str(month_num), day]
        return [day]




