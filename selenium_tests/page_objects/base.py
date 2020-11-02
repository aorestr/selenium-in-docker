# -*- coding: utf-8 -*-


from selenium.webdriver.remote.webelement import WebElement


class BasePage(object):

    """
    Base class to initialize the base page that will be called from all pages
    """

    BASE_URL = "http://automationpractice.com/index.php"
    page_uri = ""
    BASE_TITLE = "My Store"
    specific_title = ""

    def __init__(self, driver):
        self._driver = driver
        self.wait_for_page_to_load()
        self._current_url_matches()
        self._title_matches()

    # XPATH locators
    _logo_image_locator = "//img[@class='logo img-responsive']"
    _search_input_locator = "//input[@id='search_query_top']"
    _search_button_locator = "//button[@name='submit_search']"

    # Web elements
    @property
    def logo_image(self):
        return self._get_element(self._logo_image_locator)

    @property
    def search_input(self):
        return self._get_element(self._search_input_locator)

    @search_input.setter
    def search_input(self, query):
        self.search_input.clear()
        self.search_input.send_keys(query)

    @property
    def search_button(self):
        return self._get_element(self._search_button_locator)

    # Methods
    def _get_element(self, xpath: str) -> WebElement:
        """
        Wait for a element to be present on the screen
        :param xpath: xpath of the element to wait for
        :return: the WebElement
        """
        return self._driver.find_element_by_xpath(xpath)

    def _current_url_matches(self):
        """
        Make sure the current url of the page matches the expected title
        :return:
        """
        url = self.BASE_URL + "" if self.page_uri == "" else "?{}".format(self.page_uri)
        current_url = self._driver.current_url
        assert url in current_url, "URL '{0}' not on the current URL of the page ('{1}')".format(url, current_url)

    def _title_matches(self):
        """
        Make sure the title of the page matches the expected title
        :return:
        """
        title = "" if self.specific_title == "" else "{} - ".format(self.specific_title) + self.BASE_TITLE
        current_title = self._driver.title
        assert title in current_title, "Name '{0}' not on the title of the page ('{1}')".format(title, current_title)

    def search_product(self, product):
        """
        Search for a product
        :param product: name to search by
        :return: a SearchPage instance
        """
        from . import SearchPage    # not a good praxis but it's a way of avoiding circular imports
        self.search_input = product
        self.search_button.click()
        return SearchPage(self._driver)

    def wait_for_page_to_load(self):
        """
        Wait for some web elements to show up on the screen
        :return:
        """
        self.logo_image
        self.search_input
