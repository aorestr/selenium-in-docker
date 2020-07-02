# -*- coding: utf-8 -*-


from selenium.webdriver.support.ui import WebDriverWait


class BasePage(object):

    """
    Base class to initialize the base page that will be called from all pages
    """

    BASE_URL = "http://automationpractice.com/index.php"
    page_uri = ""
    BASE_TITLE = "My Store"
    specific_title = ""

    def __init__(self, driver, elements_timeout):
        self._driver = driver
        self._elements_timeout = elements_timeout
        self.wait_for_page_to_load()
        self.title_matches()

    # XPATH locators
    __logo_image_locator = "//img[@class='logo img-responsive']"

    # Web elements
    @property
    def logo_image(self):
        return self._get_element(self.__logo_image_locator)

    # Methods
    @property
    def _web_driver_waiter(self):
        """
        WebDriverWait object in case it's needed
        :return:
        """
        return WebDriverWait(self._driver, self._elements_timeout)

    def _get_element(self, xpath):
        """
        Wait for a element to be present on the screen
        :param xpath: xpath of the element to wait for
        :return: the WebElement
        """
        self._driver.find_element_by_xpath(xpath)

    def current_url_matches(self):
        """
        Make sure the current url of the page matches the expected title
        :return:
        """
        url = self.BASE_URL + self.page_uri
        current_url = self._driver.current_url
        assert url in current_url, "URL '{0}' not on the current URL of the page ('{1}')".format(url, current_url)

    def title_matches(self):
        """
        Make sure the title of the page matches the expected title
        :return:
        """
        title = self.specific_title + self.BASE_TITLE
        current_title = self._driver.title
        assert title in current_title, "Name '{0}' not on the title of the page ('{1}')".format(title, current_title)

    def wait_for_page_to_load(self):
        """
        Wait for some web elements to show up on the screen
        :return:
        """
        self.logo_image
