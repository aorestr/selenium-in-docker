from .test_base_class import TestBase
from ..page_objects.base import BasePage


class TestDummy(TestBase):

    @staticmethod
    def test_dummy_01(go_to_base_page: BasePage):
        """
        Do nothing
        :return:
        """
        pass

    @staticmethod
    def test_dummy_02(go_to_base_page: BasePage):
        """
        Do nothing
        :return:
        """
        pass
