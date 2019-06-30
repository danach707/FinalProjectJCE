import WebScraper as ws
import Lists as l
from selenium.common import exceptions as seleniumExceptions
import traceback
import StringOperations as s
import Enums as e


class FacebookScraper(ws.Webscraper):

    def __init__(self, email, password):
        ws.Webscraper.__init__(self)
        self.login(email, password)
        self.lists = l.Lists()

    def login(self, email, password):
        try:
            self.driver.get("https://www.facebook.com")
            self.driver.find_element_by_id('email').send_keys(email)
            self.wait_random()
            self.driver.find_element_by_id('pass').send_keys(password)
            self.wait_random()
            self.driver.find_element_by_id('loginbutton').click()
        except:
            print("Cannot log in to Facebook")

    def scrap(self, profile_url):
        profile_url = self.clean_url(profile_url)
        self.username = self.get_username(profile_url)

        self.driver.get(profile_url)
        self.wait_random()
        # =============== first and last name ===============
        try:
            name = self.driver.find_element_by_xpath("//span[@id='fb-timeline-cover-name']/a").get_attribute('innerHTML')
            name = s.clean_data(name)
            self.lists.words.extend(name)
        except seleniumExceptions.NoSuchElementException:
            print("No name element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== contact basic ==============

        try:
            self.driver.get(profile_url + '/about?section=overview')
            self.wait_random()
            contact_basic = self.driver\
                .find_elements_by_xpath('//ul[@data-overviewsection="contact_basic"]/li/div/div[2]/span')

            for item in contact_basic:
                item_name = item.find_element_by_xpath("./div[1]/span").get_attribute('innerHTML')

                if 'Phones' in item_name:
                    item_val = item.find_element_by_xpath("./div[2]/span").get_attribute('innerHTML')
                    print('found:', item_val)
                    self.handle_phones(item_val)
                if 'Birthday' in item_name:
                    item_val = item.find_element_by_xpath("./div[2]").get_attribute('innerHTML')
                    print('found:', item_val)
                    self.handle_dob(item_val)
                if 'Email' in item_name:
                    item_val = item.find_element_by_xpath("./div[2]/a").get_attribute('innerHTML')
                    print('found:', item_val)
                    self.handle_email(item_val)
                if 'Website' in item_name:
                    item_val = item.find_element_by_xpath("./div[2]/a").get_attribute('innerHTML')
                    print('found:', item_val)
                    self.handle_website(item_val)

        except seleniumExceptions.NoSuchElementException:
            print("No contact basic elements in the web page")
        except Exception:
            traceback.print_exc()

        # =============== family members =============== #

        try:
            self.driver.get(profile_url + '/about?section=relationship')
            self.wait_random()
            family_members = self.driver.find_elements_by_xpath(
                '//div[@id="family-relationships-pagelet"]/div/ul/li//div/div/div/div/div/div/div/span/a')

            i = 1
            for member in family_members:
                try:
                    wp = member.get_attribute('innerHTML')
                    print(wp)
                    wp = s.clean_data(wp)
                    self.lists.words.extend(wp)
                except seleniumExceptions.NoSuchElementException:
                    print('did not find family in %d' % i)
                    i += 1
                i += 1

        except seleniumExceptions.NoSuchElementException:
            print("No family elements in the web page")
        except Exception:
            traceback.print_exc()

        # =============== work places ===============
        try:
            self.wait_random()
            self.driver.get(profile_url + '/about?section=education')
            workplaces = self.driver.find_elements_by_xpath('//ul[contains(@class,"fbProfileEditExperiences")]')

            i = 1
            for workplace in workplaces:
                xpath = ".//li[contains(@class,'fbEditProfileViewExperience')][{0}]/div/div/div/div/div/div/a".format(i)
                wp = workplace.find_element_by_xpath(xpath).get_attribute('innerHTML')
                print(wp)
                wp = s.clean_data(wp)
                self.lists.words.extend(wp)
                i += 1

        except seleniumExceptions.NoSuchElementException:
            print("No workplace element in the web page")
        except Exception:
            traceback.print_exc()

        # quit browser
        self.wait_random()
        self.driver.quit()

    # ================ More Functions =================

    def handle_phones(self, phone):
        phone = phone.replace('-', '')
        self.lists.numbers.append(phone)

    def handle_dob(self, dob):
        dob = s.clean_data(dob)
        dob = self.get_month_number(dob)
        if dob is not None:
            self.lists.numbers.extend(dob)

    def handle_email(self, email):
        email = email.strip()
        self.lists.words.extend(s.parse_email(email, e.Mode_Words))
        self.lists.numbers.extend(s.parse_email(email, e.Mode_Numbers))

    def handle_website(self, website):
        website = website.strip()
        # take only the website name without http and suffixes
        res = website.split('/')
        res = res[-1]
        res = res.split('.')
        self.lists.words.append(res[0])

    def clean_url(self, profile_url):
        if profile_url[-1] == '/':
            profile_url = profile_url[:-1]
        return profile_url

    def get_month_number(self, dob):

        mon = dob[0]
        for month_num, month in enumerate(e.months, start=1):
            if month == mon:
                dob[0] = month_num
                return dob
