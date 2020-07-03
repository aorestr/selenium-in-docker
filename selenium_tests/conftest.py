# -*- coding: utf-8 -*-

import os.path
import pathlib
import pytest
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .page_objects.base import BasePage


IMPLICITLY_WAIT = 30
TESTING_URL = "http://automationpractice.com"
GECKODRIVER_PATH = os.path.join(pathlib.Path(__file__).parent.absolute(), "geckodriver")


def pytest_addoption(parser):
    """
    If we use the '--remote' flag, tests will try to be run against a Docker container on port 4444
    :param parser:
    :return:
    """
    parser.addoption("--remote", action="store_true", default=False, help="In case you run the tests using docker")


@pytest.fixture(scope="function")
def open_and_close_browser(request):
    """
    Open the browser and when the test is done it closes it
    :param request:
    :return: a BasePage instance
    """
    if request.config.getoption("--remote"):
        driver = webdriver.Remote("http://selenium-hub:4444/wd/hub", DesiredCapabilities.FIREFOX)
    else:
        driver = webdriver.Firefox(executable_path=GECKODRIVER_PATH)
    driver.implicitly_wait(IMPLICITLY_WAIT)
    driver.get(TESTING_URL)
    yield BasePage(driver)
    driver.close()
