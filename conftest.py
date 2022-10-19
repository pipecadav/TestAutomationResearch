import pytest
from _pytest.fixtures import fixture
from loguru import logger as log

from screens.base_screen import BaseScreen
from services.xray import XrayAPI
from utils.common import get_current_time
from utils.constants import XRAY_DATE
from utils.driver import Driver

driver = Driver()


def send_xray_results(start, request):
    """
    Send Xray results and take screenshot if test fails
    :param start: start test time
    :param request: test outcome
    """
    result = request.node.rep_call
    if result.outcome == "failed":
        BaseScreen().take_screenshot()
    XrayAPI().send_xray_results(start, get_current_time(formatter=XRAY_DATE), result)


@fixture()
def mobile_setup(request):
    """
    Mobile setup
    """
    log.info("Starting Mobile Setup")
    start = get_current_time(formatter=XRAY_DATE)
    mobile_driver = BaseScreen._driver = driver.init_mobile_driver()
    yield
    log.info("Mobile teardown")
    send_xray_results(start, request)
    mobile_driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_make_report(item):
    """
    Pytest method to get failures
    :param item: test item
    """
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_call", rep)


@fixture(scope="function")
def web_setup(request):
    """
    Setup automation fixture
    :param request: function
    """
    log.info("Web setup")
    start = get_current_time(formatter=XRAY_DATE)
    BaseScreen._driver = web_driver = driver.init_driver()
    yield
    log.info("Web teardown")
    send_xray_results(start, request)
    web_driver.quit()
