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

        # =============== date of birth ===============
        try:
            self.wait_random()
            self.driver.get(profile_url+'/about?section=overview')
            self.wait_random()
            dob = self.driver.find_element_by_xpath('//ul[@data-overviewsection="contact_basic"]/li[1]/div/div[2]/span/div[2]').get_attribute(
                'innerHTML')
            print(dob)
            dob = s.clean_data(dob)
            dob = self.get_month_number(dob)
            if dob is not None:
                self.lists.numbers.extend(dob)
        except seleniumExceptions.NoSuchElementException:
            print("No date of birth element in the web page")
        except Exception:
            traceback.print_exc()

        # =============== family members =============== #

            # try:
            #     self.wait_random()
            #     self.driver.get(profile_url + '/about?section=all_relationships')
            #     self.wait_random()
            #     family_members = self.driver.find_elements_by_xpath('//*[@id="pagelet_eduwork"]/div/div/ul[1]')
            #     print('fam:', family_members)
            #
            #     i = 1
            #     print(family_members)
            #     for member in family_members:
            #         xpath = ".//li[{0}]/div/div/div/div/div[2]/div/a".format(i)
            #         wp = member.find_element_by_xpath(xpath).get_attribute('innerHTML')
            #         wp = s.clean_data(wp)
            #         self.lists.words.extend(wp)
            #         i += 1
            #
            # except seleniumExceptions.NoSuchElementException:
            #     print("No workplace element in the web page")
            # except Exception:
            #     traceback.print_exc()

        # =============== work places ===============
        try:
            self.wait_random()
            self.driver.get(profile_url + '/about?section=education')
            self.wait_random()
            workplaces = self.driver.find_elements_by_xpath('//*[@id="pagelet_eduwork"]/div/div/ul[1]')
            print('wps:', workplaces)

            i = 1
            print(workplaces)
            for workplace in workplaces:
                xpath = ".//li[{0}]/div/div/div/div/div[2]/div/a".format(i)
                wp = workplace.find_element_by_xpath(xpath).get_attribute('innerHTML')
                wp = s.clean_data(wp)
                self.lists.words.extend(wp)
                i += 1

        except seleniumExceptions.NoSuchElementException:
            print("No workplace element in the web page")
        except Exception:
            traceback.print_exc()


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



if __name__ == '__main__':

    with open('creds.txt', 'r') as cr:
        email = cr.readline()
        password = cr.readline()

        scraper = FacebookScraper(email, password)
        scraper.scrap('https://www.facebook.com/orsolya.magas/')
        print(scraper.lists.numbers, '\n', scraper.lists.words)

# //*[@id="u_85_0"]/div/div[2]/span/div[2]/span/ul/li hometown

# //*[@id="u_fetchstream_18_b"]/div[2]/ul[@data-overviewsection="contact_basic"]/li[1]/div/div[2]/span/div[2]