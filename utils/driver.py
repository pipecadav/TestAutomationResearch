from os import path

import allure
from appium import webdriver as appium_driver
from loguru import logger
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager

from config_file import get_capabilities
from model.test_data import TestData
from utils.common import get_env_browser, get_env_var
from utils.constants import WindowSize


def get_window_size():
    """
    Get window size for tablet or desktop
    :return: width, height
    """
    if get_env_var("RESPONSIVE") == WindowSize.tablet.name:
        width = WindowSize.tablet.value
    else:
        width = WindowSize.desktop.value
    return width, WindowSize.height.value


class Driver:
    """
    Setup driver class
    """

    width, height = get_window_size()
    options = None

    @allure.step("Init webdriver")
    def init_driver(self):
        """
        Init driver
        :return: webdriver object
        """
        logger.info("Init webdriver")
        driver = self._get_browser()
        driver.delete_all_cookies()
        driver.get(TestData().get_base_url())
        return driver

    @allure.step("Init appium driver")
    def init_mobile_driver(self):
        """
        Init Mobile driver
        :return: appium driver object
        """
        return appium_driver.Remote("http://0.0.0.0:4723/wd/hub", get_capabilities())

    def _get_browser(self):
        """
        Get driver by selected driver in env variables
        :return: webdriver object
        """
        browser = get_env_browser()
        if browser == "firefox":
            driver = self._get_firefox()
        else:
            driver = self._get_chrome()
        driver.set_window_size(self.width, self.height)
        return driver

    def _add_headless(self):
        """
        Add headless to options
        """
        self.options.add_argument("headless")

    def _get_chrome(self):
        """
        Get Chrome driver
        :return: webdriver object
        """
        self.options = webdriver.ChromeOptions()
        if bool(int(get_env_var("HEADLESS", default=1))):
            self._add_headless()
            self.options.add_argument("--window-size={}x{}".format(self.width, self.height))
        return webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()), options=self.options
        )

    def _get_firefox(self):
        """
        Get Firefox driver
        :return: webdriver object
        """
        self.options = webdriver.FirefoxOptions()
        if bool(int(get_env_var("HEADLESS", default=1))):
            self._add_headless()
            self.options.add_argument("--width=" + self.width)
            self.options.add_argument("--height=" + self.height)
        service = FirefoxService(GeckoDriverManager().install(), log_path=path.devnull)
        return webdriver.Firefox(service=service, options=self.options)
