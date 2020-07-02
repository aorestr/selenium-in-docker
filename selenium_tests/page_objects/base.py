# -*- coding: utf-8 -*-


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage(object):

    """
    Base class to initialize the base page that will be called from all pages
    """

    BASE_URL = "http://automationpractice.com/index.php"
    page_uri = ""

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
    def _web_driver_waiter(self):
        return WebDriverWait(self._driver, self._elements_timeout)

    def _get_element(self, xpath):
        """
        Wait for a element to be present on the screen
        :param xpath: xpath of the element to wait for
        :return: the WebElement
        """
        return self._web_driver_waiter().until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )

    def title_matches(self):
        """
        Make sure the title of the page matches the expected title
        :return:
        """
        url = self.BASE_URL + self.page_uri
        assert url in self._driver.title, "URL '{}' not in the title of the page"

    def wait_for_page_to_load(self):
        self.logo_image
