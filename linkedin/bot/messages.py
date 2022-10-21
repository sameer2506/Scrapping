import os.path
import pickle
import random
import time
from datetime import datetime

from django.db.models import Q
from pytz import timezone
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

from linkedin.models import LinkedInProfile


class SendMessages:
    def __init__(self):
        # self.time = random.randint(20, 25)
        self.time = 1
        if not os.path.exists("data"):
            os.makedirs("data")

        print("Starting driver")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def login(self):
        print("Logging in")
        self.driver.get('https://www.linkedin.com/login')
        time.sleep(self.time)

        self.driver.find_element(By.ID, 'username').send_keys(email())
        self.driver.find_element(By.ID, 'password').send_keys(password())

        self.driver.find_element(By.XPATH, "//button[@aria-label='Sign in']").click()
        time.sleep(self.time)

    def save_cookie(self, path):
        with open(path, 'wb') as filehandler:
            pickle.dump(self.driver.get_cookies(), filehandler)

    def load_cookie(self, path):
        with open(path, 'rb') as cookiesFile:
            cookies = pickle.load(cookiesFile)
            for cookie in cookies:
                self.driver.add_cookie(cookie)

    def close_session(self):
        print("Closing session")
        self.driver.close()

    def check_exists_by_xpath(self, xpath):
        try:
            self.driver.find_element(By.XPATH, xpath)
        except NoSuchElementException:
            print("False")
            return False
        print("True")
        return True

    def check_exists(self, element, sel):
        try:
            self.driver.find_element(element, sel)
        except NoSuchElementException:
            return False
        return True

    def connect_request_sent(self, message, linkedin):
        is_sent = False

        if self.check_user(message, linkedin):
            is_sent = True

        return is_sent

    def check_user(self, message, url):
        print("check_user function")
        request_sent = False
        try:
            self.driver.get(url)
            time.sleep(self.time)

            selector = "pv-top-card-v2-ctas"

            # buttons = self.driver.find_element(By.CLASS_NAME, selector).text.splitlines()
            # print(buttons)

            # buttons = self.driver.find_element_by_css_selector(CSS_SELECTOR['buttons']).text.splitlines()

            buttons = self.driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR['buttons']).text.splitlines()
            print(buttons)
            time.sleep(5)

            if buttons[0].lower() == "message" or buttons[0].lower() == "follow":
                print("debug")
                request_sent = self.more_button(request_sent, message)

            elif buttons[0].lower() == "pending":
                request_sent = True

            else:
                button_list = self.driver.find_element_by_css_selector(CSS_SELECTOR['buttons'])
                button_list.find_element_by_class_name('artdeco-button').click()
                time.sleep(self.time)
                request_sent = self.add_note(self.driver, request_sent, message)
            # self.driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR['connect_button']).click()
            # time.sleep(self.time)
            # request_sent = self.add_note(request_sent, message)

            return request_sent

        except Exception as e:
            print(e)
            return request_sent

    def more_button(self, request_sent, message):
        print("more_button function")
        try:
            self.driver.find_elements_by_css_selector(CSS_SELECTOR['more_button'])[1].click()
            time.sleep(self.time)

            i = 1
            for item in self.driver.find_elements_by_css_selector(CSS_SELECTOR['more_button_dropdown']):
                if item.text == "Connect":
                    item.click()
                    time.sleep(self.time)

                elif item.text == "Pending":
                    request_sent = True
                    return request_sent
                i += 1

            request_sent = self.inside_connect_button(request_sent, message)
            return request_sent

        except Exception as ex:
            print("2", ex)
            return request_sent

    def inside_connect_button(self, request_sent, message):
        print("inside_connect_button function")
        try:
            self.driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR['connect_inside_button']).click()
            time.sleep(self.time)
            request_sent = self.add_note(request_sent, message)
            return request_sent

        except Exception as ex:
            print("3", ex)
            return request_sent

    def add_note(self, driver, request_sent, message):
        print("add_note function")
        try:
            # add note
            self.driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR['add_note_button']).click()

            note_area = self.driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR['note_area'])
            time.sleep(self.time)
            # print(message)
            note_area.send_keys(message)
            time.sleep(self.time)

            # send button
            self.driver.find_element(By.CSS_SELECTOR, CSS_SELECTOR['send_button']).click()
            request_sent = True
            time.sleep(self.time)
            return request_sent
        except Exception as ex:
            print(ex)
            return request_sent

    def run(self):
        self.driver.maximize_window()
        if os.path.exists("data/cookies.txt"):
            self.driver.get("https://www.linkedin.com/")
            self.load_cookie("data/cookies.txt")
            self.driver.get("https://www.linkedin.com/")
        else:
            self.login()
            self.save_cookie("data/cookies.txt")

        time.sleep(self.time)

        profile_list = LinkedInProfile.objects.filter(
            ~Q(status="messageSent") & ~Q(status="visit")
        )

        message_count = 0
        profile_view = 0

        for data in profile_list:

            if profile_view == 80:
                break

            if message_count == 10:
                break
            profile_id = data.id
            name = data.fullName
            link = data.linkedInUrl
            name_data = name.split()
            first_name = name_data[0]
            try:
                # print("Profile viewing ", profile_view)
                print("Searching ", name)

                if first_name == "Status":
                    message = get_message("")
                else:
                    message = get_message(first_name)

                if link != '':
                    if self.connect_request_sent(message, link):
                        profile_view += 1
                        print(profile_view, "Updated", name, link)

                        profile_item = LinkedInProfile.objects.get(id=profile_id)
                        # updated_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                        profile_item.status = "messageSent"
                        # profile_item.updatedOn = updated_time
                        profile_item.save()

                        print("Message sent to ", name)
                        message_count += 1
                        print("Message count ", message_count)
                        time.sleep(self.time)

                    else:
                        profile_item = LinkedInProfile.objects.get(id=profile_id)
                        # updated_time = datetime.now(timezone("Asia/Kolkata")).strftime('%Y-%m-%d %H:%M:%S.%f')
                        profile_item.status = "visit"
                        # profile_item.updatedOn = updated_time
                        profile_item.save()
                        print(profile_view, "Unable to send", name, link)
                        time.sleep(self.time)

            except Exception as e:
                print(e)

        print("Message Send Successfully")


def email():
    email2 = "sameerkumar081505@gmail.com"
    return email2


# password_data = "$=,db)qQ-W+)3f@Z"
def password():
    password2 = "Sameer@123"
    return password2


def get_link(page):
    link = f"https://www.linkedin.com/search/results/people/?geoUrn=%5B%22102713980%22%5D&industry=%5B%2296%22%5D" \
           f"&keywords=%22CEO%22%20OR%20%22FOUNDER%22%20OR%20%22OWNER%22&origin=FACETED_SEARCH&page={page}&sid=%3Bmk "
    return link


def world_start_up(page):
    link = f"https://www.linkedin.com/search/results/people/?industry=%5B%2296%22%5D&keywords=%22CEO%22%20OR%20" \
           f"%22FOUNDER%22%20OR%20%22OWNER%22&origin=FACETED_SEARCH&page={page}&sid=i0q "
    return link


def get_message(name):
    message = f"Hi {name},\n" \
              "Thank you for accepting my request.\n" \
              "I'm a good Android Developer with 6 months of experience in the Kotlin language.\n" \
              "Looking forward to discussing with you if you've any requirements related to Android Developer."
    return message


CSS_SELECTOR = {
    "buttons": "div.pv-top-card-v2-ctas.display-flex.pt3",
    "employees": "span.link-without-visited-state.t-bold.t-black--light",
    "profile_detail": "div.entity-result__content.entity-result__divider.pt3.pb3.t-12.t-black--light",
    "result": "div.pb2.t-black--light.t-14",
    "profile_heading": "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words",
    "desc": "div.text-body-medium.break-words",
    "emp_button": "div.display-flex.mt2.mb1",
    "company_detail": "div.block.mt2",
    "company_website": "a.ember-view.org-top-card-primary-actions__action",
    # driver.find_elements_by_css_selector('div.artdeco-dropdown.artdeco-dropdown--placement-bottom.artdeco-dropdown--justification-left.ember-view')
    'more_button': 'button.artdeco-dropdown__trigger.artdeco-dropdown__trigger--placement-bottom.ember-view.pvs-profile-actions__action.artdeco-button.artdeco-button--secondary.artdeco-button--muted.artdeco-button--2',
    'more_button_dropdown': 'span.display-flex.t-normal',
    'connect_inside_button': 'button.mr2.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view',
    'add_note_button': 'button.mr1.artdeco-button.artdeco-button--muted.artdeco-button--2.artdeco-button--secondary.ember-view',
    #             textarea.ember-text-area.ember-view.connect-button-send-invite__custom-message.mb3
    'note_area': 'textarea.ember-text-area.ember-view.connect-button-send-invite__custom-message.mb3',
    'send_button': 'button.ml1.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view',
    'connect_button': 'button.artdeco-button.artdeco-button--2.artdeco-button--primary.ember-view.pvs-profile-actions__action',

}
