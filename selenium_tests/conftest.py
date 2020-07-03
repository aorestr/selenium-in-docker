# -*- coding: utf-8 -*-

import os.path
import pathlib
import pytest
from selenium import webdriver

from .page_objects.base import BasePage


IMPLICITLY_WAIT = 30
TESTING_URL = "http://automationpractice.com"
GECKODRIVER_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "geckodriver")


@pytest.fixture(scope="function")
def open_and_close_browser():
    driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.get(TESTING_URL)
    yield BasePage(driver)
    driver.close()
