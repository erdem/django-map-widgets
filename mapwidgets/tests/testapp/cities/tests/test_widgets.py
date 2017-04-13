from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from selenium import webdriver

from mixins import SeleniumScreenShotMixin


class DummySeleniumTestCase(SeleniumScreenShotMixin, StaticLiveServerTestCase):

    def setUp(self):
        options = webdriver.ChromeOptions()
        options.add_argument("--no-sandbox")
        self.browser = webdriver.Remote(
            command_executor="http://selenium:4444/wd/hub",
            desired_capabilities=options.to_capabilities()
        )
        print self.live_server_url

    def test_user_registration(self):
        print "%s/%s/" % (self.live_server_url, "admin")
        self.browser.get("%s/%s/" % (self.live_server_url, "admin"))
        self.take_screenshot()
        print self.browser.title
