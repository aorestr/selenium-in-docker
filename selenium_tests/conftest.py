# -*- coding: utf-8 -*-

import os.path
import pathlib
from typing import Final
import pytest
from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from .page_objects.base import BasePage


IMPLICITLY_WAIT: Final = 30
TESTING_URL: Final = "http://automationpractice.com"
GECKODRIVER_PATH: Final = os.path.join(pathlib.Path(__file__).parent.absolute(), "geckodriver")


def pytest_addoption(parser):
    """
    If we use the '--remote' flag, tests will try to be run against a Docker container on port 4444
    :param parser:
    :return:
    """
    parser.addoption(
        "--remote", action="store_true", default=False,
        help="Set this flag if the driver you are using is not on the local system"
    )
    parser.addoption(
        "--rmt-host", action="store", default="localhost", type=str,
        help="Set the host name or the host IP of the system who contains the web driver. By default 'localhost'"
    )
    parser.addoption(
        "--rmt-port", action="store", default=4444, type=int,
        help="Set the port where the host who has the driver is listening. By default '4444'"
    )


@pytest.fixture(scope="session")
def get_driver(request) -> WebDriver:
    """
    Generate the Selenium driver that will be used by the tests
    :param request:
    :return: a callable that generates the driverSelenium WebDriver instance
    """
    if request.config.getoption("--remote"):
        url = "http://{host}:{port}/wd/hub".format(
            host=request.config.getoption("--rmt-host"), port=request.config.getoption("--rmt-port")
        )
        return webdriver.Remote(url, DesiredCapabilities.FIREFOX)
    else:
        return webdriver.Firefox(executable_path=GECKODRIVER_PATH)


@pytest.fixture(scope="function")
def open_and_close_browser(get_driver: WebDriver) -> BasePage:
    """
    Open the browser and when the test is done it closes it
    :param get_driver: fixture that returns the Selenium driver
    :return: a BasePage instance
    """
    get_driver.implicitly_wait(IMPLICITLY_WAIT)
    get_driver.get(TESTING_URL)
    return BasePage(get_driver)
