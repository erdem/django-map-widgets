from datetime import datetime
import sys
from constants import SCREENSHOT_DUMP_LOCATION


class SeleniumScreenShotMixin(object):

    def take_screenshot(self):
        filename = self.get_filename()
        self.browser.get_screenshot_as_file(filename)

    def get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        return '{folder}/{classname}.{method}-{timestamp}.png'.format(
            folder=SCREENSHOT_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            timestamp=timestamp
        )

    def tearDown(self):
        if sys.exc_info()[0]:  # Returns the info of exception being handled
            self.take_screenshot()
        self.browser.quit()
