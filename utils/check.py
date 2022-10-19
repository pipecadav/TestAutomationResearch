import allure
import pytest_check
from loguru import logger as log

from web.base_screen import BaseScreen

ASSERT_PASS = "ASSERT PASS: expecting [{}] message: {}"


class Check:
    """
    Soft assertions class
    """

    base = BaseScreen()

    def log_failure(self, actual, expected, msg):
        """
        Log assertion failure and take screenshot
        :param actual: value to check
        :param expected: value to check
        :param msg: to log
        """
        self.base.take_screenshot()
        log.error(
            "ASSERT FAILED: expecting [{}] actual [{}] message: {}".format(expected, actual, msg)
        )

    @allure.step("Assert true for: [{actual}] {msg}")
    def is_true(self, actual, msg="", hard=False):
        """
        Check if true
        :param hard: assertion
        :param actual: actual value
        :param msg: to log
        """
        if not actual:
            self.log_failure(actual, True, msg)
        else:
            log.success(ASSERT_PASS.format(True, msg))
        if hard:
            assert actual, msg
        else:
            pytest_check.is_true(actual, msg)

    @allure.step("Assert false for: [{actual}] {msg}")
    def is_false(self, actual, msg="", hard=False):
        """
        Check if false
        :param hard: assertion
        :param actual: actual value
        :param msg: to log
        """
        if actual:
            self.log_failure(actual, False, msg)
        else:
            log.success(ASSERT_PASS.format(False, msg))
        if hard:
            assert not actual, msg
        else:
            pytest_check.is_false(actual, msg)

    @allure.step("Assert [{actual}] is equals to [{expected}] {msg}")
    def equal(self, actual, expected, msg="", hard=False):
        """
        Check if 2 values are equals
        :param hard: assertion
        :param actual: value to check
        :param expected: value to check
        :param msg: to log
        """
        if actual != expected:
            self.log_failure(actual, expected, msg)
        else:
            log.success(ASSERT_PASS.format(expected, msg))
        if hard:
            assert actual == expected, msg
        else:
            pytest_check.equal(actual, expected, msg)

    @allure.step("Assert [{actual}] is not equals to [{expected}] {msg}")
    def not_equal(self, actual, expected, msg="", hard=False):
        """
        Check if 2 values are not equals
        :param hard: assertion
        :param actual: value to check
        :param expected: value to check
        :param msg: to log
        """
        if actual == expected:
            self.log_failure(actual, expected, msg)
        else:
            log.success(ASSERT_PASS.format(expected, msg))
        if hard:
            assert actual != expected, msg
        else:
            pytest_check.not_equal(actual, expected, msg)
