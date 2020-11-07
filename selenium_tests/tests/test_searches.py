import pytest
from faker import Faker

from .test_base_class import TestBase
from ..page_objects.base import BasePage


class TestSearches(TestBase):

    @staticmethod
    # This line could not work if parallel execution is set
    # @pytest.mark.parametrize("fake_search", [Faker().text() for _ in range(3)])
    @pytest.mark.parametrize("fake_search", ["ishdbidsfba", "iehbfisbfibwf", "pewnfeowhfo"])
    def test_fake_search_returns_nothing(go_to_base_page: BasePage, fake_search: str):
        """
        Search for a non existing product
        :param go_to_base_page: fixture to open the browser and go to the base page
        :return:
        """
        base_page = go_to_base_page
        search_page = base_page.search_product(fake_search)
        error_msg = "Some results are found even after using the random string '{}'".format(fake_search)
        assert "No results were found for your search" in search_page.error_notification_text, error_msg
        assert 0 == search_page.results_counter_text, error_msg

    @staticmethod
    def test_empty_search_returns_nothing(go_to_base_page: BasePage):
        """
        Insert an empty query
        :param go_to_base_page: fixture to open and close the browser
        :return:
        """
        base_page = go_to_base_page
        search_page = base_page.search_product("")
        error_msg = "Some results are found even after inserting an empty string"
        assert "Please enter a search keyword" in search_page.error_notification_text, error_msg
        assert 0 == search_page.results_counter_text, error_msg
