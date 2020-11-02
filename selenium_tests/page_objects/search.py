# -*- coding: utf-8 -*-


from .base import BasePage


class SearchPage(BasePage):

    page_uri = "controller=search"
    specific_title = "Search"

    def __init__(self, driver):
        super(SearchPage, self).__init__(driver)

    # XPATH locators
    _results_counter_text_locator = "//span[@class='heading-counter']"
    _error_notification_text_locator = "//div[@id='center_column']/p[@class='alert alert-warning']"

    # Web elements
    @property
    def results_counter_text(self) -> int:
        """
        Returns the number of results of the search
        :return: the number of results of the search as an integer
        """
        return int(self._get_element(self._results_counter_text_locator).text.strip().split(" ")[0])

    @property
    def error_notification_text(self) -> str:
        return self._get_element(self._error_notification_text_locator).text.strip()

    # Methods
    def wait_for_page_to_load(self):
        """
        Wait for some web elements to show up on the screen
        :return:
        """
        super(SearchPage, self).wait_for_page_to_load()
        self.results_counter_text
