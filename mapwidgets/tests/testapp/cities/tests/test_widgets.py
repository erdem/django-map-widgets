from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver


class UserRegistrationSeleniumTestCase(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.get(self.live_server_url)

    def test_user_registration(self):
        self.browser.find_element("body").click()