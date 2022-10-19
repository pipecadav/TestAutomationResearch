import os
from base64 import b64decode
from pathlib import Path
from typing import Union

import allure
import selenium.common.exceptions as exc
from appium.webdriver.common.touch_action import TouchAction
from loguru import logger as log
from selenium.webdriver import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait

from utils.common import get_current_time, get_env, get_env_browser, get_env_var
from utils.constants import BASE_DIR, MEDIUM_WAIT_TIME, NO_WAIT, WindowSize


class BaseScreen:
    """
    BaseScreen class
    """

    _driver = None
    _wait_time = MEDIUM_WAIT_TIME

    def _get_wait(self, wait_time=_wait_time):
        """
        Get wait for future expected conditions
        :param wait_time: wait default time
        :return: webDriverWait
        """
        return WebDriverWait(
            self._driver, wait_time, ignored_exceptions=[exc.ElementNotVisibleException]
        )

    @staticmethod
    def _get_locator_by_os(locator_info):
        """
        Get tuple with locator info if is a dict
        :param locator_info: dict or tuple with locator info
        :return: locator tuple
        """
        if isinstance(locator_info, dict):
            return locator_info.get(get_env_var("EXECUTE_ON").lower())
        return locator_info

    def _tap_on_element(self, locator_info, timeout=_wait_time):
        """
        Touch action: Tap on element
        :param locator_info: contains unique locator type and
        locator value
        :param timeout: wait time
        :return: none
        """
        element = self._get_element(locator_info, wait=timeout)

        if element:
            touch = TouchAction(self._driver)
            touch.tap(element).perform()
            log.info("Tapped on element with " + str(locator_info))
        else:
            log.info("Element is not present with " + str(locator_info))
            raise exc.NoSuchElementException

    @staticmethod
    def _get_element_inside_of_element(element, locator_info):
        """
        Get an element inside another element
        :param element: already located element
        :param locator_info: locator of element to locate
        :return: located element
        """
        try:
            in_element = element.find_element(*locator_info)
        except exc.NoSuchElementException:
            return False
        return in_element

    @allure.step("Get the element")
    def _get_element(self, locator: tuple, wait=_wait_time):
        """
         Get element
        :param locator: An element given a By strategy and locator.
         :param wait: Amount of time to wait (in seconds).
         :return: The element once it is located.
        """
        try:
            return self._get_wait(wait).until(ec.presence_of_element_located(locator))
        except (exc.TimeoutException, exc.NoSuchElementException) as ex:
            log.error("Element {} not found {}".format(locator[1], ex.msg))

    def _get_elements(self, locator, wait=_wait_time):
        """
         Get list of elements
        :param locator: An element given a By strategy and locator.
         :param wait: Amount of time to wait (in seconds).
         :return: Element list
        """
        try:
            return self._get_wait(wait).until(ec.presence_of_all_elements_located(locator))
        except (exc.TimeoutException, exc.NoSuchElementException) as ex:
            log.error("Elements {} were not found {}".format(locator[1], ex))

    @allure.step("Switch to frame")
    def _switch_to_frame(self, locator, wait=_wait_time):
        """
         This function expects for checking that an iframe is present.
        :param locator: An element given a By strategy and locator.
         :param wait: Amount of time to wait (in seconds).
         :return: Perform switch to the iframe
        """
        log.info("Switch to frame {}".format(locator[1]))
        return self._get_wait(wait).until(ec.frame_to_be_available_and_switch_to_it(locator))

    @allure.step("Switch to default content")
    def switch_to_default_content(self):
        """
        This functions switches from iframe section to default content.
        """
        self._driver.switch_to.default_content()

    @allure.step("Wait for page element to disappear")
    def _wait_element_disappear(self, locator: Union[tuple, WebElement], wait=_wait_time):
        """
         Wait for page element to disappear
        :param locator: An element given a By strategy and locator. tuple with locator info
         :param wait: Amount of time to wait (in seconds). wait time
        """
        log.info("Wait for element {} to disappear".format(locator))
        try:
            element = self._get_element(locator, NO_WAIT) if type(locator) == tuple else locator
            self._get_wait(wait).until(ec.invisibility_of_element(element))
        except (exc.NoSuchElementException, exc.TimeoutException, TypeError):
            log.info("Element is not present anymore")

    @allure.step("Click on element")
    def _click_on_element(self, locator: Union[tuple, WebElement], wait=_wait_time):
        """
         This function clicks on web element.
        :param locator: An element given a By strategy and locator.
         :param wait: Amount of time to wait (in seconds).
        """
        try:
            if type(locator) == tuple:
                log.info("Click on element {}".format(locator[1]))
                element = WebDriverWait(self._driver, wait).until(
                    ec.element_to_be_clickable(locator)
                )
            else:
                log.info("Click on element")
                element = locator
            element.click()
        except (
            exc.ElementClickInterceptedException,
            exc.TimeoutException,
            exc.ElementNotInteractableException,
        ) as ex:
            log.error("Was not possible to click on element {}".format(ex.msg))
            self.take_screenshot()

    @allure.step("Click JS on element")
    def _js_click(self, locator, wait=_wait_time):
        """
         Click on element by JS script
        :param locator: An element given a By strategy and locator.
         :param wait: Amount of time to wait (in seconds).
         :return: Perform click action.
        """
        element = self._get_element(locator, wait)
        return self._driver.execute_script("arguments[0].click();", element)

    @allure.step("Type into the element")
    def _send_text(self, locator, str_keys, clear=True, wait=_wait_time):
        """
         This function simulates typing into the element, this can also be used to set file inputs.
        :param locator: An element given a By strategy and locator.
         :param str_keys: A string for typing, or setting form fields.
         :param wait: Amount of time to wait (in seconds).
        """
        log.info("Send text to element {} {}".format(locator[1], str_keys))
        try:
            element = self._get_element(locator, wait)
            if clear:
                element.clear()
            element.send_keys(str_keys)
        except exc.NoSuchElementException:
            log.error("Set text was not possible")

    @allure.step("Check if element is displayed")
    def _is_element_displayed(self, locator: Union[tuple, WebElement], wait=_wait_time):
        """
        This function is an expectation for checking that an element is present on the DOM of a
        page and visible. Visibility means that the element is not only displayed
        but also has a height and width that is greater than 0.
        :param locator: An element given a By strategy and locator.
        :param wait: Amount of time to wait (in seconds).
        :return: Boolean value.
        """
        locator_name = ""
        try:
            if type(locator) == tuple:
                locator_name = locator[1]
                element = self._get_wait(wait).until(ec.visibility_of_element_located(locator))
            else:
                element = locator

            if element.is_displayed():
                log.info("Element {} is displayed".format(locator_name))
                return True
            else:
                log.error("Element {} is not displayed".format(locator_name))
                return False
        except (exc.NoSuchElementException, exc.TimeoutException):
            log.error("Element not found " + locator[1] if type(locator) == tuple else "")
            return False

    @allure.step("Go one step backward in the driver history")
    def back_to_the_previous_page(self):
        """
        This function goes one step backward in the driver history.
        """
        self._driver.back()

    @allure.step("Refresh the page")
    def refresh_page(self):
        """
        This function refreshes the current page.
        """
        log.info("Refresh the page")
        self._driver.refresh()

    @allure.step("Move to an element")
    def _move_to_element(self, locator, wait=_wait_time):
        """
         Moves to an element
        :param locator: An element given a By strategy and locator. string
        :param wait: Amount of time to wait (in seconds). int
        :return: Boolean
        """
        log.info("Moves to an element")
        element = self._get_element(locator, wait)
        if isinstance(element, WebElement):
            action = ActionChains(self._driver)
            action.move_to_element(element).perform()
        else:
            raise exc.NoSuchElementException("Element was not located")

    @allure.step("Scroll to a specific element")
    def _scroll_to_an_element_js(self, locator, wait=_wait_time):
        """
        Scrolls to a specific element
        :param locator: An element given a By strategy and locator.
        :param wait: Amount of time to wait (in seconds).
        """
        log.info("Scroll down to the bottom of the page")
        element = self._get_element(locator, wait)
        self._driver.execute_script("arguments[0].scrollIntoView();", element)

    @allure.step("Scroll down to the bottom of the page")
    def _scroll_down_to_the_bottom_of_the_page(self):
        """
        Performs a scroll down to the bottom of the webpage
        """
        log.info("Scroll down to the bottom of the page")
        self._driver.execute_script("window.scrollBy(0,document.body.scrollHeight)")

    @allure.step("Scroll up to top page")
    def _scroll_to_top_page(self):
        """
        Scroll up to top page
        """
        log.info("Scroll up to top page")
        self._driver.execute_script("window.scrollBy(0, -document.body.scrollHeight)")

    @allure.step("Open a new tab")
    def _open_a_new_tab(self):
        """This method open a new window on current driver"""
        self._driver.switch_to.new_window("tab")

    @allure.step("Close the window opened")
    def _close_new_tab_opened(self):
        """This method close a new window opened"""
        self._driver.close()
        self._driver.switch_to.window(self._driver.window_handles[0])

    @allure.step("Get the page")
    def _get_the_page(self, web_site):
        """This method gets the url to get it"""
        self._driver.get(web_site)

    @allure.step("Check if text is in element")
    def _is_text_in_element(self, locator, text, wait=_wait_time):
        """
        Check if text is in element
        :param locator: An element given a By strategy and locator. tuple with locator info
        :param text: texto to check
        :param wait: Amount of time to wait (in seconds). wait time on locator
        :return: Boolean
        """
        log.info("Check if text [{}] is in element {}".format(text, locator))
        try:
            return self._get_element(locator, wait).text == text
        except AttributeError:
            return False

    def take_screenshot(self):
        """
        Take screenshot for allure and local
        """
        if eval(get_env_var("SCREENSHOT", "True")):
            file_dir = os.path.join(BASE_DIR, "output")
            date_time = get_current_time()
            full_file = Path(os.path.join(file_dir, "{}.png".format(date_time)))
            if not os.path.exists(file_dir):
                os.mkdir(file_dir)
            png = b64decode(self._driver.get_screenshot_as_base64().encode("ascii"))
            with open(full_file, "wb") as f:
                f.write(png)
            allure.attach.file(full_file)
            log.warning("Screenshot taken placed in {}".format(full_file))

    @allure.step("Get element by text on list of elements")
    def _get_element_on_list_by_text(self, locator, text):
        """
        Get element by text on list of elements
        :param locator: An element given a By strategy and locator. tuple
        :param text: string
        :return: element found
        """
        log.info("Get element by text on list of elements")

        try:
            elem_list = list(filter(lambda x: x.text == text, self._get_elements(locator)))
            return elem_list[0]
        except IndexError:
            pass
        raise IndexError("{} was not found in list".format(text))

    @allure.step("Get element attribute")
    def _get_attribute(self, locator, attr):
        """
        Get element attribute
        :param locator: An element given a By strategy and locator. tuple with locator info
        :param attr: attribute to find
        :return: attribute value
        """
        log.info("Get element attribute")
        return self._get_element(locator).get_attribute(attr)

    @allure.step("Get Shadow element")
    def get_shadow_element(self, shadow, locator, wait=_wait_time, elem_list=False):
        """
        Get Shadow element
        :param elem_list: if is a list of elements
        :param shadow: father locator
        :param locator: An element given a By strategy and locator. element to find
        :param wait: wait number
        :return: element
        """
        log.info("Get Shadow element")
        shadow_host = self._get_element(shadow, wait)
        if get_env_browser() == "firefox":
            return self._driver.execute_script(
                "return arguments[0].shadowRoot.children", shadow_host
            )
        else:
            shadow_root = shadow_host.shadow_root
            if elem_list:
                return shadow_root.find_elements(locator[0], locator[1])
            else:
                return shadow_root.find_element(locator[0], locator[1])

    def is_responsive(self):
        """
        Check if execution is responsive
        :return: true if is not desktop size
        """
        return self._driver.get_window_size()["width"] != WindowSize.desktop.value

    def get_locator_by_size(self, locator):
        """
        Get locators by responsive size if needed
        :param locator: locator info can be dict or  tuple
        :return: tuple with locator
        """
        if type(locator) == dict:
            if self.is_responsive():
                return locator.get(WindowSize.tablet.name)
            else:
                return locator.get(WindowSize.desktop.name)
        else:
            return locator

    @staticmethod
    def get_locator_by_env(locator):
        """
        Get locators by responsive size if needed
        :param locator: locator info can be dict or  tuple
        :return: tuple with locator
        """
        env = get_env()
        if type(locator) == dict:
            if env in locator:
                return locator.get(env)
            else:
                return locator.get("default")
        else:
            return locator

    def _get_text(self, locator_info):
        """
        Get element text
        :param locator_info: tuple or dict
        :return: element text
        """
        element = self._get_element(locator_info)
        return element.text if element else None
